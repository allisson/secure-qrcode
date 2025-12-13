import time

from secure_qrcode.crypto import decrypt, encrypt
from secure_qrcode.models import EncryptedData
from secure_qrcode.qrcode import make


def test_encrypt_performance(plaintext, key, benchmark=None):
    """Test encryption performance - should complete in reasonable time."""
    start = time.perf_counter()
    encrypted_data = encrypt(plaintext, key)
    elapsed = time.perf_counter() - start

    # Encryption with PBKDF2 should complete within reasonable time
    # With 1,200,000 iterations, this should take less than 2 seconds
    assert elapsed < 2.0, f"Encryption took {elapsed:.3f}s, expected < 2.0s"
    assert encrypted_data.salt
    assert encrypted_data.ciphertext


def test_decrypt_performance(key):
    """Test decryption performance - should complete in reasonable time."""
    encrypted_data = EncryptedData(
        salt="KtiCW1E0VLupOXOtpDIlZQ==",
        iterations=1200000,
        associated_data="JFPRP6/RMmCIn3DLjA/ceg==",
        nonce="LbF9P5FwPYyGCTJM",
        ciphertext="/N8WF0+QnqsDhOQ9iWuhWrXgbrZlG4Hqm9cYt/QO9Msu",
    )

    start = time.perf_counter()
    decrypted_data = decrypt(encrypted_data, key)
    elapsed = time.perf_counter() - start

    # Decryption with PBKDF2 should complete within reasonable time
    # With 1,200,000 iterations, this should take less than 2 seconds
    assert elapsed < 2.0, f"Decryption took {elapsed:.3f}s, expected < 2.0s"
    assert decrypted_data == "super secret text"


def test_qrcode_generation_performance(plaintext, key):
    """Test QR code generation performance."""
    encrypted_data = encrypt(plaintext, key)

    start = time.perf_counter()
    img_io = make(encrypted_data)
    elapsed = time.perf_counter() - start

    # QR code generation should be fast
    assert elapsed < 0.5, f"QR code generation took {elapsed:.3f}s, expected < 0.5s"
    assert img_io.getbuffer().nbytes > 0


def test_full_encode_decode_cycle_performance(plaintext, key):
    """Test full encode/decode cycle performance."""
    start = time.perf_counter()

    # Encrypt
    encrypted_data = encrypt(plaintext, key)

    # Generate QR code
    img_io = make(encrypted_data)

    # Decrypt
    decrypted_data = decrypt(encrypted_data, key)

    elapsed = time.perf_counter() - start

    # Full cycle should complete in reasonable time
    assert elapsed < 4.0, f"Full cycle took {elapsed:.3f}s, expected < 4.0s"
    assert decrypted_data == plaintext
    assert img_io.getbuffer().nbytes > 0
