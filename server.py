from flask import Flask, request, send_file, send_from_directory, render_template
from werkzeug.datastructures import FileStorage
import tempfile
import json
import os

from connection_manager import ConnectionManager
from mongo_db import Database


#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'edf'])

conn_manager = ConnectionManager()

app = Flask(__name__)
app.config['BASE_FOLDER'] = "."
app.config['UPLOAD_FOLDER'] = f"{app.config['BASE_FOLDER']}/UPLOAD_FOLDER"
app.config['CLIENT_JSON'] = f"{app.config['BASE_FOLDER']}/resources/json"
app.config['CLIENT_IMAGES'] = f"{app.config['BASE_FOLDER']}/resources/images"
app.config['CLIENT_AUDIO'] = f"{app.config['BASE_FOLDER']}/resources/audio"
app.config['UPLOAD_JSON'] = f"{app.config['UPLOAD_FOLDER']}/json"
app.config['UPLOAD_GENERAL'] = f"{app.config['UPLOAD_FOLDER']}/general"
app.config['UPLOAD_EDF'] = f"{app.config['UPLOAD_FOLDER']}/edf"

@app.route("/")
def home():
    return "Welcome to the server"

##### FILES UPLOAD/DOWNLOAD

@app.route("/files/general/images/<image_filename>", methods=['GET'])
def get_image(image_filename):
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], path=image_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/files/user-made/<filename>", methods=['GET'])
def get_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_GENERAL"], path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/files/general", methods=['POST'])
def upload_general_():
    file = request.files['file']
    FileStorage(file).save(os.path.join(app.config['UPLOAD_GENERAL'], file.filename))
    return 'OK', 200

@app.route("/additional-data/<dataType>/<deviceID>", methods=['GET'])
def pre_upload_edf(deviceID):
    temp_name = next(tempfile._get_candidate_names())
    dev_conn = conn_manager.find_connection_deviceID(deviceID)
    dev_conn.add_associatedData({dataType:temp_name})
    return temp_name

@app.route("/additional-data/<dataType>", methods=['POST'])
def upload_edf(deviceID):
    file = request.files['file']
    temp_name = file.filename
    filename = Database.update_filename(dataType, temp_name)
    FileStorage(file).save(os.path.join(app.config['UPLOAD_EDF'], filename))
    return 'OK', 200

##### DATABASE

@app.route("/db", methods=['GET','POST'])
def db_initialize():
    Database.initialize()
    return 'OK', 200

@app.route("/connection/<deviceID>", methods=['POST'])
def db_initialize_w_userID(deviceID):
    Database.initialize()
    conn_manager.add_device_connection(request.remote_addr, deviceID)
    return 'OK',200

@app.route("/connection",methods=['DELETE'])
def remove_device_connection():
    conn_manager.remove_device_connection(conn_manager.find_connection_ip(request.remote_addr).get_deviceID())
    return 'OK', 200

@app.route("/users", methods=['GET'])
def get_users():
    return Database.get_users()

@app.route("/users", methods=['POST'])
def insert_user():
    file = request.files["file"]
    json_dict = json.load(file.stream)
    Database.insert_user(json_dict)
    return 'OK', 200

@app.route("/users/<userID>", methods=['GET'])
def get_tests(userID):
    return Database.get_tests_info_from_userID(userID)

@app.route("/trials", methods=['GET'])
def get_trials():
    return Database.get_trials_info()

@app.route("/trials/<trialID>", methods=['GET'])
def get_trial_from_trialID(trialID):
    return Database.get_trial_from_trialID(trialID)

@app.route("/user-trials/<trialID>", methods=['GET'])
def get_user_trial(trialID):
    return Database.get_user_trial(trialID)

@app.route("/user-trials", methods=['POST'])
def upload_user_trial():
    file = request.files["file"]
    dev_conn = conn_manager.find_connection_ip(request.remote_addr)
    associatedData = dev_conn.get_associatedData()
    json_dict = json.load(file.stream)
    Database.insert_user_trial(json_dict, associatedData)
    dev_conn.remove_associated_data()
    return 'OK', 200

@app.route("/user-trials", methods=['PATCH'])
def update_user_trial():
    file = request.files['file']
    json_dict = json.load(file.stream)
    Database.update_user_trial(json_dict)
    return 'OK', 200

if __name__ == "__main__":
    app.run(host='0.0.0.0')
