from flask import Flask, request, send_file, send_from_directory, render_template
from werkzeug.datastructures import FileStorage
import json
import os

from mongo_db import Database


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'edf'])

app = Flask(__name__)
app.config['BASE_FOLDER'] = "."
app.config['UPLOAD_FOLDER'] = f"{app.config['BASE_FOLDER']}/UPLOAD_FOLDER"
app.config['CLIENT_JSON'] = f"{app.config['BASE_FOLDER']}/resources/json"
app.config['CLIENT_IMAGES'] = f"{app.config['BASE_FOLDER']}/resources/images"
app.config['CLIENT_AUDIO'] = f"{app.config['BASE_FOLDER']}/resources/audio"
app.config['UPLOAD_JSON'] = f"{app.config['UPLOAD_FOLDER']}/json"
app.config['UPLOAD_GENERAL'] = f"{app.config['UPLOAD_FOLDER']}/general"

@app.route("/")
def home():
    return "Welcome to the server"

##### FILES UPLOAD/DOWNLOAD

@app.route("/get-file/general/json/<json_filename>", methods=['GET','POST'])
def get_json(json_filename):
    #print(os.path.join(app.config['CLIENT_JSON'], json_filename))
    try:
        return send_from_directory(app.config["CLIENT_JSON"], path=json_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-file/general/image/<image_filename>", methods=['GET','POST'])
def get_image(image_filename):
    #print(os.path.join(app.config["CLIENT_IMAGES"], image_filename))
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], path=image_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-file/user-made/<filename>", methods=['GET','POST'])
def get_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_GENERAL"], path=filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/upload/json", methods=['POST'])
def upload_json():
    file = request.files['file']
    FileStorage(file).save(os.path.join(app.config['UPLOAD_JSON'], file.filename))
    return 'OK', 200

@app.route("/upload/general", methods=['POST'])
def upload_general_():
    file = request.files['file']
    FileStorage(file).save(os.path.join(app.config['UPLOAD_GENERAL'], file.filename))
    return 'OK', 200

@app.route("/upload-audio", methods=['POST'])
def upload_audio():
    file = request.files['file']
    filename = file.filename
    file.save(os.path.join(app.config['CLIENT_AUDIO'], filename))

@app.route("/upload", methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    FileStorage(request.stream).save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return 'OK', 200

@app.route("/upload-general", methods=['POST'])
def upload_general():
    #print(dir(request.files))
    #print(request.files['picture'].filename)
    #print(request.files)

    # Vale para leer la description que se manda desde Retrofit2
    #print(request.form)

    file = request.files['file']
    FileStorage(file).save(os.path.join(app.config['UPLOAD_GENERAL'], file.filename))
    return 'OK', 200

@app.route("/upload-json", methods=['POST'])
def upload_json_():
    file = request.files['file']
    FileStorage(file).save(os.path.join(app.config['UPLOAD_JSON'], file.filename))
    return 'OK', 200

##### DATABASE

@app.route("/initialize", methods=['GET','POST'])
def db_initialize():
    Database.initialize()
    return 'OK', 200


'''@app.route("/insert_sth", methods=['GET','POST'])
def db_insert_something():
    mydict = { "name": "prueba a ver si esto tira", "objetivo": "Que pinche funcione" }
    Database.insert("prueba", mydict)
    return 'OK', 200

@app.route("/insert-trial", methods=['GET','POST'])
def db_insert_trial():
    with open(f"{app.config['CLIENT_JSON']}/moca_trial.json", 'r') as f:
        print(f.read())
        f.seek(0)
        mydict = json.load(f)
    print(mydict)
    print(type(mydict))
    final_dict = {"moca_trial": mydict}

    Database.insert("trials", mydict)
    return 'OK', 200'''

@app.route("/get-users", methods=['GET','POST'])
def get_users():
    return Database.get_users()

@app.route("/get-trials", methods=['GET','POST'])
def get_trials():
    return Database.get_trials_info()

@app.route("/get-user-trials/<userID>", methods=['GET','POST'])
def get_tests(userID):
    return Database.get_tests_info_from_userID(userID)

@app.route("/get-trial/<trialID>", methods=['GET','POST'])
def get_trial_from_trialID(trialID):
    return Database.get_trial_from_trialID(trialID)

@app.route("/get-user-trial/<userID>/<start_time>", methods=['GET','POST'])
def get_user_trial(userID, start_time):
    return Database.get_user_trial(userID, start_time)

@app.route("/upload-user-trial", methods=['POST'])
def upload_user_trial():
    file = request.files["file"]
    #print(dir(file))
    #print(file)
    #print(file.stream.read())
    json_dict = json.load(file.stream)
    Database.insert_user_trial(json_dict)

    return 'OK', 200

@app.route("/update-user-trial", methods=['POST'])
def update_user_trial():
    file = request.files['file']
    json_dict = json.load(file.stream)
    Database.update_user_trial(json_dict)

    return 'OK', 200

app.run(host='0.0.0.0')
