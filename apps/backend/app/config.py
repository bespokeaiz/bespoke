from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Пример: postgresql+psycopg2://user:pass@localhost:5432/artistdb
    DATABASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
