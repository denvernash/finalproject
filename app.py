
from flask import Flask, render_template
import requests
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("index.html")

@app.route("/dogs")
def map():
    return render_template("index.html")



if __name__=="__main__":
    model.init()
    app.run(debug=True)
