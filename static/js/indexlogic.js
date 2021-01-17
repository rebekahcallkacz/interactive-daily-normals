// Select the zipcode search button
var zip_search = d3.select('#zip-search');

// Select the date range button (adds datepicker to page)
var date_picker = d3.select('#add-dates');

// Create event listeners for buttons
zip_search.on('click', printZip);

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
        // Select search button
        var search = d3.select('#add-dates');

        // Create event listener for button
        search.on('click', generatePlot(start, end));
    });
  });

// This function prints the zipcode input
  function printZip(){
    // Select the zipcode input
    var zipcode = d3.select('#zipcode').property('value');
    console.log(zipcode)
}

// This function generates the plot
function generatePlot(start, end) {
    // Select zipcode entry
    var zipcode = d3.select('#zipcode').property('value');
    console.log(zipcode)
    console.log("A new date selection was made: " + start.format('YYYY-MM-DD') + ' to ' + end.format('YYYY-MM-DD'));
    console.log(start)
    console.log(end)
}