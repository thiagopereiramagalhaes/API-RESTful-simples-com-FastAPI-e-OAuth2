import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "sua_chave_secreta_super_segura_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PASSWORD_ADMIN: str = "admin123"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
