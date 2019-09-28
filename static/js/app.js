function buildMetadata(plant) {

    // @TODO: Complete the following function that builds the metadata panel
    // Use `d3.json` to fetch the metadata for a sample
    // Call API to get the data
    //d3.json(`/metadata/${plant}`).then((data) => {
    d3.json(`/metadata/${plant}`,(data) => {
        
        //console.log(data["min_temp_deg_f"]);
        maxP = data["max_precip_inches"]/12;
        minP = data["min_precip_inches"]/12;
        minT = data["min_temp_deg_f"];
        // Use d3 to select the panel with id of `#sample-metadata`
        // Select which element to display the sample
        var panel = d3.select("#detail");
        var pan = document.getElementById("image");
        // Use `.html("") to clear any existing metadata
        panel.html("");
        
        // Use `Object.entries` to add each key and value pair to the panel
        // Hint: Inside the loop, you will need to use d3 to append new
        // tags for each key-value in the metadata.
        var i = 0;
        Object.entries(data).forEach(function([key, value]) {
            if(i<6){
                panel.append("h5").text(`${key}: ${value}`);
            }
            if(i==6){
                console.log(value);
                pan.src = value;
            }
            i++;
        });
        FusionCharts.ready(drawCharts);
        colorUpdate();
    });
}  
  
function optionChanged(newPlant) {
// Fetch new data each time a new plant is selected
    buildMetadata(newPlant);
}

function updateWeather(){
    var year_ = document.getElementById("year").innerHTML;
    var month_ = document.getElementById("monthRange").value;
    getWeather(year_,month_);
    colorUpdate();
    //console.log(year_);
    //console.log(month_);
}

function getWeather(year_,month_){
    d3.json(`/weather/${year_}/${month_}`,(data) => {
        
        counties = {};
        //console.log(counties);
        //c.county, w.tmax, w.tmin, w.prcp, w.year, w.month
        //console.log(data);
        Object.entries(data).forEach(function(c){
            //console.log(c[1]);
            var d=[c[1][1],c[1][2],(c[1][3])];
            counties[c[1][0]] = d;
        });
        //console.log(counties);
        // Use d3 to select the panel with id of `#sample-metadata`
        // Select which element to display the sample
        /*var panel = d3.select("#detail");

        // Use `.html("") to clear any existing metadata
        panel.html("");
        
        // Use `Object.entries` to add each key and value pair to the panel
        // Hint: Inside the loop, you will need to use d3 to append new
        // tags for each key-value in the metadata.
        
        Object.entries(data).forEach(function([key, value]) {
            panel.append("h5").text(`${key}: ${value}`);
        });
        FusionCharts.ready(drawCharts);*/
    });
}
function init(){
    var selector = d3.select("#plantChoices");

    var y = document.getElementById("year").innerHTML;
    var m = document.getElementById("monthRange").value;
    /*d3.json("/plantchoices").then((sampleNames)=>{*/
    d3.json("/plantchoices",(sampleNames)=>{
        sampleNames.forEach((sample)=>{
            selector.append("option").text(sample).property("value",sample);
        });
        const firstSample = sampleNames[0];
        //buildCharts(firstSample);
        buildMetadata(firstSample);
    });
    getWeather(y,m);
}
init();