import datetime

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509.base import Certificate
from cryptography.x509.extensions import Extension


def generate_ca_certificate(subject_name: x509.Name,
                            root_key,
                            signature_algorithm,
                            not_before=None,
                            not_after=None,
                            serial_number: int = None,
                            key_usage: x509.KeyUsage = None) -> Certificate:
    """ Generate Certificate Authority
    :param subject_name: the subject
    :param root_key: CA private key
    :param signature_algorithm: the signature hash algorithm
    :param not_before:
    :param not_after:
    :param serial_number:
    :param key_usage:
    :return:
    """
    extension_types = [x509.BasicConstraints(ca=True, path_length=None)]
    if key_usage is None:
        # default key usage for CA: digitalSignature,keyCertSign,cRLSign
        key_usage = x509.KeyUsage(True, False, False, False, False, True, True, False, False)
    extension_types.append(key_usage)
    return generate_certificate(subject_name, subject_name, root_key, root_key.public_key(), signature_algorithm,
                                not_before=not_before,
                                not_after=not_after,
                                serial_number=serial_number,
                                extension_types=extension_types)


def generate_csr(private_key, subject, signature_algorithm):
    """Generate certificate CSR
    :param private_key: the certificate private keu
    :param subject: the certificate subject
    :param signature_algorithm: the signature hash algorithm
    :return:
    """
    return x509.CertificateSigningRequestBuilder().subject_name(subject).sign(private_key, signature_algorithm,
                                                                              default_backend())


def generate_certificate(subject_name: x509.Name,
                         issuer_name: x509.Name,
                         private_key,
                         public_key,
                         signature_algorithm,
                         not_before=None,
                         not_after=None,
                         serial_number: int = None,
                         extension_types=None) -> Certificate:
    """ Generate certificate
    :param subject_name: the certificate subject
    :param issuer_name: the issuer name。it should equals to subject_name when generate CA
    :param private_key: the issuer's private key
    :param public_key: the certificate public key. From CSR when generate common certificate or from CA private key
                       when generate CA
    :param signature_algorithm: the signature hash algorithm
    :param not_before:
    :param not_after:
    :param serial_number:
    :param extension_types:
    :return:
    """
    if not_before is None:
        not_before = datetime.datetime.utcnow()

    if not_after is None:
        not_after = not_before

    extensions = []
    if extension_types is not None and isinstance(extension_types, list):
        for extension in extension_types:
            extensions.append(Extension(extension.oid, False, extension))

    return (x509.CertificateBuilder(extensions=extensions)
            .subject_name(subject_name)
            .issuer_name(issuer_name)
            .public_key(public_key)
            .serial_number(x509.random_serial_number() if serial_number is None else serial_number)
            .not_valid_before(not_before)
            .not_valid_after(not_after)
            .sign(private_key, signature_algorithm, default_backend()))


def load_pem_x509_certificate(certificate_data) -> Certificate:
    return x509.load_pem_x509_certificate(certificate_data)
