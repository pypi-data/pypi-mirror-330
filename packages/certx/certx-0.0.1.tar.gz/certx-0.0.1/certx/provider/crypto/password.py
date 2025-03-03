import abc


class PasswordEncoder(abc.ABC):
    @abc.abstractmethod
    def encrypt(self, row_data):
        pass

    @abc.abstractmethod
    def decrypt(self, cipher_data):
        pass


class DefaultPasswordEncoder(PasswordEncoder):
    """Default without any crypto"""

    def encrypt(self, row_data):
        return row_data

    def decrypt(self, cipher_data):
        return cipher_data
