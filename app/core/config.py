from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    app_title: str = 'Бронирование переговорок'
    description: str = 'Организуйте работу!'

    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    token_lifetime: int = 3600
    password_min_length: int = 3

    first_superuser_email: Optional[str] = None
    first_superuser_password: Optional[str] = None


settings = Settings()
