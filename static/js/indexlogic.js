// References: http://www.daterangepicker.com/ 
// https://stackoverflow.com/questions/6291225/convert-date-from-thu-jun-09-2011-000000-gmt0530-india-standard-time-to

// Colors for the plot(s)
// Bright blue, light green, dark blue, light blue
var colors = ["rgb(32,142,183)", "rgb(167,212,121)", "rgb(28,69,133)", "rgb(160,205,226)"]

// This function parses the dates to only return year/month/day
function formatXticks(str) {
  var date = new Date(str),
    mnth = ("0" + (date.getMonth() + 1)).slice(-2),
    day = ("0" + date.getDate()).slice(-2);
  return [date.getFullYear(), mnth, day].join("-");
}; 

// This function formats the dates for the plot title
function formatDateRange(str) {
  var date = new Date(str),
    mnth = ("0" + (date.getMonth() + 1)).slice(-2),
    day = ("0" + date.getDate()).slice(-2);
  return [mnth, day].join("-");
}; 

// This function creates the plot
function generatePlot(data){
        // Set up marker for temps in range
        var min = {
          type: 'scatter',
          mode: 'lines',
          line: {
            color: 'rgb(160,205,226)'
          },
          x: data.map(date => formatXticks(date['DATE_FILTER'])),
          y: data.map(date => date['DLY-TMIN-NORMAL']),
          name: 'Minimum (F)'
        };
  
        var avg = {
          type: 'scatter',
          mode: 'lines',
          line: {
            color: 'rgb(32,142,183)'
          },
          x: data.map(date => formatXticks(date['DATE_FILTER'])),
          y: data.map(date => date['DLY-TAVG-NORMAL']),
          name: 'Average (F)'
        };
  
        var max = {
          type: 'scatter',
          mode: 'lines',
          line: {
            color: 'rgb(28,69,133)'
          },
          x: data.map(date => formatXticks(date['DATE_FILTER'])),
          y: data.map(date => date['DLY-TMAX-NORMAL']),
          name: 'Maximum (F)'
        }; 
  
        // Calculate max and min dates in range
        let max_date = d3.max(data.map(date => date['DATE_FILTER']))
        let min_date = d3.min(data.map(date => date['DATE_FILTER']))
  
        // Set up layout
        var layout = {
          title: `Daily Normals for ${formatDateRange(min_date)} to ${formatDateRange(max_date)}`,
          xaxis: {
            tickformat: '%b-%e',
            tickangle: 45,
          },
          yaxis: {
            range: [0, 120]
          },
          legend: {
            x: 1,
            y: 0.75
          },
          shapes: [
            {
              type: 'rect',
              yref: 'y',
              xref: 'paper',
              x0: 0,
              y0: 50,
              // Set to max of dataset
              x1: 50,
              y1: 100,
              fillcolor: 'rgb(167,212,121)',
              opacity: '0.2',
              line: {
                width:0
              } 
            }
          ]
        };
  
        var data = [min, avg, max];
  
        Plotly.newPlot('normals-plot', data, layout);
};

// This function adds station metadata to the page
function addStationData(data){
  // Clear previous text
  d3.selectAll('#station-data').text('');

  d3.select('#station-name').text(data['NAME']);
  d3.select('#station-county').text(data['COUNTY']);
  d3.select('#station-zipcode').text(data['ZIP']);
}
// This function creates a datatable
function createDataTable(data){
  // Destroy former datatable
  try {
    $('#data').DataTable().destroy()
  }
  finally {
    // Format dates
    for (i=0; i<data.length; i++) {
      let format_date = formatDateRange(data[i]['DATE_FILTER'])
      data[i]['DATE_FILTER'] = format_date
    };
    // Select and reveal table html
    d3.select('#data').classed('d-none', false)

    // Initiate datatable
    $(document).ready(function() {
      $('#data').DataTable( {
        data: data,
        'columns': [
          {'data': 'DATE_FILTER'},
          {'data': 'DLY-TMIN-NORMAL'},
          {'data': 'DLY-TAVG-NORMAL'},
          {'data': 'DLY-TMAX-NORMAL'}
        ],
        searching: false,
        dom: 'Bfrtip',
        buttons: [
          'copy', 'csv', 'excel'
        ]
      });
    });
  }
}

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
        showData(api_call);
    });
  });

// This function prints the zipcode input
  function zipAPI(){
    // Select the zipcode input
    var zipcode = d3.select('#zipcode').property('value');
    let api_call = '/api/' + zipcode;
    showData(api_call);
}

// This function calls in the data and displays it on the webpage
function showData(api_call) {
    d3.json(api_call).then((data) => {
      // Create the plot
      generatePlot(data);
      createDataTable(data);
      addStationData(data[0]);
    })
}