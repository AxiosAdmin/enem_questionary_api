import hashlib
import re


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_nickname(value: str) -> str:
    return value.strip().lower()


def normalize_cpf(value: str) -> str:
    return re.sub(r"\D", "", value)


def hash_lookup_value(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()
