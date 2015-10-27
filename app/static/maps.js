L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
var map = L.mapbox.map('map', 'mapbox.streets', {
  zoomControl: false }).setView([37.9, -77],4);
// Disable the scroll Zoom
    map.scrollWheelZoom.disable();
var marker = L.marker(new L.LatLng(37.9, -77), {
    icon: L.mapbox.marker.icon({
        'marker-color': 'ff8888'
    }),
    draggable: true
});


marker.bindPopup('This marker is draggable! Click Edit on the profile to move it around.');

addMarker = function() {
    marker.addTo(map);
}

// to update the lat/long on marker changes
listenToMarker = function() {
    //pseudo
    marker.onChange(updateCoordinates()); //mapbox should have some similar function to onChange
}
listenToMarker();


updateCoordinates = function() {
    //first, take the new lat, long from the "marker" object
    
    //pseudo
    var newLat = marker.getLatitude; //get this from their docs
    
    //send http request to update the child's coordinates
    var params = "latitude=" + newLat.toString() + "&longitude=" + newLong.toString();
    
    
  x = new(this.XMLHttpRequest || ActiveXObject)('MSXML2.XMLHTTP.3.0');
  x.open("POST", url, false);
  x.send();
}