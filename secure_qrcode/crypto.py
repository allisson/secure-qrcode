from base64 import b64decode, b64encode

from Crypto.Cipher import ChaCha20_Poly1305
from Crypto.Random import get_random_bytes

from secure_qrcode.exceptions import DecryptError
from secure_qrcode.models import EncryptedData


def encrypt(plaintext: str, key: str) -> EncryptedData:
    header = get_random_bytes(16)
    cipher = ChaCha20_Poly1305.new(key=key.encode(encoding="utf-8").ljust(32))
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode(encoding="utf-8"))
    jk = ["nonce", "header", "ciphertext", "tag"]
    jv = [b64encode(x).decode("utf-8") for x in (cipher.nonce, header, ciphertext, tag)]
    result = dict(zip(jk, jv))
    return EncryptedData(**result)


def decrypt(encrypted_data: EncryptedData, key: str) -> str:
    try:
        b64 = encrypted_data.model_dump()
        jk = ["nonce", "header", "ciphertext", "tag"]
        jv = {k: b64decode(b64[k]) for k in jk}
        cipher = ChaCha20_Poly1305.new(key=key.encode(encoding="utf-8").ljust(32), nonce=jv["nonce"])
        cipher.update(jv["header"])
        plaintext = cipher.decrypt_and_verify(jv["ciphertext"], jv["tag"])
    except (ValueError, KeyError) as exc:
        raise DecryptError(f"Incorrect decryption, exc={exc}")

    return plaintext.decode("utf-8")
