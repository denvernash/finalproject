
from flask import Flask, render_template, request
import model
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/maps/<nm>")
def maps(nm):
    model.get_maps(to_look_up = nm)
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        dogs_list = model.get_breeds_listing(sortby, sortorder)
    else:
        dogs_list = model.get_breeds_listing()
    return render_template("breeds.html", breeds_list= dogs_list)

@app.route("/breeds", methods=['GET', 'POST'])
def breeds():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        dogs_list = model.get_breeds_listing(sortby, sortorder)
    else:
        dogs_list = model.get_breeds_listing()
    return render_template("breeds.html", breeds_list= dogs_list)

@app.route("/dogs/<nm>", methods=['GET', 'POST'])
def dogs(nm):
    model.get_dogs(nm)
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        dogs_list = model.get_dogs_listing(sortby, sortorder)
    else:
        dogs_list = model.get_dogs_listing()
    return render_template('dogs.html', dogs_list = dogs_list, number=nm)

@app.route("/breed_details/<nm>")
def details(nm):
    image = model.get_images(nm)
    image_url = image.image_url
    content_url = image.content_url
    title = image.title
    author = image.username
    license_url = image.license_url

    breed = model.get_breed_details(nm)
    breed_id = breed.id
    breed_type = breed.breed
    height = breed.height
    wt = breed.weight
    coat = breed.coat
    color = breed.color
    life_span = breed.life_span
    litter_size = breed.litter_size

    return render_template('breed_details.html', image_url = image_url, content_url= content_url, title = title,
    author = author, license_url = license_url, breed_id = breed_id, breed_type = breed_type, height = height,
    weight = wt, coat = coat, color = color,
    life_span = life_span, litter_size = litter_size
    )

if __name__=="__main__":
    model.init_breeds()
    app.run(debug=True)
