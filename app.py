# Dependencies
from flask import Flask, render_template, jsonify
from flask_pymongo import PyMongo
import os
from dotenv import load_dotenv
import datetime as dt
import re

# Pull passwords from your .env file for when you are working locally
# TODO: Create a .env file at the same level as this file - include these two lines:
# db_username='mongodbusername'
# db_password='mongodbpassword'

load_dotenv()
username = os.getenv("db_username")
password = os.getenv("db_password")
API_KEY = os.getenv("API_KEY")

# This function unpacks MONGODB data
def returnNormals(data):
    normals_list = []
    for normals in data:
        normals_list.append(normals)
    return(normals_list)

# This function replaces the year in a date with the year 2008
def formatYear(date_string):
    regex = re.compile('[0-9][0-9][0-9][0-9](-[0-9][0-9]-[0-9][0-9])')
    date = '2008' + regex.findall(date_string)[0]
    return date

# Initialize the Flask app
app = Flask(__name__)

# Connection to MongoDB database
normals_database = f'mongodb+srv://{username}:{password}@cluster0.lnnzp.mongodb.net/weather?retryWrites=true&w=majority'
local_database = 'mongodb://localhost:27017/weather'

# Configure MongoDB
app.config['MONGO_URI'] = os.environ.get('MONGODB_URI', local_database)

# Initialize MongoDB application
mongo = PyMongo(app)

# Format of db in MONGODB:
# Database: weather
# Collection: normals
# In this dataset, 'DATE' is an aggregate (the average of 1981-2010) and is in the format 'MM-DD' for all 366 calendar days. 
# Because date functionality in MongoDB requires a year, a 'DATE_FILTER' field was added which contains 'MM-DD-2008'
# Keys: ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'ELEVATION', 'DATE', 'DLY-TAVG-NORMAL', 'DLY-TAVG-STDDEV', 'DLY-TMAX-NORMAL', 
# 'DLY-TMAX-STDDEV', 'DLY-TMIN-NORMAL', 'DLY-TMIN-STDDEV', 'STATE', 'COUNTY', 'ZIP', 'DATE_FILTER']
# Collection: stations
# Keys: ['STATION', 'NAME', 'LATITUDE', 'LONGITUDE', 'STATE', 'COORD', 'COUNTY', 'ZIP']
# Collection: zipcodes
# Keys: ['ZIP', 'STATE', 'LATITUDE', 'LONGITUDE', 'CLOSEST-STATION']
# Collection: normals_test
# Keys: same as normals except only contains zipcodes 27253 (1 weather station) and 27215 (2 weather stations)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/nav')
def navbar():
    return render_template('nav.html')

@app.route('/methods')
def methods():
    return render_template('methods.html')

@app.route('/data')
def data():
    return render_template('data.html', API_KEY=API_KEY)

@app.route('/about')
def about():
    return render_template('about.html')


# These routes return data

# This route returns all normals for all stations in the dataset
@app.route('/api/allnormals')
def getNormals():
    normals_data = mongo.db.normals.find({})
    normals_list = []
    for normals in normals_data:
        del normals['_id']
        normals_list.append(normals)

    return jsonify(normals_list)

# This route returns metadata for all stations in the dataset
@app.route('/api/allstations')
def getStations():
    station_data = mongo.db.stations.find({}, {'LATITUDE':1, 'LONGITUDE':1, 'NAME':1, 'COUNTY':1, 'ZIP':1})
    station_list = []
    for station in station_data:
        del station['_id']
        station_list.append(station)

    return jsonify(station_list)

# This route returns all zipcodes in the SE US and their closest weather station
@app.route('/api/allzipcodes')
def getZipcodes():
    zip_data = mongo.db.zipcodes.find({})
    zip_list = []
    for zipcode in zip_data:
        del zipcode['_id']
        zip_list.append(zipcode)

    return jsonify(zip_list)

# This route returns all normals for a specific zipcode
@app.route('/api/<zipcode>')
def searchZipcode(zipcode):
    zip_data = mongo.db.zipcodes.find({'ZIP':zipcode})
    zip_list = []
    for doc in zip_data:
        del doc['_id']
        zip_list.append(doc)
    if len(zip_list) > 0:
        weather_station = zip_list[0]['CLOSEST-STATION']
        normals_data = mongo.db.normals.find({'NAME': weather_station}, {'DATE_FILTER':1, 
        'DATE':1,
        'DLY-TAVG-NORMAL':1, 
        'DLY-TMAX-NORMAL':1, 
        'DLY-TMIN-NORMAL':1,
        'NAME':1,
        'COUNTY':1,
        'ZIP':1})
        normals_list = []
        for normals in normals_data:
            del normals['_id']
            normals_list.append(normals)

        return jsonify(normals_list)

    else:
        return jsonify(zip_list)

# This route returns normals for a given zipcode and date range 
# Dates should be in the form: 'YYYY-MM-DD'
# The dataset includes an average of normals from 1981-2010. For this reason, an arbitrary year (2008) was assigned
# to the dataset to allow for MongoDB date filtering. When the user enters a date range that spans multiple years, 
# e.g. 12/31/2020 - 1/20/2021, this creates an issue with filtering in MongoDB and also creates issues with presenting
# the data to the user on the front end. For this reason, the type of date range requested is tested and if this type of 
# range is required, this difference in years is also noted.
@app.route('/api/<zipcode>/<start>/<end>')
def searchDate(zipcode, start, end):
    zip_data = mongo.db.zipcodes.find({'ZIP':zipcode})
    zip_list = []
    for doc in zip_data:
        del doc['_id']
        zip_list.append(doc)

    # If the zipcode is in the database, return the normals for the nearest weather station
    if len(zip_list) > 0:
        # Determine if dates are in same year
        start_year = dt.datetime.strptime(start, '%Y-%m-%d').year
        end_year = dt.datetime.strptime(end, '%Y-%m-%d').year
        # If the search is within one year, create a filter between those two dates but w/ the year 2008
        if start_year == end_year:
            # Format years to match those in database (2008)
            start_2008 = formatYear(start)
            end_2008 = formatYear(end)
            start_filter = dt.datetime.strptime(start_2008, '%Y-%m-%d')
            end_filter = dt.datetime.strptime(end_2008, '%Y-%m-%d') + dt.timedelta(days=1)

            # Select this range in mongodb
            weather_station = zip_list[0]['CLOSEST-STATION']

            normals_data = mongo.db.normals.find({'NAME': weather_station, 
            'DATE_FILTER': {'$gte': start_filter, '$lte': end_filter}}, {'_id':0, 'DATE_FILTER':1, 
            'DATE':1,
            'DLY-TAVG-NORMAL':1, 
            'DLY-TMAX-NORMAL':1, 
            'DLY-TMIN-NORMAL':1,
            'NAME':1,
            'COUNTY':1,
            'ZIP':1})

            # Unpack MONGODB object
            normals_list = returnNormals(normals_data)

        # Determine if the search spans more than one year 
        else:
            # If there is only year difference between the two dates, return start - end of 2008 AND beginning of 2008 - end
            # In order to ensure that front end display is in the order the user expects based on their input
            # (e.g. Dec 31, 2020 - Jan 1 ,2021), the 'DATE_FILTER' is manipulated to record the difference in years
            if (end_year - start_year) == 1:
                # Format dates for filtering in MONGODB
                start_1 = formatYear(start)
                start_2 = '2008-01-01'
                end_1 = '2008-12-31'
                end_2 = formatYear(end)
                start_filter_1 = dt.datetime.strptime(start_1, '%Y-%m-%d')
                end_filter_1 = dt.datetime.strptime(end_1, '%Y-%m-%d') + dt.timedelta(days=1)
                start_filter_2 = dt.datetime.strptime(start_2, '%Y-%m-%d')
                end_filter_2 = dt.datetime.strptime(end_2, '%Y-%m-%d') + dt.timedelta(days=1)

                # Determine weather station nearest to the zipcode
                weather_station = zip_list[0]['CLOSEST-STATION']

                # Search for this zipcode and these date ranges in MONGODB
                normals_data = mongo.db.normals.find({'$or': 
                [{'NAME': weather_station, 'DATE_FILTER': {'$gte': start_filter_1, '$lte': end_filter_1}}, 
                {'NAME': weather_station, 'DATE_FILTER': {'$gte': start_filter_2, '$lte': end_filter_2}}]}, 
                {'_id':0, 
                'DATE_FILTER':1, 
                'DATE':1,
                'DLY-TAVG-NORMAL':1, 
                'DLY-TMAX-NORMAL':1, 
                'DLY-TMIN-NORMAL':1,
                'NAME':1,
                'COUNTY':1,
                'ZIP':1})

                # Unpack MONGODB object
                normals_list = []
                normals_list = returnNormals(normals_data)

                # If the full dataset was not returned, replace 2008 with the search years
                if len(normals_list) != 366:
                    for normals in normals_list:
                        date_filter = normals['DATE_FILTER']
                        # If date is in first range, add first year
                        if date_filter > end_filter_2:
                            normals['DATE_FILTER'] = date_filter.replace(year=start_year)
                        # If date is in second range, add second year
                        else:
                            normals['DATE_FILTER'] = date_filter.replace(year=end_year)

            # If there is more than a one year difference, return the entire year of 2008
            else:
                weather_station = zip_list[0]['CLOSEST-STATION']

                normals_data = mongo.db.normals.find({'NAME': weather_station}, {'_id':0,
                'DATE_FILTER':1, 
                'DATE':1,
                'DLY-TAVG-NORMAL':1, 
                'DLY-TMAX-NORMAL':1, 
                'DLY-TMIN-NORMAL':1,
                'NAME':1,
                'COUNTY':1,
                'ZIP':1})           

                # Unpack MONGODB object
                normals_list = returnNormals(normals_data)

        return jsonify(normals_list)

    # If the zipcode is not in the database, return an empty list
    else:
        return jsonify(zip_list)
        
if __name__ == '__main__':
    app.run(debug=True)