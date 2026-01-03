from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings."""

    model_config = SettingsConfigDict(env_prefix="secure_qrcode_")
    pbkdf2_iterations: int = Field(description="PBKDF2 iterations", default=1_200_000)


settings = Settings()
