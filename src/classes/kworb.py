from src.base import LoguruLogger


class KworbClass:
    def __init__(self):
        self.logger = LoguruLogger(__name__).get_logger()


    def