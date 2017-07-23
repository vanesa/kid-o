$(function() {
	$(".hidden-profiles").css("display", "none");
	$.getJSON("/api/children_location",function (data) {
	  L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
	  
	  var geojson = [];

	  for (child in data.profiles) {
	  	child = data.profiles[child];

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
	  	
	  	if (child.guardian_fname) {
				description += child.guardian_fname + ' ' + child.guardian_lname + ' ';
	  	}

	  	if (child.siblings_in_project) {
				description += child.siblings_in_project;
	  	}

	  	var marker_color;
	  	if (child.is_active) {
	  		marker_color = '#fc4353';
	  	}
	  	else {
	  		marker_color = '#808080';
	  		description += '(inactive)'
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
					'marker-color': marker_color,
					'marker-size': 'large',
					'marker-symbol': 'building'
				}
			};

			geojson.push(child_geo);
	  }

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
	})
  .fail(function() {
    $("#map").html("Error retrieving the children's profiles!").addClass("maperror animated1");
  });
});