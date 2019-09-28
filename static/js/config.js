// API key
const API_KEY = "pk.eyJ1Ijoid2poYXRjaGVyIiwiYSI6ImNrMGVkaTU1YzBneWIzYnFoMXdjY3I1cjQifQ.ZASxjO9gPO3quTjvYWXAjQ";

var maxP = 8;
var minP = 2;
var precip = 6;
var minT = 30;
var pTemp = 40;

var counties = {};

var year_ = document.getElementById("year").innerHTML;
var month_ = document.getElementById("monthRange").value;