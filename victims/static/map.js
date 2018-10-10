$(document).ready(function () {
    var brazil = [-14.23, -51.92];
    var map    = L.map('map').setView(brazil, 4);

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 13
    }).addTo(map);

    // TODO: Create markers and popups
});
