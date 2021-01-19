// This function plots all stations on a map
function plotStations(data){
    // Initialize map
    var myMap = L.map("map", {
        center: [
            35.5951, -82.5515
        ],
        zoom: 5
          });

    // Create base map layer
    L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "outdoors-v11",
        accessToken: API_KEY
      }).addTo(myMap);

    // Set circle marker properties
    let properties = {fillOpacity: 0.8, weight: 1, color: 'white', fillColor: "rgb(28,69,133)", radius: 5}
        
    // Create station layers 
    for (var i = 0; i < data.length; i++) {
        let station = data[i];
        let coords = [parseFloat(station['LATITUDE']), parseFloat(station['LONGITUDE'])]

        L.circleMarker(coords, properties)
          .bindPopup("<h5>" + station['NAME'] + "</h5> <hr> <h6>County: " + station['COUNTY'] + "</h6><br><h6>Zipcode: " + station['ZIP'] + "</h6>")
          .addTo(myMap);
    }
}

// Call in the data
d3.json('api/allstations').then((station_data) => {
    plotStations(station_data)
})