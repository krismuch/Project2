function buildMetadata(sample) {

  // @TODO: Complete the following function that builds the metadata panel
  // Use `d3.json` to fetch the metadata for a sample
  // Call API to get the data
  d3.json(`/metadata/${sample}`).then((data) => {
   
    console.log(data)

    // Use d3 to select the panel with id of `#sample-metadata`
    // Select which element to display the sample
    var panel = d3.select("#sample-metadata");

    // Use `.html("") to clear any existing metadata
    panel.html("");
    
    
    // Use `Object.entries` to add each key and value pair to the panel
    // Hint: Inside the loop, you will need to use d3 to append new
    // tags for each key-value in the metadata.
      
    Object.entries(data).forEach(function([key, value]) {
      panel.append("h5").text(`${key}: ${value}`);
    });

    // BONUS: Build the Gauge Chart
    // buildGauge(data.WFREQ);
  });
}

function buildCharts(sample) {

  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(`/samples/${sample}`).then((sample_data) => {
   
    console.log(sample);

    var otu_ids = sample_data.otu_ids
    var sample_values = sample_data.sample_values
    var otu_labels = sample_data.otu_labels

    // @TODO: Build a Bubble Chart using the sample data
    
    var trace2 = {
      x: otu_ids,
      y: sample_values,
      mode: 'markers',
      marker: {
        size: sample_values,
        color: otu_ids,
        hovertext: otu_labels,
        hoverinfo: "hovertext"
      }
    };
    
    var data = [trace2];
    
    var layout = {
      title: 'Bubbles',
      showlegend: false,
      height: 400,
      width: 1600
    };
    
    Plotly.newPlot("bubble", data, layout);

    // @TODO: Build a Pie Chart
    values = sample_values.slice(0, 10);
    labels =  otu_ids.slice(0, 10);
    hovertext = otu_labels.slice(0, 10);
    console.log(values);
    console.log(labels);
    console.log(hovertext);

    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
  
   var trace1 = {
    values: sample_values.slice(0, 10),
    labels: otu_ids.slice(0, 10),
    hovertext: otu_labels.slice(0, 10),   
    hoverinfo: "hovertext", 
    type: 'pie'
};

var data = [trace1];

var layout = {
  title: "Pie Chart",
};

Plotly.newPlot("pie", data, layout);

  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    buildCharts(firstSample);
    buildMetadata(firstSample);

  });
}

function optionChanged(newSample) {
  // Fetch new data each time a new sample is selected
  buildCharts(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
