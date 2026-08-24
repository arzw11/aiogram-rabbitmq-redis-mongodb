from pydantic_settings import SettingsConfigDict

from src.project.configs.general import GeneralSettings
from src.project.configs.logger import LoggerSettings


class Settings(
    LoggerSettings,
    GeneralSettings,
):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file='.env',
    )


settings = Settings()
