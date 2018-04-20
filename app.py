
from flask import Flask, render_template, request
import model
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/maps/<nm>")
def maps(nm):
    model.get_maps(to_look_up = nm)
    return render_template("breeds.html")

@app.route("/breeds", methods=['GET', 'POST'])
def breeds():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        dogs_list = model.get_breeds_listing(sortby, sortorder)
    else:
        dogs_list = model.get_breeds_listing()
    return render_template("breeds.html", breeds_list= dogs_list)

@app.route("/dogs", methods=['GET', 'POST'])
def dogs():
    return render_template('dogs.html', dogs_list = '')

@app.route("/breed_details/<nm>")
def details(nm):
    pass

if __name__=="__main__":
    model.init_breeds()
    app.run(debug=True)
