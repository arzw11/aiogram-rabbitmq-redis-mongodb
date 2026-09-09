from pydantic_settings import SettingsConfigDict

from src.project.configs.general import GeneralSettings
from src.project.configs.logger import LoggerSettings
from src.project.configs.mongodb import MongoDBSettings


class Settings(
    LoggerSettings,
    GeneralSettings,
    MongoDBSettings,
):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
    )


settings = Settings()
