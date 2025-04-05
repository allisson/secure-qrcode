import os
from base64 import b64decode, b64encode

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from secure_qrcode.config import settings
from secure_qrcode.exceptions import DecryptError
from secure_qrcode.models import EncryptedData


def derive_key(key: str, salt: bytes, iterations: int) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
    )
    return kdf.derive(key.encode(encoding="utf-8"))


def encrypt(plaintext: str, key: str) -> EncryptedData:
    salt = os.urandom(16)
    iterations = settings.pbkdf2_iterations
    associated_data = os.urandom(16)
    nonce = os.urandom(12)
    derived_key = derive_key(key, salt, iterations)
    chacha = ChaCha20Poly1305(derived_key)
    ciphertext = chacha.encrypt(nonce, plaintext.encode(encoding="utf-8"), associated_data)
    return EncryptedData(
        salt=b64encode(salt).decode("utf-8"),
        iterations=iterations,
        associated_data=b64encode(associated_data).decode("utf-8"),
        nonce=b64encode(nonce).decode("utf-8"),
        ciphertext=b64encode(ciphertext).decode("utf-8"),
    )


def decrypt(encrypted_data: EncryptedData, key: str) -> str:
    salt = b64decode(encrypted_data.salt)

    associated_data = b64decode(encrypted_data.associated_data)
    nonce = b64decode(encrypted_data.nonce)
    ciphertext = b64decode(encrypted_data.ciphertext)
    derived_key = derive_key(key, salt, encrypted_data.iterations)
    chacha = ChaCha20Poly1305(derived_key)

    try:
        plaintext = chacha.decrypt(nonce, ciphertext, associated_data)
    except InvalidTag:
        raise DecryptError("Incorrect decryption, exc=Invalid Tag")
    except Exception as exc:
        raise DecryptError(f"Incorrect decryption, exc={exc}")

    return plaintext.decode("utf-8")
