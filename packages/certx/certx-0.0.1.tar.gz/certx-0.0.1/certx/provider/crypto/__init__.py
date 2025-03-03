from . import key
from . import password

from certx.common.model import model


def get_crypto():
    return password.DefaultPasswordEncoder()


def encrypt(row_data):
    return get_crypto().encrypt(row_data)


def decrypt(cipher_data):
    return get_crypto().decrypt(cipher_data)


_KEY_PROVIDER_MAP = {
    model.KeyAlgorithm.RSA2048: key.RsaKeyProvider,
    model.KeyAlgorithm.RSA3072: key.RsaKeyProvider,
    model.KeyAlgorithm.RSA4096: key.RsaKeyProvider,
    model.KeyAlgorithm.EC256: key.EcKeyProvider,
    model.KeyAlgorithm.EC384: key.EcKeyProvider,
    model.KeyAlgorithm.SM2: key.SmKeyProvider,
}


def get_key_provider(key_algorithm: model.KeyAlgorithm):
    if key_algorithm not in _KEY_PROVIDER_MAP:
        raise NotImplemented

    return _KEY_PROVIDER_MAP.get(key_algorithm)(key_algorithm.value)
