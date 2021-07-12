
import pymongo
from bson.json_util import dumps
from bson.objectid import ObjectId

class Database:
    """docstring for MongoDB."""
    URI = "mongodb://127.0.0.1:27017"
    db = None
    isInitialized = False

    DB_NAME = "EEG_Environment"
    USERS_COL = "users"
    NEW_TRIALS_COL = "new_trials"
    USERS_TRIALS_COL = "user_trials"


    @staticmethod
    def initialize():
        if not Database.isInitialized:
            client = pymongo.MongoClient(Database.URI)
            Database.db = client[Database.DB_NAME]
        Database.isInitialized = True

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
        cursor = users.find({})
        json_data = dumps(list(cursor),indent=2)
        return json_data

    @staticmethod
    def get_trials_info():
        trials = Database.db[Database.NEW_TRIALS_COL]
        cursor = trials.find({}, {'tests':False})
        json_data = dumps(list(cursor),indent=2)
        return json_data

    @staticmethod
    def get_tests_info_from_userID(userID):
        tests = Database.db[Database.USERS_TRIALS_COL]
        cursor = tests.find({"info.userID":userID}, {'tests': False})
        json_data = dumps(list(cursor), indent=2)
        return json_data

    @staticmethod
    def get_trial_from_trialID(trialID):
        trials = Database.db[Database.NEW_TRIALS_COL]
        cursor = trials.find({"_id":ObjectId(trialID)},{'_id':False})
        json_data = dumps(list(cursor), indent=2)
        return json_data

    @staticmethod
    def get_user_trial(trialID):
        tests = Database.db[Database.USERS_TRIALS_COL]
        cursor = tests.find({"_id":ObjectId(trialID)},{'_id':False})
        json_data = dumps(list(cursor), indent=2)
        return json_data

    @staticmethod
    def insert_user_trial(data, additional_data=None):
        if additional_data:
            data['info'].update(additional_data)
        Database.insert(Database.USERS_TRIALS_COL, data)

    @staticmethod
    def insert_user(data):
        Database.insert(Database.USERS_COL, data)

    @staticmethod
    def update_user_trial(data):
        user_trials = Database.db[Database.USERS_TRIALS_COL]
        #tests.update({'info.userID':userID,'info.startTime':startTime}, data)
        user_trials.update({"_id":ObjecttId(data["_id"])}, {'$set':{'info':data['info'],'tests':data['tests']}})

    @staticmethod
    def update_filename(dataType, temp_filename):
        user_trials = Database.db[Database.USERS_TRIALS_COL]
        cursor = user_trials.find({f'info.additionalData.{dataType}':temp_filename},{'_id':False})
        info_dict = list(cursor)[0]['info']
        userID = info_dict['userID']
        startTime = info_dict['startTime']
        ## TODO: mantener extensión del archivo
        filename = f"{dataType}_{userID}_{startTime}.edf"
        user_trials.update({f'info.additionalData.{dataType}':temp_filename},{'$set':{f'info.additionalData.{dataType}':filename}})
        return filename
