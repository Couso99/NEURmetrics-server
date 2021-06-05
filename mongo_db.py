
import pymongo
from bson.json_util import dumps

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
        Database.db[collection].insert_one(data)

    @staticmethod
    def find(collection,query):
        return Database.db[collection].find(query)

    @staticmethod
    def find_one(collection,query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def get_users():
        users = Database.db["users"]
        cursor = users.find({}, {'_id': False})
        json_data = dumps(list(cursor),indent=2)
        return json_data

    @staticmethod
    def get_trials_info():
        trials = Database.db["trials"]
        cursor = trials.find({}, {'_id': False,'info': True})
        json_data = dumps(list(cursor),indent=2)
        return json_data

    @staticmethod
    def get_tests_info_from_userID(userID):
        tests = Database.db["tests"]
        cursor = tests.find({"info.userID":int(userID)}, {'_id': False,'info': True})
        json_data = dumps(list(cursor), indent=2)
        return json_data
