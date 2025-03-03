from datetime import datetime

from cryptography.hazmat.primitives.serialization import Encoding
from oslo_log import log as logging

from certx.common import exceptions
from certx.db import api as db_api
from certx.db.model import models as db_model
from certx.common.model import model
from certx.provider import crypto
from certx import service
from certx.service.certificate_authority_service import CertificateAuthorityService
from certx.utils.crypto import x509_tools
from certx.utils import generator

logger = logging.getLogger(__name__)


class CertificateAuthorityServiceImpl(CertificateAuthorityService):
    def __init__(self, **kwargs):
        pass

    def create_certificate_authority(self, ca_option) -> model.PrivateCertificateAuthority:
        key_algorithm = ca_option.get('key_algorithm')
        signature_algorithm = ca_option.get('signature_algorithm')
        logger.info('generate CA private key...')
        _key_provider = crypto.get_key_provider(key_algorithm)
        ca_key = _key_provider.generate_private_key()

        ca_dn = model.DistinguishedName(**ca_option.get('distinguished_name'))
        ca_subject = ca_dn.build_subject()
        ca_validity = model.Validity(**ca_option.get('validity'))
        not_before = datetime.utcfromtimestamp(
            ca_validity.start_from) if ca_validity.start_from is not None else datetime.utcnow()
        not_after = not_before + ca_validity.get_effective_time()

        logger.info('generate CA...')
        ca_cert = x509_tools.generate_ca_certificate(subject_name=ca_subject, root_key=ca_key, not_before=not_before,
                                                     not_after=not_after,
                                                     signature_algorithm=signature_algorithm.to_alg())

        key_pass = generator.gen_password()

        logger.info('generate CA resource...')
        resource_service = service.get_resource_service()
        ca_uri = resource_service.save_certificate(
            model.CertificateResourceType.CA,
            ca_cert.public_bytes(Encoding.PEM),
            _key_provider.get_private_bytes(ca_key, password=key_pass))

        ca = db_model.PrivateCertificateAuthorityModel(id=generator.gen_uuid(),
                                                       type=ca_option.get('type').value,
                                                       status=model.CaStatus.ISSUE.value,
                                                       path_length=0,
                                                       issuer_id=None,
                                                       key_algorithm=key_algorithm.value,
                                                       signature_algorithm=signature_algorithm.value,
                                                       serial_number=str(ca_cert.serial_number),
                                                       not_before=not_before,
                                                       not_after=not_after,
                                                       common_name=ca_dn.common_name,
                                                       country=ca_dn.country,
                                                       state=ca_dn.state,
                                                       locality=ca_dn.locality,
                                                       organization=ca_dn.organization,
                                                       organization_unit=ca_dn.organization_unit,
                                                       uri=ca_uri,
                                                       password=crypto.encrypt(key_pass))
        try:
            db_api.save_object(ca)
        except Exception as e:
            logger.error('Save CA failed, delete resource file %s...', ca_uri, e)
            resource_service.delete_certificate(ca_uri)
            raise exceptions.ServiceException('Create CA failed')

        return model.PrivateCertificateAuthority.from_db(ca)

    def list_certificate_authorities(self, query_option):
        return [model.PrivateCertificateAuthority.from_db(ca) for ca in db_api.list_all_ca()]

    def get_certificate_authority(self, ca_id) -> model.PrivateCertificateAuthority:
        ca = db_api.query_by_id(ca_id, db_model.PrivateCertificateAuthorityModel)
        if ca is None:
            logger.error('CA {} not found'.format(ca_id))
            raise exceptions.ServiceException('CA {} not found'.format(ca_id))
        return model.PrivateCertificateAuthority.from_db(ca)

    def delete_certificate_authority(self, ca_id):
        certs = db_api.list_all_ca(db_model.PrivateCertificateModel)
        if certs:
            logger.error('CA {} has signed certificate, could not be deleted'.format(ca_id))
            raise exceptions.CaSignedCertificate('CA {} has signed certificate, could not be deleted'.format(ca_id))

        ca = self.get_certificate_authority(ca_id)
        logger.info('delete CA {}'.format(ca_id))
        db_api.delete_by_id(ca_id, db_model.PrivateCertificateAuthorityModel)
        logger.info('delete CA {} resource with uri {}'.format(ca_id, ca.uri))
        service.get_resource_service(ca.uri).delete_certificate(ca.uri)

    def export_certificate_authority(self, ca_id) -> model.CertificateContent:
        ca = self.get_certificate_authority(ca_id)
        ca_resource = service.get_resource_service(ca.uri).load_certificate(ca.uri)
        return model.CertificateContent(certificate=ca_resource.certificate_data)
