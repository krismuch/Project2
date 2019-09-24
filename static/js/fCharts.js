FusionCharts.ready(function() {
    var x = 6;
    var minPercip = 2;
    var maxPercip = 8;
    var buffer = 1.2;
    var csatGauge = new FusionCharts({
        "type": "angulargauge",
        "renderAt": "dial",
        "width": "450",
        "height": "250",
        "dataFormat": "json",
        "dataSource": {
            // Chart Configuration
            "chart": {
                "caption": "Amount of Precipitation",
                "lowerLimit": "0",
                "upperLimit": maxPercip+minPercip,
                "showValue": "1",
                "numberSuffix": " inches",
                "theme": "fusion",
                "showToolTip": "0"
            },
            // Chart Data
            "colorRange": {
                "color": [{
                    "minValue": "0",
                    "maxValue": minPercip,
                    "code": "#F2726F"
                }, 
                {
                    "minValue": minPercip,
                    "maxValue": minPercip+buffer,
                    "code": "#FFC533"
                }, 
                {
                    "minValue": minPercip+buffer,
                    "maxValue": maxPercip-buffer,
                    "code": "#62B58F"
                },
                {
                    "minValue": maxPercip-buffer,
                    "maxValue": maxPercip,
                    "code": "#FFC533"
                },
                {
                    "minValue": maxPercip,
                    "maxValue": maxPercip+minPercip,
                    "code": "#F2726F"
                    //"code": "#62B58F"
                }]
            },
            "dials": {
                "dial": [{
                    "value": x
                }]
            }
        }
    });
    csatGauge.render();

    var y = 60;
    var tempMin = 20;

    var chartObj = new FusionCharts({
        type: 'thermometer',
        renderAt: 'meter',
        width: '240',
        height: '310',
        dataFormat: 'json',
        dataSource: {
            "chart": {
                "caption": "Temperature",
                "subcaption": " ",
                "lowerLimit": "-10",
                "upperLimit": "110",
                "decimals": "1",
                "numberSuffix": "°F",
                "showhovereffect": "1",
                "thmFillColor": "#008ee4",
                "showGaugeBorder": "1",
                "gaugeBorderColor": "#008ee4",
                "gaugeBorderThickness": "2",
                "gaugeBorderAlpha": "30",
                "thmOriginX": "100",
                "chartBottomMargin": "20",
                "valueFontColor": "#000000",
                "theme": "fusion"
            },
            "value": y,
            //All annotations are grouped under this element
            "annotations": {
                "showbelow": "0",
                "groups": [{
                    //Each group needs a unique ID
                    "id": "indicator",
                    "items": [
                        //Showing Annotation
                        {/*
                            "id": "background",
                            //Rectangle item
                            "type": "rectangle",
                            "alpha": "50",
                            "fillColor": "#AABBCC",
                            "x": "$gaugeEndX-40",
                            "tox": "$gaugeEndX",
                            "y": "$gaugeEndY+54",
                            "toy": "$gaugeEndY+72"
                        */}
                    ]
                }]
            },
        }/*,
        "events": {
            "rendered": function(evt, arg) {
                evt.sender.dataUpdate = setInterval(function() {
                    var value,
                        prevTemp = evt.sender.getData(),
                        mainTemp = (Math.random() * 10) * (-1),
                        diff = Math.abs(prevTemp - mainTemp);
                    diff = diff > 1 ? (Math.random() * 1) : diff;
                    if (mainTemp > prevTemp) {
                        value = prevTemp + diff;
                    } else {
                        value = prevTemp - diff;
                    }
                    evt.sender.feedData("&value=" + value);
                }, 3000);
                evt.sender.updateAnnotation = function(evtObj, argObj) {
                    var code,
                        chartObj = evtObj.sender,
                        val = chartObj.getData(),
                        annotations = chartObj.annotations;
                    if (val >= -4.5) {
                        code = "#00FF00";
                    } else if (val < -4.5 && val > -6) {
                        code = "#ff9900";
                    } else {
                        code = "#ff0000";
                    }
                    annotations.update("background", {
                        "fillColor": code
                    });
                };
            },
            'renderComplete': function(evt, arg) {
                evt.sender.updateAnnotation(evt, arg);
            },
            'realtimeUpdateComplete': function(evt, arg) {
                evt.sender.updateAnnotation(evt, arg);
            },
            'disposed': function(evt, arg) {
                clearInterval(evt.sender.dataUpdate);
            }
        }*/
    });
    chartObj.render();

});