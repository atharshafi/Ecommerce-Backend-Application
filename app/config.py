from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database configuration
    DATABASE_URL: str

    # JWT configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24  # You need this too!

    # First admin user
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = 'utf-8'


settings = Settings()
