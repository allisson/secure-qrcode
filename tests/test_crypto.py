from base64 import b64encode

import pytest

from secure_qrcode.crypto import decrypt, encrypt
from secure_qrcode.exceptions import DecryptError
from secure_qrcode.models import EncryptedData


def test_encrypt_decrypt(plaintext, key):
    encrypted_data = encrypt(plaintext, key)

    assert encrypted_data.salt
    assert encrypted_data.iterations
    assert encrypted_data.associated_data
    assert encrypted_data.nonce
    assert encrypted_data.ciphertext
    assert decrypt(encrypted_data, key) == plaintext


def test_decrypt_error(key):
    encrypted_data = EncryptedData(
        salt="KtiCW1E0VLupOXOtpDIlZQ==",
        iterations=1200000,
        associated_data="JFPRP6/RMmCIn3DLjA/ceg==",
        nonce="LbF9P5FwPYyGCTJM",
        ciphertext="/N8WF0+QnqsDhOQ9iWuhWrXgbrZlG4Hqm9cYt/QO9Msu",
    )
    encrypted_data.associated_data = b64encode(b"invalid-aad").decode("utf-8")

    with pytest.raises(DecryptError) as excinfo:
        decrypt(encrypted_data, key)

    assert str(excinfo.value) == "Incorrect decryption, exc=Invalid Tag"
