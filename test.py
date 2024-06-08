import os

from src.base import Config
from src.db.mongo_db import MongoDBClient


def main():
    config = Config()
    mongo_client = MongoDBClient(
        connection_string=os.getenv('MONGO_CONNECTION_STRING', config.get_value('mongo_db', 'connection_url')),
        database_name=os.getenv('MONGO_DATABASE_NAME', config.get_value('mongo_db', 'database')),
        collection_name=os.getenv('MONGO_COLLECTION_NAME', config.get_value('mongo_db', 'collection'))
    )
    mongo_client.delete_documents(query={'target_language': 'Hindi'})


if __name__ == '__main__':
    main()