$(function() {
  $.getJSON("/api/child_profile/" + window.id, function (data) {

    var child = data.profile[0];

  	L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
    var map = L.mapbox.map('map', 'vanesa.e4c935ef');

    if (!child.longitude) {
      map.setView([18.542769, -69.801216],15);
    }
    else{
      map.setView([child.latitude, child.longitude],15);
    }
    
    // Disable the scroll Zoom
    map.scrollWheelZoom.disable();
    var marker;
    var clicked = false;

    if(child.latitude && child.longitude) {
    marker = L.marker(new L.LatLng(
        child.latitude, child.longitude
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
        marker.bindPopup(child.first_name + "'s home location.");
               
        marker.addTo(map);
        clicked = true;
      }
      else {
        marker.setLatLng(new L.LatLng(child_latitude, child_longitude)).update();
      }
    });

    $('#delete_address').on('click', function() {
      map.removeLayer(marker);
      $("#lat").val();
      $("#lng").val();
    });
  });
});