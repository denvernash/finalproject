
from flask import Flask, render_template
import requests
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("index.html")

@app.route("/dogs", methods=['GET', 'POST'])
def dogs():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        dogs_list = model.get_dogs_listing(sortby, sortorder)
    else:
        dogs_list = model.get_dogs_listing()
    return render_template("dogs.html", dogs_list= dogs_list)



if __name__=="__main__":
    model.init_dogs()
    app.run(debug=True)
