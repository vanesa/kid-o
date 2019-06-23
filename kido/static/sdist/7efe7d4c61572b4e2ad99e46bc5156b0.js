
$('#myModal').on('shown.bs.modal',function(){$('#myInput').focus()})
$(function(){$.getJSON("/api/child_profile/"+window.id,function(data){var child=data.profile[0];var description='lives here '
if(child.guardian_fname||child.siblings_in_project){description+='with ';}
if(child.guardian_fname){description+=child.guardian_fname+' '+child.guardian_lname+' ';}
if(child.siblings_in_project){description+=child.siblings_in_project;}
L.mapbox.accessToken='pk.eyJ1IjoidmFuZXNhIiwiYSI6ImYxOTAxOGI1NTBlOGJkMTdjZTRmNGVmNTg0NTUxMjFjIn0._G3yYtIvkPX1EC9QEkNB6Q';var map=L.mapbox.map('map','vanesa.e4c935ef');if(!child.longitude){map.setView([18.542769,-69.801216],15);}
else{map.setView([child.latitude,child.longitude],15);L.mapbox.featureLayer({type:'Feature',geometry:{type:'Point',coordinates:[child.longitude,child.latitude]},properties:{title:child.first_name+' '+child.last_name,description:description,'marker-size':'large','marker-color':'#BE9A6B','marker-symbol':'building',}}).addTo(map);}
map.scrollWheelZoom.disable();});});