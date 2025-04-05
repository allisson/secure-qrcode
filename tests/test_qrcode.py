from secure_qrcode.models import EncryptedData
from secure_qrcode.qrcode import make


def test_make():
    encrypted_data = EncryptedData(
        salt="KtiCW1E0VLupOXOtpDIlZQ==",
        iterations=1200000,
        associated_data="JFPRP6/RMmCIn3DLjA/ceg==",
        nonce="LbF9P5FwPYyGCTJM",
        ciphertext="/N8WF0+QnqsDhOQ9iWuhWrXgbrZlG4Hqm9cYt/QO9Msu",
    )

    img_io = make(encrypted_data)
    assert img_io.getbuffer().nbytes == 2046
