import asyncio

from src.bot.bot import start_polling
from src.project.configs import settings

if __name__ == '__main__':
    settings.config_logger()
    asyncio.run(start_polling())
