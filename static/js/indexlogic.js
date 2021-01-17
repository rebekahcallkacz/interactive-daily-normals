// References: http://www.daterangepicker.com/ 

// Select the zipcode search button
var zip_search = d3.select('#zip-search');

// Select the date range button (adds datepicker to page)
var date_picker = d3.select('#add-dates');

// Create event listeners for buttons
zip_search.on('click', zipAPI);

date_picker.on('click', showDatePicker);

// This shows the date picker
function showDatePicker(){
    var date_picker = d3.select('#date-picker');
    date_picker.classed('d-none', false);
}

// Initiate date range picker
$(function() {
    $('input[name="daterange"]').daterangepicker({
        "showDropdowns": true,
      opens: 'left'
    }, function(start, end, label) {
        var zipcode = d3.select('#zipcode').property('value');
        let api_call = '/api/' + zipcode + '/' + start.format('YYYY-MM-DD') + '/' + end.format('YYYY-MM-DD')
        console.log(api_call)
        generatePlot(api_call);
    });
  });

// This function prints the zipcode input
  function zipAPI(){
    // Select the zipcode input
    var zipcode = d3.select('#zipcode').property('value');
    let api_call = '/api/' + zipcode
    console.log(api_call)
    generatePlot(api_call)
}

// This function generates the plot
function generatePlot(api_call) {
    console.log('get data and plot here')
}