from abc import ABC, abstractmethod
from typing import List

from certx.common.model import model


class CertificateAuthorityService(ABC):
    @abstractmethod
    def create_certificate_authority(self, ca_option) -> model.PrivateCertificateAuthorityModel:
        pass

    @abstractmethod
    def list_certificate_authorities(self, query_option) -> List[model.PrivateCertificateAuthority]:
        pass

    @abstractmethod
    def get_certificate_authority(self, ca_id) -> model.PrivateCertificateAuthorityModel:
        pass

    @abstractmethod
    def delete_certificate_authority(self, ca_id):
        pass

    @abstractmethod
    def export_certificate_authority(self, ca_id) -> model.CertificateContent:
        pass
