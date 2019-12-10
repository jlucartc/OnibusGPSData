
var data = JSON.parse(document.getElementById("data").innerHTML);

console.log(data);


var layer = new L.StamenTileLayer("toner");
var map = new L.Map("mapid", {
    center: new L.LatLng(-3.747268,-38.575144),
    zoom: 14
});
map.addLayer(layer);

for(var i = 0; i < data.length; i++){

	var coords = data[i].raw.trim().split(";");
	if(!isNaN(data[i].raw.trim()[5])){
		coords[1] = coords[1].substring(0,coords[1].length-1);
		var marker = L.marker([parseFloat(coords[0]),parseFloat(coords[1])]).addTo(map);
		marker.bindPopup("<h3>"+data[i].device_id+"</h3><br><h5>"+coords[0]+","+coords[1]+"</h5>");
		console.log("ponto "+i+"adicionado");
	}
}

//var marker = L.marker([-3.717, -38.543]).addTo(map);
//marker.bindPopup("<b>Hello world!</b><br>I am a popup.");
