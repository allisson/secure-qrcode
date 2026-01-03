from base64 import b64encode

import pytest

from secure_qrcode.crypto import decrypt, encrypt
from secure_qrcode.exceptions import DecryptError


def test_encrypt_decrypt(plaintext, key):
    """Test that encryption and decryption work correctly."""
    encrypted_data = encrypt(plaintext, key)

    assert encrypted_data.salt
    assert encrypted_data.iterations
    assert encrypted_data.associated_data
    assert encrypted_data.nonce
    assert encrypted_data.ciphertext
    assert decrypt(encrypted_data, key) == plaintext


def test_decrypt_error(key, sample_encrypted_data):
    """Test that decryption fails with invalid data."""
    encrypted_data = sample_encrypted_data.model_copy(
        update={"associated_data": b64encode(b"invalid-aad").decode()}
    )

    with pytest.raises(DecryptError) as excinfo:
        decrypt(encrypted_data, key)

    assert str(excinfo.value) == "Incorrect decryption, invalid key or corrupted data"
