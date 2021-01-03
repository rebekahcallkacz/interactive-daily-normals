# interactive-daily-normals
This project determines ranges which are appropriate for laying epoxy.

## Tasks
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


## TODO

* Build out Flask API
    Dynamic search: date/zipcode (zip required, dates not)
    Zipcode pulls closest weather station from zipcodes collection and uses that to filter normals collection
    Optional additional filter is dates for normals
* Create plot(s): https://plotly.com/javascript/filled-area-plots/ 
* Work on HTML
* Create API
* Write website text/info
