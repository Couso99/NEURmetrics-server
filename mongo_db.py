
import pymongo

class Database:
    """docstring for MongoDB."""
    URI = "mongodb://127.0.0.1:27017"
    db = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.db = client["EEG_Environment"]


    @staticmethod
    def insert(collection,data):
        Database.db[collection].insert(data)

    @staticmethod
    def find(collection,query):
        return Database.db[collection].find(query)

    @staticmethod
    def find(collection,query):
        return Database.db[collection].find_one(query)
