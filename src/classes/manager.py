from src.base import LoguruLogger, Config
from src.classes.websites_access import KworbClass
from src.db import MongoDBClient


class Manager:
    def __init__(self):
        self.logger = LoguruLogger(__name__).get_logger()
        self.config = Config()
        self.mongo_client = MongoDBClient(
            connection_string=self.config.get_value('mongo_db', 'connection_url'),
            database_name=self.config.get_value('mongo_db', 'database'),
            collection_name=self.config.get_value('mongo_db', 'collection')
        )
        self.kworb = KworbClass()

    def fetch_song_and_insert_to_db(self):
        self.logger.info("Start Fetching songs and inserting them")
        for song_list in self.kworb.fetch_songs():
            self.mongo_client.insert_documents(documents=song_list, check_if_already_exist=True)
