from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.enum import ProjectStatus


class Settings(BaseSettings):

    bot_token: str

    admin_id: int
    dev_id: int 
    admin_chat_id: int | None = None
    admin_chat_url: str | None = None

    log_file_name: str = "logs.log"
    log_level: str = "DEBUG"

    db_name: str = "db.sqlite3"
    project_status: ProjectStatus = ProjectStatus.common
    check_subscription: bool = Field(
        default=False,
        validation_alias="CHECK_SUBSCRIPTION"
    )


    @property
    def db_uri(self):
        return (
            f"sqlite+aiosqlite:///{self.db_name}"
        )


    model_config = SettingsConfigDict(
        env_file=Path(__file__).parents[1].joinpath(".env"),
        case_sensitive=False,
    )

settings = Settings()

def get_config():
    return Settings()