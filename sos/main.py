from flask import Flask, render_template, url_for, redirect, request
from flask import Blueprint
from .extensions import mongo

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # user_collection = mongo.db.users
    # user_collection.insert({'name' : 'johnCena'})
    # return '<h1>Added a user!</h1>'
    return render_template('index.html')

@main.route("/map")
def map():
    return render_template('map.html')

@main.route("/volunteer")
def volunteer():
    return render_template('volunteer.html')

@main.route("/helpMe")
def helpMe():
    return render_template('helpMe.html')

@main.route("/helpMe", methods=["POST"])
def updateRescueDB():
    name = request.form['name']
    number = request.form['number']
    address = request.form['address']
    # user_collection = mongo.db.users
    # user_collection.insert({'name' : name, 'number' : number, 'address' ; address})
    return redirect('/map')