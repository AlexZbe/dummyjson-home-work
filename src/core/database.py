from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent / ".env"


class DBSettings(BaseSettings):
    DATABASE_URL: str

    @property
    def url(self) -> str:
        return f"sqlite+aiosqlite:///./{self.DATABASE_URL}"

    @property
    def url_sync_migration(self) -> str:
        return f"sqlite:///.{self.DATABASE_URL}"

    model_config = SettingsConfigDict(env_file=env_path)


db_settings = DBSettings()  # pyright: ignore[reportCallIssue]
