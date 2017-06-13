$(function() {
	$.getJSON("/api/child_profile/" + window.id, function (data) {

		var child = data.profile[0];

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

	  L.mapbox.accessToken = 'pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';
		var map = L.mapbox.map('map', 'vanesa.e4c935ef');
		
		if (!child.longitude) {
      map.setView([18.542769, -69.801216],15);
    }
    else{
      map.setView([child.latitude, child.longitude],15);
			L.mapbox.featureLayer({
			// this feature is in the GeoJSON format: see geojson.org
			// for the full specification
			type: 'Feature',
			geometry: {
			type: 'Point',
			// coordinates here are in longitude, latitude order because
			// x, y is the standard for GeoJSON and many formats
			coordinates: [child.longitude, child.latitude]},
			properties: {
				title: child.first_name + ' ' + child.last_name,
				description: description,
				// one can customize markers by adding simplestyle properties
				// https://www.mapbox.com/guides/an-open-platform/#simplestyle
				'marker-size': 'large',
				'marker-color': '#BE9A6B',
				'marker-symbol': 'building',
				}
			}).addTo(map);
    }
		// Disable the scroll Zoom
		map.scrollWheelZoom.disable();

	});
});