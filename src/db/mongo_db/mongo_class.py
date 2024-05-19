import re

from pymongo import MongoClient, errors
from src.base import LoguruLogger


class MongoDBClient:
    def __init__(self, connection_string, database_name, collection_name):
        self.connection_string = connection_string
        self.database_name = database_name
        self.collection_name = collection_name
        self.logger = LoguruLogger(__name__).get_logger()
        self.client = None
        self.db = None
        self.collection = None
        self.connect()

    def connect(self):
        """
        Tries to connect to the MongoDB server with the provided connection string
        and sets up the database and collection.
        :return: True if connection is successful, False otherwise
        """
        try:
            self.client = MongoClient(self.connection_string)
            # Attempt to fetch server information to confirm connection
            self.client.server_info()
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            self.logger.debug("Connection to MongoDB successful")
            return True
        except errors.ServerSelectionTimeoutError as err:
            self.logger.debug(f"Connection failed: {err}")
            return False

    def insert_documents(self, documents, check_if_already_exist=True):
        """
        Inserts a list of documents into the collection one by one.
        :param check_if_already_exist: check if already exist
        :param documents: List of documents to be inserted
        :return: Inserted IDs of the documents
        """
        documents_dont_exist = []
        if check_if_already_exist:
            self.logger.info("Check if the documents already exists")
            for index, document in enumerate(documents):
                if not self.is_document_already_exists(document=document):
                    self.logger.debug(f"{index} - Document {document['song_name']} DOESN'T EXIST")
                    documents_dont_exist.append(document)
                else:
                    self.logger.debug(f"{index} - Document {document['song_name']} EXIST")

        else:
            documents_dont_exist = documents

        counter = 0
        self.logger.info("Start insert documents to db")
        for document in documents_dont_exist:
            result = self.collection.insert_one(document)
            counter += 1

        self.logger.debug(
            f"Inserted {counter} documents into {self.database_name}.{self.collection_name}")

    def is_document_already_exists(self, document):
        song_regex = re.compile(re.escape(document['song_name']), re.IGNORECASE)
        artist_regex = re.compile(re.escape(document['artist_names']), re.IGNORECASE)
        query = {
            "song_name": {"$regex": song_regex},
            "artist_names": {"$regex": artist_regex}
        }
        found_documents = self.find_documents(query)
        if len(found_documents):
            return True
        return False

    def find_documents(self, query):
        """
        Finds documents in the collection based on the given query.

        :param query: Dictionary query to search documents
        :return: List of found documents
        """
        results = self.collection.find(query)
        found_documents = list(results)
        return found_documents

    def update_document(self, query, new_values):
        """
        Updates a document in the collection based on the given query.

        :param query: Dictionary query to find the document to be updated
        :param new_values: Dictionary with the new values
        :return: Modified count
        """
        result = self.collection.update_one(query, {'$set': new_values})
        self.logger.debug(
            f"Updated document in {self.database_name}.{self.collection_name} with query {query} and new values {new_values}")
        return result.modified_count

    def delete_documents(self, query):
        """
        Deletes documents in the collection based on the given query.

        :param query: Dictionary query to delete documents
        :return: Deleted count
        """
        result = self.collection.delete_many(query)
        self.logger.debug(
            f"Deleted {result.deleted_count} documents from {self.database_name}.{self.collection_name} with query {query}")
        return result.deleted_count

    def list_collections(self):
        """
        Lists all collections in the database.

        :return: List of collection names
        """
        collections = self.db.list_collection_names()
        self.logger.debug(f"Listed collections in {self.database_name}: {collections}")
        return collections

    def list_databases(self):
        """
        Lists all databases in the MongoDB server.

        :return: List of database names
        """
        databases = self.client.list_database_names()
        self.logger.debug(f"Listed databases: {databases}")
        return databases
