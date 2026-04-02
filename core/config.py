from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from core.enum import ProjectStatus


class Settings(BaseSettings):

    bot_token: str = Field(validation_alias="BOT_TOKEN")

    admin_id: int = Field(validation_alias="ADMIN_ID")
    dev_id: int = Field(validation_alias="DEVELOPER_ID")
    admin_chat_id: int = Field(valid_signals="ADMIN_CHAT_ID")
    admin_chat_url: str = Field(validation_alias="ADMIN_CHAT_URL")

    log_file_name: str = Field(validation_alias="LOG_FILE_NAME")
    log_level: str = Field(validation_alias="LOG_LEVEL")

    db_name: str = Field(validation_alias="DB_NAME")
    project_status: ProjectStatus = Field(validation_alias="PROJECT_STATUS")
    check_subsribtion: bool = Field(validation_alias="CHECK_SUBSCRIPTION")


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