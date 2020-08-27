#use Flask to render a template
from flask import Flask, render_template
#use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
#use the scraping code, convert from Jupyter notebook to Python
import scraping

#setup Flask
app = Flask(__name__)
#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

#define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() #uses PyMongo to find the "mars" collection in database
   return render_template("index.html", mars=mars) #tells Flask to return an HTML template using an index.html file

@app.route("/scrape") #define the route
def scrape():
   mars = mongo.db.mars #assign new variable that points to Mongo database
   mars_data = scraping.scrape_all() #create new variable to hold the newly scraped data
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

#final lines needed to function
if __name__ == "__main__":
   app.run()