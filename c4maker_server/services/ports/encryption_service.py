import abc


class EncryptionService(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def encrypt_password(self, password: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def check_encrypted_password(self, password: str, encrypted_password: str) -> bool:
        raise NotImplementedError
