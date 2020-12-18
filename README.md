# interactive-daily-normals
This project determines ranges which are appropriate for laying epoxy.


## Questions
* Where should I store the data? MongoDB Atlas/Postgres
* Is there a preferred order to creating the different pieces of the project?




## TODO
* Create ERD - upload data to database
    1. Table 1: Zip code in SE w/ nearest weather station
    2. Table 2: Weather station metadata (zipcodes, station IDs, counties, etc.)
    3. Table 3: Weather data (daily normals for entire year for each station)
* Create Flask API
    1. Filter by zipcode 
    2. Filter by date
    3. Filter by date and zipcode
    4. Find closest weather station to given zip code
* Create plots/visuals with filtered data
    1. Daily normals for given date range (w/ background color to indicate "good" colors)
    2. Table w/ temps for given date range
* Build website
    1. Navbar 
    2. Search page
    3. Search results w/ dashboard
    4. Landing page
    5. Data page (data sources)
* Heroku deployment
