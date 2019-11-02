from flask import Flask, render_template, url_for, redirect, request

app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/map")
def map():
    return render_template('map.html')

@app.route("/volunteer")
def volunteer():
    return render_template('volunteer.html')


if __name__ == "__main__":
    app.run(debug=True)