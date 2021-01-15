# interactive-daily-normals
This project determines date ranges which are appropriate for laying epoxy.

## Tasks
* Make dataset leaner (remove any unnecessary/unused columns)
* Add date that includes a year to dataset (2008)
* Create Flask API
    3. Filter by date and zipcode
* Create plots/visuals with filtered data
    1. Daily normals for given date range (w/ background color to indicate "good" colors)
    2. Table w/ temps for given date range
* Build website
    1. Navbar 
    2. Search page
    3. Search results w/ dashboard
    4. Landing page
    5. Data page (data sources)


## TODO
* Clean/update data
* Build out Flask API
    Dynamic search: date/zipcode (zip required, dates not)
* Sketch out HTML layout
* Create JS/plot(s): https://plotly.com/javascript/filled-area-plots/ 
    Require zip code filter
    Allow date filter
        Potential library: https://bootstrap-datepicker.readthedocs.io/en/latest/  - tutorial for this library: https://formden.com/blog/date-picker - sandbox: https://uxsolutions.github.io/bootstrap-datepicker/?markup=input&format=&weekStart=&startDate=&endDate=&startView=0&minViewMode=0&maxViewMode=4&todayBtn=false&clearBtn=false&language=en&orientation=auto&multidate=&multidateSeparator=&keyboardNavigation=on&forceParse=on#sandbox 
        Another library (date range): http://www.daterangepicker.com/ 

* Work on HTML
* Write website text/info
* Create API
