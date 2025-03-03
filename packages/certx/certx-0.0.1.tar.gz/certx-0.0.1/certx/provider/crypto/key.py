import abc

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import BestAvailableEncryption, Encoding, NoEncryption, PrivateFormat
from oslo_log import log as logging

from certx.common import exceptions

logger = logging.getLogger(__name__)


class KeyProvider(abc.ABC):
    def __init__(self, key_algorithm, **kwargs):
        self.key_algorithm = key_algorithm
        self.kwargs = kwargs

    @abc.abstractmethod
    def generate_private_key(self):
        pass

    @abc.abstractmethod
    def get_private_bytes(self, private_key, password: str = None):
        pass

    @abc.abstractmethod
    def load_private_key(self, private_key_bytes, password: str = None):
        pass


RSA_KEY_SIZE_MAP = {
    'RSA2048': 2048,
    'RSA3072': 3072,
    'RSA4096': 4096
}


class RsaKeyProvider(KeyProvider):
    def generate_private_key(self):
        if self.key_algorithm not in RSA_KEY_SIZE_MAP:
            logger.error('unsupported key_algorithm {}'.format(self.key_algorithm))
            raise exceptions.ServiceException('unsupported key_algorithm {}'.format(self.key_algorithm))
        return rsa.generate_private_key(public_exponent=65537,
                                        key_size=RSA_KEY_SIZE_MAP.get(self.key_algorithm),
                                        backend=default_backend())

    def get_private_bytes(self, private_key, password: str = None):
        encryption = BestAvailableEncryption(password.encode('utf-8')) if password else NoEncryption()
        return private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, encryption)

    def load_private_key(self, private_key_bytes, password: str = None):
        return serialization.load_pem_private_key(private_key_bytes, password=password.encode('utf-8'))


CURVE_MAP = {
    'EC256': ec.SECP256R1,
    'EC384': ec.SECP384R1,
}


class EcKeyProvider(KeyProvider):
    def generate_private_key(self):
        if self.key_algorithm not in CURVE_MAP:
            logger.error('unsupported key_algorithm {}'.format(self.key_algorithm))
            raise exceptions.ServiceException('unsupported key_algorithm {}'.format(self.key_algorithm))
        return ec.generate_private_key(CURVE_MAP.get(self.key_algorithm)(), default_backend())

    def get_private_bytes(self, private_key, password: str = None):
        encryption = BestAvailableEncryption(password.encode('utf-8')) if password else NoEncryption()
        return private_key.private_bytes(Encoding.PEM, PrivateFormat.PKCS8, encryption)

    def load_private_key(self, private_key_bytes, password: str = None):
        return serialization.load_pem_private_key(private_key_bytes, password=password.encode('utf-8'))


class SmKeyProvider(KeyProvider):
    def generate_private_key(self):
        raise exceptions.NotImplementException("GM algorithm not supported")

    def get_private_bytes(self, private_key, password: str = None):
        raise exceptions.NotImplementException()

    def load_private_key(self, private_key_bytes, password: str = None):
        raise exceptions.NotImplementException()
