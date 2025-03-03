import os
from pathlib import Path
import shutil
import uuid

from oslo_log import log as logging

from certx.common import exceptions
from certx.db import api as db_api
from certx.db.model import models as db_model
from certx.common.model import model
from certx.service import resource_service
from certx.utils import generator

logger = logging.getLogger(__name__)

local_folder = 'cert-repo'


class FileCertificateResourceServiceImpl(resource_service.CertificateResourceService):
    URI_TYPE = 'file'
    CERT_FILE_TAG = 'cert.crt'
    PRIVATE_KEY_FILE_TAG = 'cert.key'

    def _get_base_path(self):
        return Path(local_folder)

    def _check_base_path(self):
        if not os.path.exists(Path(local_folder)):
            os.makedirs(local_folder)

    def _gen_location(self, certificate_type: model.CertificateResourceType):
        location = os.path.join(local_folder, '{}#{}'.format(certificate_type.value, str(uuid.uuid4())))
        if not os.path.exists(location):
            os.makedirs(location)
        return location

    def _get_certificate_type(self, resource_uri):
        return resource_uri.split('#')[-1]

    def _save_certificate(self, certificate_type: model.CertificateResourceType, certificate_data: bytes,
                          private_key_data: bytes) -> str:
        self._check_base_path()
        uri_id = self._gen_location(certificate_type)

        if certificate_data is not None:
            cert_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.CERT_FILE_TAG)
            with open(cert_path, 'wb') as cp:
                cp.write(certificate_data)

        if private_key_data is not None:
            key_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.PRIVATE_KEY_FILE_TAG)
            with open(key_path, 'wb') as kp:
                kp.write(private_key_data)
        return resource_service.build_resource_uri(FileCertificateResourceServiceImpl.URI_TYPE, uri_id)

    def load_certificate(self, resource_uri) -> model.CertificateResource:
        _, uri_id = resource_service.analyze_resource_uri(resource_uri)

        if not os.path.exists(uri_id):
            logger.error('certificate file path does not exist. {}'.format(uri_id))
            raise exceptions.ServiceException('certificate file does not exist.')

        certificate_type = self._get_certificate_type(resource_uri)

        cert_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.CERT_FILE_TAG)
        if not os.path.exists(cert_path):
            logger.error('certificate file does not exist. {}'.format(cert_path))
            raise exceptions.ServiceException('certificate file does not exist.')

        with open(cert_path, 'rb') as cp:
            cert_data = cp.read()

        key_path = os.path.join(uri_id, FileCertificateResourceServiceImpl.PRIVATE_KEY_FILE_TAG)
        private_key_data = None
        if os.path.exists(key_path):
            with open(key_path, 'rb') as kp:
                private_key_data = kp.read()

        return model.CertificateResource(certificate_type=certificate_type,
                                         certificate_data=cert_data,
                                         private_key_data=private_key_data)

    def delete_certificate(self, resource_uri: str):
        _, uri_id = resource_service.analyze_resource_uri(resource_uri)
        if not os.path.exists(uri_id):
            logger.info('certificate file path does not exist, ignore to delete. path={}'.format(uri_id))
            return
        shutil.rmtree(uri_id)


class DbCertificateResourceServiceImpl(resource_service.CertificateResourceService):
    URI_TYPE = 'db'

    def _save_certificate(self, certificate_type: model.CertificateResourceType, certificate_data: bytes,
                          private_key_data: bytes) -> str:
        certificate_resource = db_model.CertificateResourceModel(
            id=generator.gen_uuid(),
            certificate_type=certificate_type.value,
            certificate_data=certificate_data,
            private_key_data=private_key_data)
        db_api.save_object(certificate_resource)
        return resource_service.build_resource_uri(uri_type=DbCertificateResourceServiceImpl.URI_TYPE,
                                                   uri_id=certificate_resource.id)

    def load_certificate(self, resource_uri: str) -> model.CertificateResource:
        _, obj_id = resource_service.analyze_resource_uri(resource_uri)
        cert_res_model = db_api.query_by_id(obj_id, db_model.CertificateResourceModel)
        if cert_res_model is None:
            logger.log('Certificate resource not found. resource_uri={}'.format(resource_uri))
            raise exceptions.ServiceException('Certificate resource not found')
        return model.CertificateResource(certificate_type=cert_res_model.certificate_type,
                                         certificate_data=cert_res_model.certificate_data,
                                         private_key_data=cert_res_model.private_key_data)

    def delete_certificate(self, resource_uri: str):
        _, obj_id = resource_service.analyze_resource_uri(resource_uri)
        db_api.delete_by_id(obj_id, db_model.CertificateResourceModel)
