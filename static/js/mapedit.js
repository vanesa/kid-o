L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
var map = L.mapbox.map('map', 'mapbox.streets')
    .setView([{{child.latitude}}, {{child.longitude}}],15);

var marker;
var clicked = false;


marker = L.marker(new L.LatLng({{child.latitude}}, {{child.longitude}}));
console.log({{child.latitude}}, {{child.longitude}});
marker.addTo(map);

map.on('click', function(e) {
    var child_latitude = e.latlng.lat;
    var child_longitude = e.latlng.lng;
    $("#lat").val(child_latitude)
    $("#lng").val(child_longitude)

   	marker.setLatLng(new L.LatLng(child_latitude, child_longitude)).update();
});