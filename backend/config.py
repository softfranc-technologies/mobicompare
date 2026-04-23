"""
config.py — App settings loaded from environment variables / .env file
"""
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # MongoDB
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB:  str = "mobicompare"

    # JWT
    SECRET_KEY:                  str = "change-this-in-production-use-openssl-rand-hex-32"
    ALGORITHM:                   str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24   # 24 hours

    # App
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
