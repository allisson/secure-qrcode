from base64 import b64encode

import pytest

from secure_qrcode.crypto import decrypt, encrypt
from secure_qrcode.exceptions import DecryptError
from secure_qrcode.models import EncryptedData


def test_encrypt_decrypt(plaintext, key):
    encrypted_data = encrypt(plaintext, key)

    assert encrypted_data.nonce
    assert encrypted_data.header
    assert encrypted_data.ciphertext
    assert encrypted_data.tag
    assert decrypt(encrypted_data, key) == plaintext


def test_decrypt_error(key):
    encrypted_data = EncryptedData(
        nonce="c2nduzQLo4sWOe3n",
        header="oheZpcpquDA7CoUuAi8Mng==",
        ciphertext="7WXqkkf4CWlH5A2vmXDbyMc=",
        tag="l027RcLlp2acAUxIxfYiAg==",
    )
    encrypted_data.header = b64encode(b"invalid-header").decode("utf-8")

    with pytest.raises(DecryptError) as excinfo:
        decrypt(encrypted_data, key)

    assert str(excinfo.value) == "Incorrect decryption, exc=MAC check failed"
