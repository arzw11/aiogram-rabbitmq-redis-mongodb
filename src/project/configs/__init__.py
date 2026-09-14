from pydantic_settings import SettingsConfigDict

from src.project.configs.general import GeneralSettings
from src.project.configs.logger import LoggerSettings
from src.project.configs.mongodb import MongoDBSettings
from src.project.configs.rabbitmq import RabbitMQSettings
from src.project.configs.telegram import TelegramSettings


class Settings(
    LoggerSettings,
    GeneralSettings,
    MongoDBSettings,
    RabbitMQSettings,
    TelegramSettings,
):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file='.env',
    )


settings = Settings()
