from src.db import MongoDBClient


def main():
    mongo = MongoDBClient(
        connection_string="mongodb+srv://larityai1:YmphRV89c6CxDjkj@cluster0.txarrod.mongodb.net/?retryWrites=true&w=majority",
        database_name="song_lyrics",
        collection_name="song_test",
    )
    document = {
        "song_name": "IDAN 123",
        "artist_names": "idan itagg"
    }
    mongo.is_document_already_exists(document=document)


if __name__ == '__main__':
    main()
