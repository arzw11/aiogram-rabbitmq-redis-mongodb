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
        logging.getLogger('pymongo').setLevel(logging.WARNING)
        logging.getLogger('motor').setLevel(logging.WARNING)
        logging.getLogger('aio_pika').setLevel(logging.WARNING)
        logging.getLogger('aiormq').setLevel(logging.WARNING)

        if self.ENVIRONMENT == Environment.LOCAL:
            self.config_local_logger()
        else:
            self.config_server_logger()
