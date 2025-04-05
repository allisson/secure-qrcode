from enum import IntEnum

from pydantic import BaseModel, Field


class EncryptedData(BaseModel):
    salt: str
    iterations: int
    associated_data: str
    nonce: str
    ciphertext: str


class ErrorCorrection(IntEnum):
    Level_L = 1
    Level_M = 0
    Level_Q = 3
    Level_H = 2


class EncodeRequest(BaseModel):
    plaintext: str = Field(min_length=1, max_length=2048, description="Text to be encrypted")
    key: str = Field(min_length=1, max_length=32, description="Key used to encrypt the data")
    error_correction: ErrorCorrection = Field(
        default=ErrorCorrection.Level_M,
        description="Error correction level, possible values: 1 (About 7% or less errors can be corrected), 0 (About 15% or less errors can be corrected), 3 (About 25% or less errors can be corrected), 2 (About 30% or less errors can be corrected)",
    )
    box_size: int = Field(default=10, description="How many pixels each 'box' of the QR code is")
    border: int = Field(default=4, description="How many boxes thick the border should be")


class EncodeResponse(BaseModel):
    content: str = Field(description="Image content encoded in base64")
    media_type: str = Field(description="The media type of the image")


class DecodeRequest(BaseModel):
    encrypted_data: EncryptedData = Field(description="The encrypted data read from the image")
    key: str = Field(min_length=1, max_length=32, description="Key used to encrypt the data")


class DecodeResponse(BaseModel):
    decrypted_data: str = Field(description="The result decrypted data")


class DecryptErrorResponse(BaseModel):
    message: str


class HealthResponse(BaseModel):
    success: bool
