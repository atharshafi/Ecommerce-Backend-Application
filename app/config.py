from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration class to load settings from environment variables.
    Uses Pydantic's BaseSettings to automatically read from the `.env` file.
    """

    # Database configuration
    DATABASE_URL: str  # Database connection URL

    # JWT configuration
    SECRET_KEY: str  # Secret key for signing JWT tokens
    ALGORITHM: str = "HS256"  # JWT signing algorithm, default is HS256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  # Token expiration time in minutes
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 24  # Password reset token expiration time in hours

    # First admin user credentials
    FIRST_SUPERUSER: str  # Admin username for the first user
    FIRST_SUPERUSER_PASSWORD: str  # Admin password for the first user

    class Config:
        # Configuration settings for Pydantic
        env_file = ".env"  # Path to the environment file
        case_sensitive = True  # Make environment variables case-sensitive
        env_file_encoding = 'utf-8'  # Encoding for the environment file


# Instantiate settings from environment variables
settings = Settings()
