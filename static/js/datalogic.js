// This function plots all stations on a map
function plotStations(data){
    console.log(data)
}


// Call in the data
d3.json('api/allstations').then((station_data) => {
    plotStations(station_data)
})