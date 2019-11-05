from flask import Flask, render_template, url_for, redirect, request
from flask import Blueprint
from .extensions import mongo
import json

from .cv import runCV

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    return render_template('index.html')

@main.route("/volunteer")
def volunteer():
    posts = []
    user_collection = mongo.db.users
    for doc in user_collection.find({}, { '_id': 0 }):
        posts.append(doc)
    # print(info)
    posts = json.dumps(posts)
    # posts = 'hi'
    # print(user_collection.find_one())
    # temp = json.dumps(user_collection.find_one())
    # print(posts)
    # print('te')
    return render_template('map.html', posts=posts)

@main.route("/helpMe")
def helpMe():
    return render_template('helpMe.html')

@main.route("/helpMe", methods=["POST"])
def updateRescueDB():
    lat = request.form['lat']
    lon = request.form['long']
    message = request.form['message']
    text = request.form['text']
    print(lat, lon, message, text)
    user_collection = mongo.db.users
    user_collection.insert({'lat' : lat, 'long' : lon, 'message' : message, 'text' : text})
    # return redirect('/volunteer')
    return redirect('/volunteer')

@main.route("/runCVwebcam")
def runWebcam():
    data = runCV(True)
    user_collection = mongo.db.users
    for x in data:
        user_collection.insert(x)
    return redirect('/volunteer')

@main.route("/runCVvid")
def runVid():
    data = runCV(False)
    user_collection = mongo.db.users
    for x in data:
        user_collection.insert(x)
    return redirect('/volunteer')