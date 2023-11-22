from secure_qrcode.models import EncryptedData
from secure_qrcode.qrcode import make


def test_make():
    encrypted_data = EncryptedData(
        nonce="c2nduzQLo4sWOe3n",
        header="oheZpcpquDA7CoUuAi8Mng==",
        ciphertext="7WXqkkf4CWlH5A2vmXDbyMc=",
        tag="l027RcLlp2acAUxIxfYiAg==",
    )

    img_io = make(encrypted_data)
    assert img_io.getbuffer().nbytes == 1435
