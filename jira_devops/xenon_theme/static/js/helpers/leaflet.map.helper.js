var map, requestedMarkerArray, excludedMarkerArray, myMarkerArray, groupMarkerArray, routesArray, requestedMarkers, myMarkers, groupMarkers, excludedMarkers, routesLines;
// Prepare marker icons
var myIcon = L.icon({
    iconUrl: '/static/images/marker-my.png'
});
var groupIcon = L.icon({
    iconUrl: '/static/images/marker-group.png'
});
var requestedIcon = L.icon({
    iconUrl: '/static/images/marker-selected.png'
});

function updateLeafletLayers() {
    try {
        reArrangeMarkers();
        requestedMarkers.clearLayers();
        myMarkers.clearLayers();
        groupMarkers.clearLayers();
        excludedMarkers.clearLayers();

        requestedMarkers.addLayers(requestedMarkerArray);
        myMarkers.addLayers(myMarkerArray);
        groupMarkers.addLayers(groupMarkerArray);
        excludedMarkers.addLayers(excludedMarkerArray);

        routesLines.clearLayers();
        reArrangeRoutes();
        routesLines.addLayer(L.layerGroup(routesArray));
    } catch (err) {
        //
    }
}

function reArrangeMarkers() {
    requestedMarkerArray = [];
    excludedMarkerArray = [];
    myMarkerArray = [];
    groupMarkerArray = [];
    try {
        angular.element($("#actrl")).scope().filteredMarkers.forEach(function (item) {
            // Storing backend id in marker.alt
            var marker = L.marker([item.lat, item.lng], {icon: groupIcon, alt: item.id}).on('click', function (a) {
                angular.element($("#actrl")).scope().selectPortal(a)
            });
            if (item.props[0]) {
                marker.options.icon = requestedIcon;
                requestedMarkerArray.push(marker);
            } else if (item.props[1]) {
                if (item.props[2]) {
                    marker.options.icon = myIcon;
                } else {
                    marker.options.icon = groupIcon;
                }
                excludedMarkerArray.push(marker);
            } else if (item.props[2]) {
                marker.options.icon = myIcon;
                myMarkerArray.push(marker);
            } else {
                groupMarkerArray.push(marker);
            }
        });
    } catch (err) {

    }
}

function reArrangeRoutes() {
    routesArray = [];
    try {
        angular.element($("#actrl")).scope().routes.forEach(function (item) {
            var line = L.polyline([item.start, item.end], {
                color: randomColor({
                    luminosity: 'bright',
                    hue: 'random'
                })
            });
            // .on('click', function (e) {
            // alert("test");
            // });
            routesArray.push(line);
        });
    } catch (err) {

    }
}

function updateExcludedMarkers() {
    angular.element($("#actrl")).scope().updateExcludedGeojson();
}

function updateRoutes() {
    angular.element($("#actrl")).scope().updateRoutesGeojson();
}

function getURLParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}