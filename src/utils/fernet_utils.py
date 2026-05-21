from cryptography.fernet import Fernet

from src.configs.configs import settings


class FernetUtils:
    _fernet = Fernet(settings.FERNET_KEY.encode())

    @classmethod
    def encrypt(cls, value: str) -> str:
        return cls._fernet.encrypt(value.encode()).decode()

    @classmethod
    def decrypt(cls, value: str) -> str:
        return cls._fernet.decrypt(value.encode()).decode()
