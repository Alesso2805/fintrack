from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FinTrack API"
    app_env: str = "local"
    api_v1_prefix: str = "/api/v1"
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    jwt_algorithm: str = "HS256"
    initial_admin_email: str = "admin@fintrack.dev"
    initial_admin_password: str
    initial_admin_full_name: str = "FinTrack Admin"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @field_validator("database_url", "secret_key", "initial_admin_password")
    @classmethod
    def reject_placeholders(cls, value: str) -> str:
        if "<" in value or ">" in value or "replace-with" in value:
            raise ValueError("Replace placeholder values with real environment-specific secrets")
        return value

    @field_validator("secret_key")
    @classmethod
    def validate_secret_key(cls, value: str) -> str:
        if len(value) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return value

    @field_validator("initial_admin_password")
    @classmethod
    def validate_initial_admin_password(cls, value: str) -> str:
        if len(value) < 12:
            raise ValueError("INITIAL_ADMIN_PASSWORD must be at least 12 characters long")
        return value


settings = Settings()
