from datetime import datetime

from cryptography.hazmat.primitives.serialization import Encoding
from oslo_log import log as logging

from certx.common import exceptions
from certx.db import api as db_api
from certx.db.model import models as db_model
from certx.common.model import model
from certx.provider import crypto
from certx import service
from certx.service.certificate_service import CertificateService
from certx.utils import algorithm_util
from certx.utils.crypto import x509_tools
from certx.utils import generator

logger = logging.getLogger(__name__)


class CertificateServiceImpl(CertificateService):
    def __init__(self, **kwargs):
        pass

    def create_certificate(self, cert_option) -> model.PrivateCertificate:
        issue_id = cert_option.get('issue_id')
        ca_model = db_api.query_by_id(issue_id, db_model.PrivateCertificateAuthorityModel)
        if ca_model is None:
            logger.error('CA %s not found.', issue_id)
            raise exceptions.NotFoundException('CA {} not found.'.format(issue_id))

        # Load CA
        resource_service = service.get_resource_service(ca_model.uri)
        ca_resource = resource_service.load_certificate(ca_model.uri)
        ca_cert = x509_tools.load_pem_x509_certificate(ca_resource.certificate_data)

        _ca_key_provider = crypto.get_key_provider(model.KeyAlgorithm(ca_model.key_algorithm))
        ca_key = _ca_key_provider.load_private_key(ca_resource.private_key_data,
                                                   password=crypto.decrypt(ca_model.password))

        key_algorithm = cert_option.get('key_algorithm') if cert_option.get(
            'key_algorithm') else model.KeyAlgorithm(ca_model.key_algorithm)
        signature_algorithm = cert_option.get('signature_algorithm') if cert_option.get(
            'signature_algorithm') else model.SignatureAlgorithm(ca_model.signature_algorithm)

        if not algorithm_util.validate_key_and_signature_algorithm(key_algorithm, signature_algorithm):
            msg = 'unmatched key_algorithm {} and signature_algorithm {}'.format(
                key_algorithm.value, signature_algorithm.value)
            logger.error(msg)
            raise exceptions.InvalidInput(msg)

        # Generate certificate
        _cert_key_provider = crypto.get_key_provider(key_algorithm)
        cert_key = _cert_key_provider.generate_private_key()

        # DN
        cert_dn_option = cert_option.get('distinguished_name')
        cert_dn_country = cert_dn_option.get('country')
        cert_dn_state = cert_dn_option.get('state')
        cert_dn_locality = cert_dn_option.get('locality')
        cert_dn_organization = cert_dn_option.get('organization')
        cert_dn_organization_unit = cert_dn_option.get('organization_unit')
        cert_dn = model.DistinguishedName(
            common_name=cert_dn_option.get('common_name'),
            country=cert_dn_country if cert_dn_country else ca_model.country,
            state=cert_dn_state if cert_dn_state else ca_model.state,
            locality=cert_dn_locality if cert_dn_locality else ca_model.locality,
            organization=cert_dn_organization if cert_dn_organization else ca_model.organization,
            organization_unit=cert_dn_organization_unit if cert_dn_organization_unit else ca_model.organization_unit)

        # Generate CSR
        server_csr = x509_tools.generate_csr(cert_key, cert_dn.build_subject(), signature_algorithm.to_alg())

        cert_validity = model.Validity(**cert_option.get('validity'))
        not_before = datetime.utcfromtimestamp(
            cert_validity.start_from) if cert_validity.start_from is not None else datetime.utcnow()
        not_after = not_before + cert_validity.get_effective_time()

        # Generate Certificate
        cert = x509_tools.generate_certificate(server_csr.subject, ca_cert.subject, ca_key,
                                               server_csr.public_key(), signature_algorithm.to_alg(),
                                               not_before, not_after)

        # Save certificate and private key
        key_pass = generator.gen_password()
        cert_uri = resource_service.save_certificate(
            model.CertificateResourceType.CERTIFICATE,
            cert.public_bytes(Encoding.PEM),
            _cert_key_provider.get_private_bytes(cert_key, password=key_pass))

        cert = db_model.PrivateCertificateModel(id=generator.gen_uuid(),
                                                status=model.CaStatus.ISSUE.value,
                                                issuer_id=ca_model.id,
                                                key_algorithm=key_algorithm.value,
                                                signature_algorithm=signature_algorithm.value,
                                                serial_number=str(ca_cert.serial_number),
                                                not_before=not_before,
                                                not_after=not_after,
                                                common_name=cert_dn.common_name,
                                                country=cert_dn.country,
                                                state=cert_dn.state,
                                                locality=cert_dn.locality,
                                                organization=cert_dn.organization,
                                                organization_unit=cert_dn.organization_unit,
                                                uri=cert_uri,
                                                password=crypto.encrypt(key_pass))
        try:
            db_api.save_object(cert)
        except Exception as e:
            logger.error('Save certificate failed, delete resource file %s...', cert_uri, e)
            resource_service.delete_certificate(cert_uri)
            raise exceptions.ServiceException('Create certificate failed')

        return model.PrivateCertificate.from_db(cert)

    def list_certificates(self):
        return [model.PrivateCertificate.from_db(ca) for ca in db_api.list_all_ca(db_model.PrivateCertificateModel)]

    def get_certificate(self, cert_id) -> model.PrivateCertificate:
        cert = db_api.query_by_id(cert_id, db_model.PrivateCertificateModel)
        if cert is None:
            logger.error('certificate %s not found', cert_id)
            raise exceptions.NotFoundException('certificate {} not found'.format(cert_id))
        return model.PrivateCertificate.from_db(cert)

    def delete_certificate(self, cert_id):
        cert = self.get_certificate(cert_id)
        db_api.delete_by_id(cert_id, db_model.PrivateCertificateModel)
        service.get_resource_service(cert.uri).delete_certificate(cert.uri)

    def export_certificate(self, cert_id, export_option) -> model.CertificateContent:
        cert = self.get_certificate(cert_id)
        ca_model = db_api.query_by_id(cert.issue_id, db_model.PrivateCertificateAuthorityModel)
        if ca_model is None:
            logger.error('CA %s not found.', cert.issue_id)
            raise exceptions.NotFoundException('CA {} not found.'.format(cert.issue_id))

        cert_resource = service.get_resource_service(cert.uri).load_certificate(cert.uri)

        _cert_key_provider = crypto.get_key_provider(cert.key_algorithm)
        cert_key = _cert_key_provider.load_private_key(cert_resource.private_key_data,
                                                       password=crypto.decrypt(cert.password))

        user_pass = export_option.get('password')

        ca_resource = service.get_resource_service(ca_model.uri).load_certificate(ca_model.uri)
        return model.CertificateContent(
            certificate=cert_resource.certificate_data,
            private_key=_cert_key_provider.get_private_bytes(cert_key, password=user_pass),
            certificate_chain=[ca_resource.certificate_data])
