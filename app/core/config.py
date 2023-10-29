from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = '.env'

    app_title: str = 'Бронирование переговорок'
    description: str = 'Организуйте работу!'
    database_url: str
    secret: str = 'SECRET'
    first_superuser_email: Optional[str] = None
    first_superuser_password: Optional[str] = None


settings = Settings()
