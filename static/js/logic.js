// Create our initial map object
// Set the longitude, latitude, and the starting zoom level
var myMap = L.map("map", {
    center: [35.120196, -79.723586],
    zoom: 7
});

// Add a tile layer (the background map image) to our map
// We use the addTo method to add objects to our map
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
maxZoom: 18,
id: "mapbox.outdoors",
accessToken: API_KEY
}).addTo(myMap);

var link = "static/data/counties.geojson";

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
    temp = data.features.filter(a=>{return a.properties["STATE"]==37})
    L.geoJson(temp, {
        // Style each feature (in this case a neighborhood)
        style: function(feature) {
            return {
                color: "white",
                fillColor: "blue",
                fillOpacity: 0.5,
                weight: 1.5
            };
        },
        // Called on each feature
        
        onEachFeature: function(feature, layer) {
          // Set mouse events to change map styling
          layer.on({
            mouseover: function(event) {
                layer = event.target;
                layer.setStyle({
                    fillOpacity: 0.9
                });
            },
            mouseout: function(event) {
                layer = event.target;
                layer.setStyle({
                    fillOpacity: 0.5
                });
            }/*,
            click: function(event) {
              map.fitBounds(event.target.getBounds());
            }*/
          });
          layer.bindPopup("<h1>"+feature.properties["STATE"]+"</h1>");
    
        }
    }).addTo(myMap);
  
});