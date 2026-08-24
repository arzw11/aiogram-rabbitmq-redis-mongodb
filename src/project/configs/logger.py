import logging

from src.project.configs.general import (
    Environment,
    GeneralSettings,
)


class LoggerSettings(GeneralSettings):
    def config_server_logger(self):
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        logger.addHandler(handler)

    def config_local_logger(self):
        logging.basicConfig(level=logging.DEBUG)

    def config_logger(self):
        if self.ENVIRONMENT == Environment.LOCAL:
            self.config_local_logger()
        else:
            self.config_server_logger()
