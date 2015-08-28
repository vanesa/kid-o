L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([18.542769, -69.801216],16);

var marker;
var clicked = false;

map.on('click', function(e) {
    var child_latitude = e.latlng.lat;
    var child_longitude = e.latlng.lng;
    $("#lat").val(child_latitude)
    $("#lng").val(child_longitude)
  
   if (clicked === false) {
           marker = L.marker(new L.LatLng(child_latitude, child_longitude), {
    icon: L.mapbox.marker.icon({
        'marker-color': 'ff8888'
    }),
    draggable: false
});
    marker.bindPopup('This marker is draggable! Move it around.');
       
       marker.addTo(map);
   	   clicked = true;
   }
   else {
   	marker.setLatLng(new L.LatLng(child_latitude, child_longitude)).update();
    }
});