from abc import ABC, abstractmethod

from certx.common.model import model


class CertificateService(ABC):
    @abstractmethod
    def create_certificate(self, cert_option) -> model.PrivateCertificate:
        pass

    @abstractmethod
    def list_certificates(self):
        pass

    @abstractmethod
    def get_certificate(self, cert_id) -> model.PrivateCertificate:
        pass

    @abstractmethod
    def delete_certificate(self, cert_id) -> model.PrivateCertificate:
        pass

    @abstractmethod
    def export_certificate(self, cert_id, export_option) -> model.CertificateContent:
        """导出证书
        :param cert_id 证书ID
        :param export_option 导出参数
        :param export_option.type 导出证书的格式
        :param export_option.password 证书密钥密码，如不提供，则返回未加密的证书
        :return 证书内容，包括 证书、证书链、密钥文件 等
        """
        pass
