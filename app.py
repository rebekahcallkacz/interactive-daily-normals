# Dependencies
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv

# Pull passwords from your .env file for when you are working locally
# TODO: Create a .env file at the same level as this file - include these two lines:
# db_username='mongodbusername'
# db_password='mongodbpassword'

load_dotenv()
username = os.getenv("db_username")
password = os.getenv("db_password")

# Initialize the Flask app
app = Flask(__name__)

# Connection to MongoDB database
normals_database = f'mongodb+srv://{username}:{password}@clusterprime.mpaq0.mongodb.net/ETL?retryWrites=true&w=majority'

# Configure MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI', normals_database)

# Initialize MongoDB application
mongo = PyMongo(app)

# Format of db in MONGODB:
# Database: normals
# Collection: weather
# Keys: ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'DLY-TAVG-NORMAL', 'DLY-TAVG-STDDEV', 'DLY-TMAX-NORMAL', 
# 'DLY-TMAX-STDDEV', 'DLY-TMIN-NORMAL', 'DLY-TMIN-STDDEV', 'STATE', 'COUNTY', 'ZIP']
# Collection: stations
# Keys: ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'STATE', 'COORD', 'COUNTY', 'ZIP']
# Collection: zipcodes
# Keys: ['ZIP', 'STATE', 'LATITUDE', 'LONGITUDE', 'CLOSEST-STATION']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nav')
def home():
    return render_template('nav.html')

# Will need to add templates for rendering additional webpages 

# @app.route('/api/stations')
# def getStations():
#     station_data = mongo.db.stations.find({})

#     return station_data

if __name__ == '__main__':
    app.run(debug=True)