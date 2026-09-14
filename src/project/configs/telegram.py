from pydantic_settings import BaseSettings


class TelegramSettings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
