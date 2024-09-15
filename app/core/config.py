from typing import Optional
from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):

    app_title: str = 'QRKot'
    description: str = 'Сharitable service'
    secret: str = 'Secret123'
    first_superuser_email: Optional[EmailStr] = 'test@qrkot.com'
    first_superuser_password: Optional[str] = 'Test123'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'

    class Config:
        env_file = '.env'


settings = Settings()
