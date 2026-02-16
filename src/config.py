import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # API Configurations
    RANDOM_USER_API_URL: str = "https://randomuser.me/api/"
    
    # LLM Configurations
    OPENAI_API_KEY: Optional[str] = None
    HF_API_KEY: Optional[str] = None
    MODEL_NAME: str = "gpt-4o-mini"
    
    # Application settings
    LOG_LEVEL: str = "INFO"
    SSL_VERIFY: bool = True
    CACHE_EXPIRATION: int = 300
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
