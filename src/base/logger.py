import sys
from loguru import logger
from src.base.config import Config


class LoguruLogger:
    def __init__(self, name):
        self.logger_config = Config().get_value('logger')
        self.log_level = self.logger_config['level']

        self.name = name

        # remove default handler
        logger.remove()

        # configure console handler
        logger.add(
            sys.stderr,
            level=self.log_level
        )

    def get_logger(self):
        return logger.bind(name=self.name)
