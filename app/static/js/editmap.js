$(function() {
	L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
  var map = L.mapbox.map('map', 'vanesa.e4c935ef')
  .setView([latitude, longitude],15);
  // Disable the scroll Zoom
  map.scrollWheelZoom.disable();
  var marker;
  var clicked = false;

  if(latitude && longitude) {
  marker = L.marker(new L.LatLng(
      latitude, longitude
    ));
  marker.addTo(map);
	}

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
      marker.bindPopup("Child's home location.");
             
      marker.addTo(map);
      clicked = true;
    }
    else {
      marker.setLatLng(new L.LatLng(child_latitude, child_longitude)).update();
    }
  });
  
  $('#delete_address').on('click', function(marker) {
    map.removeLayer(marker);
  });
});