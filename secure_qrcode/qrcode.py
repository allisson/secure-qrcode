from io import BytesIO

import qrcode

from secure_qrcode.models import EncryptedData, ErrorCorrection


def make(
    encrypted_data: EncryptedData,
    error_correction: ErrorCorrection = ErrorCorrection.Level_M,
    box_size: int = 10,
    border: int = 4,
) -> BytesIO:
    """Generate a QR code image from encrypted data."""
    data = encrypted_data.model_dump_json()
    qr = qrcode.QRCode(
        version=None,
        error_correction=error_correction.value,
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    return img_io
