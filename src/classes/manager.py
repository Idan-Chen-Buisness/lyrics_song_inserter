import os

from src.base import LoguruLogger, Config
from src.classes.lyrics_class import Lyrics
from src.classes.websites_access import KworbClass
from src.db import MongoDBClient


class Manager:
    def __init__(self):
        self.logger = LoguruLogger(__name__).get_logger()
        self.config = Config()
        self.mongo_client = MongoDBClient(
            connection_string=os.getenv('MONGO_CONNECTION_STRING', self.config.get_value('mongo_db', 'connection_url')),
            database_name=os.getenv('MONGO_DATABASE_NAME', self.config.get_value('mongo_db', 'database')),
            collection_name=os.getenv('MONGO_COLLECTION_NAME', self.config.get_value('mongo_db', 'collection'))
        )
        self.kworb = KworbClass()
        self.lyrics_class = Lyrics()

    def fetch_song_and_insert_to_db(self):
        self.logger.info("Start Fetching songs and inserting them")
        for song_list in self.kworb.fetch_songs():
            for song in song_list:
                if not self.lyrics_class.is_lyrics_language_the_same_as_the_target(song_name=song['song_name'],
                                                                                   artist=song['artist_names'],
                                                                                   target_language=song[
                                                                                       'target_language']):
                    self.mongo_client.insert_document(document=song, check_if_already_exist=True)
