# Interactive Daily Normals Website
Version 1.0.0

## [View the Website](https://dailynormals.herokuapp.com/)

## Description
This project displays daily normals (max, min, and average) for a given date range and zip code in the Southeast United States in order to assist in determining the best time to schedule concrete restoration contracts.

## Background
My client works for a concrete restoration company and is responsible for scheduling job contracts in the Southeast United States. Concrete restoration projects which use epoxy require that the temperature be between 50 and 100 degrees in order for the epoxy to properly adhere. For my client, it is essential that they know when temperatures will most likely be within this range. To assist my client when planning these contract jobs, I collected data on daily temperatures in the Southeast US and displayed it on a searchable website.

## Data
NCEI's data was chosen due to its availability and how extensive it is: 30 years of normals normed by measurement (Arguez et al., 2010). This should provide a fairly accurate evaluation of what the average temperature is for any calendar date. The 8 states (AL, GA, KY, NC, SC, TN, WV, and VA) my client works in most regularly were selected for this analysis.

![alt text](https://github.com/rebekahcallkacz/interactive-daily-normals/blob/main/static/images/etl.jpg "ETL Process")

### Extract
Temperature data for the 8 selected states were downloaded from NCEI's 1981-2010 U.S. Climate Normals dataset. This dataset included 932 weather stations with daily normals recorded for all 366 calendar dates. The dataset had close  to 350,000 entries.

Zip codes for the Southeast United States were downloaded from the Free Zip Code Database (Coven, 2012).

### Transform
Weather stations that did contained null values for any of the daily normals were removed from the dataset.

The original weather dataset did not include location data outside of geographic coordinates. The station names all included the state they were located in, so state data was extracted using regex. County and zip code for each weather station were determined using Google's Geocoding API. The weather dataset was split into two datasets: normals by date for each weather station and station metadata. 

Since the goal of this project was to be able to search for weather data by any zip code in the region (and not just the zip codes of the weather stations), the closest weather station to each zip code in the zip code database was calculated. This was stored in a zipcode dataset. Although there are API's that can calculate this in real time, they are costly to deploy which is why this method was chosen instead. 

### Load
These three datasets (normals, stations and zipcodes) were uploaded to two MongoDB databases: one local for testing and one in Atlas for deployment. In addition, due to the size of the normals collection, a subset of the normals collection was stored in a separate collection for testing.

## Methods
Heroku was used to deploy a full stack application allowing the user to search for daily normals by zipcode and calendar date. In order to avoid being throttled in MongoDB's free tier, the website was designed so that the user must search each zipcode individually and cannot request the entire dataset at once.

### Calendar Days vs. Dates
In the normals dataset, the field "DATE" is in the format "MM-DD" since this is a dataset of averages calculated across multiple years. This poses challenges when attempting to filter the data. In order to store the date in MONGODB using the Date datatype, a new field ("DATE_FILTER") was created which contains "MM-DD-2008". The year 2008 was chosen because it is a leap year within 1981-2010 (the timeframe in which the dataset was collected). 

The date range picker on the front end is a JavaScript library. Date range pickers assume that the entire date is of interest, and they allow the user to pick a date or date range which always includes a year. For ease of use, this functionality was not disabled. Instead, the API route was built to accommodate any year(s). The user enters their dates which are appended to the API call. These dates are then converted to the year 2008 and the appropriate calendar days are returned. The data displayed to the user does not include years since the dataset does not actually contain years. 

### App Architecture
![alt text](https://github.com/rebekahcallkacz/interactive-daily-normals/blob/main/static/images/architecture.jpg "App Architecture")

A total of 5 Flask API routes were created.
1. All normals: This route returns recorded daily normals for all stations in the dataset (this is not available to the user at this time).
2. All stations: This route returns the metadata for all stations in the dataset.
3. All zipcodes: This route returns all zipcodes in the dataset and their nearest weather station (this is not available to the user at this time).
4. Normals filtered by zipcode: This route first determines the nearest weather station based on the zipcode. It then returns all daily normals for this weather station.
5. Normals filtered by zipcode and date range: This route first determines the nearest weather station based on the zipcode. It then returns daily normals for this weather station filtered by the given date range. 

The date range picker was generated using the Javascript library Date Range Picker, the visualizations were created using Leaflet and Plotly, the table of data was created using DataTables.js and interactivity, filtering and API calls were created using D3.js.

## Results: [View the Website](https://dailynormals.herokuapp.com/)
When the user enters their search parameters, the webpage displays a line graph of the daily normals, metadata about the weather station and a downloadable datatable with the dates and normals. 

![alt text](https://github.com/rebekahcallkacz/interactive-daily-normals/blob/main/static/images/results1.jpg "Resuts Page pt. 1")

![alt text](https://github.com/rebekahcallkacz/interactive-daily-normals/blob/main/static/images/results2.jpg "Results Page pt. 2")

The user can also view an interactive map of all weather stations in the dataset. 

![alt text](https://github.com/rebekahcallkacz/interactive-daily-normals/blob/main/static/images/map1.jpg "Map pt. 1")

The user can click on each weather station to view further information about that station.

![alt text](https://github.com/rebekahcallkacz/interactive-daily-normals/blob/main/static/images/map2.jpg "Map pt. 2")

## Limitations
Predicting weather is particularly difficult even only a few days beforehand, so, although this analysis provides general guidelines as to what the weather might be like, it is not guaranteed to be accurate. In the future, I would like to add more states to the database and create a publicly available API. In addition, the functionality of the website on mobile could be improved.

## References 
Arguez, A., Durre, I., Applequist, S., Squires, M., Vose, R., Yin, X., and Bilotta, R. (2010). NOAA's U.S. Climate Normals (1981-2010). [AL, GA, KY, NC, SC, TN, WV, and VA]. NOAA National Centers for Environmental Information. DOI:10.7289/V5PN93JP[12-7-2020].

Coven, D. S., (2012). Free Zipcode Database: All Locations [data file]. Retrieved from http://federalgovernmentzipcodes.us

## Contributors
Rebekah Callari-Kaczmarczyk

## License and Copyright
&copy; Rebekah Callari-Kaczmarczyk

