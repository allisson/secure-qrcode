from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="secure_qrcode_")
    left_padding_char: str = Field(description="Left padding char", min_length=1, max_length=1, default=" ")


settings = Settings()
