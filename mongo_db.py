
import pymongo
from bson.json_util import dumps

class Database:
    """docstring for MongoDB."""
    URI = "mongodb://127.0.0.1:27017"
    db = None

    DB_NAME = "EEG_Environment"
    USERS_COL = "users"
    NEW_TRIALS_COL = "new_trials"
    USERS_TRIALS_COL = "user_trials"


    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.db = client[Database.DB_NAME]

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
        users = Database.db[Database.USERS_COL]
        cursor = users.find({}, {'_id': False})
        json_data = dumps(list(cursor),indent=2)
        return json_data

    @staticmethod
    def get_trials_info():
        trials = Database.db[Database.NEW_TRIALS_COL]
        cursor = trials.find({}, {'_id': False,'info': True})
        json_data = dumps(list(cursor),indent=2)
        return json_data

    @staticmethod
    def get_tests_info_from_userID(userID):
        tests = Database.db[Database.USERS_TRIALS_COL]
        cursor = tests.find({"info.userID":userID}, {'_id': False,'info': True})
        json_data = dumps(list(cursor), indent=2)
        return json_data

    @staticmethod
    def get_trial_from_trialID(trialID):
        trials = Database.db[Database.NEW_TRIALS_COL]
        cursor = trials.find({"info.trialID":trialID}, {'_id': False})
        json_data = dumps(list(cursor), indent=2)
        return json_data

    @staticmethod
    def get_user_trial(userID, start_time):
        tests = Database.db[Database.USERS_TRIALS_COL]
        cursor = tests.find({'info.userID':userID,'info.startTime':int(start_time)},{'_id': False})
        json_data = dumps(list(cursor), indent=2)
        return json_data

    @staticmethod
    def insert_user_trial(data):
        Database.insert(Database.USERS_TRIALS_COL, data)

    @staticmethod
    def update_user_trial(data):
        userID = data['info']['userID']
        startTime = data['info']['startTime']
        tests = Database.db[Database.USERS_TRIALS_COL]
        tests.update({'info.userID':userID,'info.startTime':startTime}, data)
