from flask import Flask, render_template, redirect
import scrape_mars
import pymongo

app = Flask(__name__)  # Creating an instance of Flask module

# setting up mongo connection via pymongo
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars_db

# Routes


@app.route('/')
def index():
    mars_complete_data = list(db.mars.find())[0]
    mars_hemi_data = list(db.mars.find())[0]["hemisphere"]
    return render_template('index.html', mars_complete_data=mars_complete_data, mars_hemi_data=mars_hemi_data)


@app.route('/scraper')
def scrape():
    # Call the scrape method
    mars_data = scrape_mars.scrape()
    db.mars.update({}, mars_data)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
