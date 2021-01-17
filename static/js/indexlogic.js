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
        generatePlot(api_call);
    });
  });

// This function prints the zipcode input
  function zipAPI(){
    // Select the zipcode input
    var zipcode = d3.select('#zipcode').property('value');
    let api_call = '/api/' + zipcode;
    generatePlot(api_call);
}

// This function generates the plot
function generatePlot(api_call) {
    d3.json(api_call).then((data) => {
      console.log(data);

      // Set up marker for temps in range
      var temp_min = {
        // Set these to max/min of dataset x
        x: [0, 100],
        y: [40, 100]
      };

      var temp_buffer = {
        x: [0, 100],
        y: [20, 20],
      };

      // Set up layout
      var layout = {
        title: 'Daily Normals for Selected Date Range',
        shapes: [
          {
            type: 'rect',
            //xref: 'paper',
            //yref: 'y',
            x0: 0,
            y0: 50,
            // Set to max of dataset
            x1: 100,
            y2: 100,
            fillcolor: '#d3d3d3',
            opacity: '0.3',
            line: {
              width:0
            } 
          }
        ]
      }

      var data = [temp_min, temp_buffer]

      Plotly.newPlot('normals-plot', data, layout)
    })
}