$(function() {
  L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
  
  var geojson = [];

  for (child in window.children) {
  	child = window.children[child];
  	if (child.photo_url == '/static/images/childphotopreview.png') {
  		var child_photo = '/static/images/photos/childphotopreview.png';
  	}
  	else if (child.photo_url.indexOf(child.first_name.toLowerCase()) !== -1) {
  		var child_photo = child.photo_url;
  	}
  	else {
  		var child_photo = '/static/images/photos/childphotopreview.png';
  	}

  	var description = 'lives here '
  	if (child.guardian_fname || child.siblings_in_project) {
  		description += 'with ';
  	}
  	else if (child.guardian_fname) {
			description.append(child.guardian_fname + ' ' + child.guardian_lname + ' ');
  	}
  	else if (child.siblings_in_project) {
			description.append(child.siblings_in_project);
  	}

		var child_geo = {
	    'type': 'Feature',
	    'geometry': {
	    'type': 'Point',
	    'coordinates': [child.longitude, child.latitude]
	    },
	    'properties': {
	  	'image': child_photo,
	  	'title': child.first_name + ' ' + child.last_name,
	  	'url': '/child/' + child.id,
			'description': description,
			'marker-color': '#fc4353',
			'marker-size': 'large',
			'marker-symbol': 'building'
			}
		};

	geojson.push(child_geo);

  }


//   var geojson = [
//   // Loop through each child and create marker and tooltip containing the information available
//   {% for child in child_profiles %}
//     {% if child.latitude and child.longitude %}
//       {
//       'type': 'Feature',
//       'geometry': {
//       'type': 'Point',
//       'coordinates': [{{ child.longitude }},{{ child.latitude }}]
//       },
//       'properties': {
//     'image': '/static/images/photos/' + {% if child.photo_url == '/static/images/childphotopreview.png' %}'childphotopreview.png'{% elif child.photo_url == '/static/images/photos/' + child.first_name.lower() + '.jpg' %}'{{ child.first_name }}'.toLowerCase() + '.jpg' {% else %} 'childphotopreview.png'{% endif %},
//     'title': '{{ child.first_name }} {{ child.last_name }}',
//     'url': '/child/{{ child.id }}',
//   'description': 'lives here {% if child.guardian_fname and child.guardian_lname or child.siblings_in_project %} with {{ child.guardian_fname }} {{ child.guardian_lname }} {% if child.guardian_type %}({{ child.guardian_type }}){% else %} {% endif %} {{ child.siblings_in_project}} {% else %}{% endif %}',
//   'marker-color': '#fc4353',
//   'marker-size': 'large',
//   'marker-symbol': 'building'
//   }
// },{% endif %}{% endfor %}
// ];

var map = L.mapbox.map('map', 'vanesa.e4c935ef', {
  scrollWheelZoom: false
})
.setView([18.542769, -69.801216], 15)
.featureLayer;
// Add custom feature to the tooltip
map.on('layeradd', function(e) {
  var marker = e.layer,
  feature = marker.feature;

  // Create custom popup content
  var popupContent =  '<div class="popupleft"><a href="' + feature.properties.url + '">' +
      '<img class="popupimage" src="' + feature.properties.image + '" />' + '</div>' + '<div class="popupright">' +
      '<a href="' + feature.properties.url + '">' + feature.properties.title +
      '</a> ' + feature.properties.description + '</div>';

    // http://leafletjs.com/reference.html#popup
    marker.bindPopup(popupContent,{
      closeButton: false,
      minWidth: 180
      });
      });

      map.setGeoJSON(geojson);
});