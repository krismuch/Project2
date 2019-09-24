function buildMetadata(plant) {

    // @TODO: Complete the following function that builds the metadata panel
    // Use `d3.json` to fetch the metadata for a sample
    // Call API to get the data
    //d3.json(`/metadata/${plant}`).then((data) => {
    d3.json(`/metadata/${plant}`,(data) => {
        
        console.log(data)

        // Use d3 to select the panel with id of `#sample-metadata`
        // Select which element to display the sample
        var panel = d3.select("#detail");

        // Use `.html("") to clear any existing metadata
        panel.html("");
        
        
        // Use `Object.entries` to add each key and value pair to the panel
        // Hint: Inside the loop, you will need to use d3 to append new
        // tags for each key-value in the metadata.
        
        Object.entries(data).forEach(function([key, value]) {
        panel.append("h5").text(`${key}: ${value}`);
        });
        
    });
}  
  
function optionChanged(newPlant) {
// Fetch new data each time a new plant is selected
    buildMetadata(newPlant);
}

function init(){
    var selector = d3.select("#plantChoices");

    /*d3.json("/plantchoices").then((sampleNames)=>{*/
    d3.json("/plantchoices",(sampleNames)=>{
        sampleNames.forEach((sample)=>{
            selector.append("option").text(sample).property("value",sample);
        });
        const firstSample = sampleNames[0];
        //buildCharts(firstSample);
        buildMetadata(firstSample);
    });
}
init();