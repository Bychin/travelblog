function initialize(post) {
    var locations = post.places;
    var map = new google.maps.Map(document.getElementById('map'+post.id), {
        mapTypeId: google.maps.MapTypeId.ROADMAP,
        scrollwheel: true
    });
    
    var infowindow = new google.maps.InfoWindow();
    var flightPlanCoordinates = [];
    var bounds = new google.maps.LatLngBounds();

    for (i = 0; i < locations.length; i++) {
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(locations[i][0], locations[i][1]),
            map: map
        });
        
        flightPlanCoordinates.push(marker.getPosition());
        bounds.extend(marker.position);

        google.maps.event.addListener(marker, 'click', (function(marker, i) {
            return function() {
                infowindow.setContent('place '+(i+1));
                infowindow.open(map, marker);
            }
        })(marker, i));
    }

    map.fitBounds(bounds);
    
    var flightPath = new google.maps.Polyline({
        map: map,
        path: flightPlanCoordinates,
        strokeColor: "#FF0000",
        strokeOpacity: 1.0,
        strokeWeight: 2
    });
}

google.maps.event.addDomListener(window, 'load', initialize);
