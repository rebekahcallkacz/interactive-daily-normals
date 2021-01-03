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
normals_database = f'mongodb+srv://{username}:{password}@cluster0.lnnzp.mongodb.net/weather?retryWrites=true&w=majority'

# Configure MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI', normals_database)

# Initialize MongoDB application
mongo = PyMongo(app)

# Format of db in MONGODB:
# Database: weather
# Collection: normals
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
def navbar():
    return render_template('nav.html')

# Will need to add templates for rendering additional webpages 

@app.route('/api/normals')
def getNormals():
    normals_data = mongo.db.normals.find({})
    normals_list = []
    for normals in normals_data:
        del normals['_id']
        normals_list.append(normals)

    return jsonify(normals_list)

@app.route('/api/stations')
def getStations():
    station_data = mongo.db.stations.find({})
    station_list = []
    for station in station_data:
        del station['_id']
        station_list.append(station)

    return jsonify(station_list)

@app.route('/api/zipcodes')
def getZipcodes():
    zip_data = mongo.db.zipcodes.find({})
    zip_list = []
    for zipcode in zip_data:
        del zipcode['_id']
        zip_list.append(zipcode)

    return jsonify(zip_list)

if __name__ == '__main__':
    app.run(debug=True)