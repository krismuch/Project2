// Create our initial map object
// Set the longitude, latitude, and the starting zoom level
/*var myMap = L.map("map", {
    center: [35.120196, -79.723586],
    zoom: 7
});*/

// Add a tile layer (the background map image) to our map
// We use the addTo method to add objects to our map
/*L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
maxZoom: 18,
id: "mapbox.outdoors",
accessToken: API_KEY
}).addTo(myMap);*/

var myMap = L.map("map", {
    center: [35.120196, -79.723586],
    zoom: 7
});


L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
maxZoom: 18,
id: "mapbox.outdoors",
accessToken: API_KEY
}).addTo(myMap);

var link = "static/data/counties.geojson";
var selection = "";

function getColor(name){
    data = getStats(name);
    grade = 0;
    tmin = 20;
    tmax = 170;
    //console.log(data);
    if(data[1]>minT){
        if((data[1]>minT+tmin)&(data[1]<minT+tmax)){grade++;}
        if(data[1]>minT+tmax){grade--;}
    }
    else{grade--;}

    if((data[2]>minP)&(data[2]<maxP)){
        b = (maxP-minP)/6
        if((data[2]>minP+b)&(data[2]<maxP-b)){grade++;}
    }
    else if((data[2]<minP-(b/2))||(data[2]>maxP+b)){
        grade--;
        grade--;
        if(data[2]>maxP+minP+b){
            grade--;
        }
    }
    else{grade--;}
    if(grade>1){return "green";}
    if(grade>0){return "#66cc00";}
    if(grade>-1){return "orange";}
    if(grade<-1){return "red";}
    return "yellow";
}
// Grabbing our GeoJSON data..

function colorUpdate(){
    //console.log("colorUpdate");
    myMap.remove();
    myMap = L.map("map", {
        center: [35.120196, -79.723586],
        zoom: 7
    });
    L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
        attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
        maxZoom: 18,
        id: "mapbox.outdoors",
        accessToken: API_KEY
    }).addTo(myMap);

    d3.json(link, function(data) {
        temp = data.features.filter(a=>{return a.properties["STATE"]==37})
        L.geoJson(temp, {
            // Style each feature (in this case a neighborhood)
            style: function(feature) {
                return {
                    color: "white",
                    fillColor: feature.properties["NAME"]==selection?"blue":getColor(feature.properties["NAME"]),
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
                    /*if(feature.properties["NAME"]!=selection){
                        layer.setStyle({
                            fillColor: "blue"
                        })
                    }*/
                    //console.log(selection);
                },
                click: function(event) {
                    layer = event.target;
                    layer.setStyle({
                        fillColor:"blue"
                    });
                    if(selection!=feature.properties["NAME"]){
                        selection = feature.properties["NAME"];
                    }
                    else{
                        selection = "";
                    }
                    //console.log(selection);
                    var t = document.getElementById("activeCounty");
                    //console.log(t);
                    t.innerHTML = selection;
                    FusionCharts.ready(drawCharts);
                    colorUpdate();
                //map.fitBounds(event.target.getBounds());
                }
            });
            layer.bindPopup("<h1>"+feature.properties["NAME"]+"</h1>");
        
            }
        }).addTo(myMap);  
    });
}

function updateMap(){
    console.log("updating");

    d3.json(link, function(data) {
        temp = data.features.filter(a=>{return a.properties["STATE"]==37})
        L.geoJson(temp, {
            // Style each feature (in this case a neighborhood)
            style: function(feature) {
                return {
                    color: "white",
                    fillColor: feature.properties["NAME"]==selection?"blue":getColor(feature.properties["NAME"]),
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
                    /*if(feature.properties["NAME"]!=selection){
                        layer.setStyle({
                            fillColor: "blue"
                        })
                    }*/
                    //console.log(selection);
                },
                click: function(event) {
                    layer = event.target;
                    layer.setStyle({
                        fillColor:"blue"
                    });
                    if(selection!=feature.properties["NAME"]){
                        selection = feature.properties["NAME"];
                    }
                    else{
                        selection = "";
                    }
                    //console.log(selection);
                    var t = document.getElementById("activeCounty");
                    //console.log(t);
                    t.innerHTML = selection;
                    FusionCharts.ready(drawCharts);
                    colorUpdate();
                //map.fitBounds(event.target.getBounds());
                }
            });
            layer.bindPopup("<h1>"+feature.properties["NAME"]+"</h1>");
        
            }
        }).addTo(myMap);  
    });
    myMap.eachLayer(function(layer){
        console.log("layer",layer);
    });
}
updateMap();

function getStats(sel){
    //console.log(sel);
    //console.log(counties[sel]);
    if(sel==""){
        var max = 0;
        var min = 0;
        var p = 0;
        Object.keys(counties).forEach(function(key) {
            //console.log(max);
            max = max+counties[key][0];
            min = min+counties[key][1];
            p = p+counties[key][2];
        });
        //console.log(max);
        max = max/100;
        min = min/100;
        p = p/100;
        //console.log(max);
        var t = [max,min,p];
        //console.log("here");
        //console.log(t);
        return(t);
    }
    return (counties[sel]);
}