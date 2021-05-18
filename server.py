from flask import Flask, request, send_file, send_from_directory, render_template
from werkzeug.datastructures import FileStorage
import os

from mongodb_db import Database


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
        return send_from_directory(app.config["CLIENT_JSON"], filename=json_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-file/general/image/<image_filename>", methods=['GET','POST'])
def get_image(image_filename):
    #print(os.path.join(app.config["CLIENT_IMAGES"], image_filename))
    try:
        return send_from_directory(app.config["CLIENT_IMAGES"], filename=image_filename, as_attachment=True)
    except FileNotFoundError:
        abort(404)

@app.route("/get-file/user-made/<filename>", methods=['GET','POST'])
def get_file(filename):
    try:
        return send_from_directory(app.config["UPLOAD_GENERAL"], filename=filename, as_attachment=True)
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


@app.route("/insert_sth", methods=['GET','POST'])
def db_insert_something():
    mydict = { "name": "prueba a ver si esto tira", "objetivo": "Que pinche funcione" }
    Database.insert("prueba", mydict)
    return 'OK', 200

@app.route("/insert_trial", methods=['GET','POST'])
def db_insert_trial():
    with open(f"{app.config["CLIENT_JSON"]}/moca_trial.json") as f:
        mydict = eval(f.read())
    print(mydict)
    Database.insert("trials", mydict)


app.run(host='0.0.0.0')
