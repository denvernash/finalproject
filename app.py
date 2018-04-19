
from flask import Flask, render_template, request
import model
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/map")
def map():
    return render_template("map.html")

@app.route("/breeds", methods=['GET', 'POST'])
def dogs():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        dogs_list = model.get_breeds_listing(sortby, sortorder)
    else:
        dogs_list = model.get_breeds_listing()
    return render_template("breeds.html", breeds_list= dogs_list)



if __name__=="__main__":
    model.init_breeds()
    app.run(debug=True)
