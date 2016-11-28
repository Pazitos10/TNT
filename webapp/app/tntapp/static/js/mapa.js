  //Las posiciones deberían venir desde la BD
  const DISTANCIA =150;
  const ZOOM = 15;
  const dit=new google.maps.LatLng(-43.2574009,-65.3077459);
  const aulas = new google.maps.LatLng(-43.251302, -65.307704);
  const center= new google.maps.LatLng(-43.2537476,-65.3093174);
  var marker;
  var map;
  function marcar(){
      var markerDit=new google.maps.Marker({
      position:dit,
      animation:google.maps.Animation.BOUNCE
    });
    var markerAulas=new google.maps.Marker({
      position:aulas,
      animation:google.maps.Animation.BOUNCE
    });
  markerDit.setMap(map);
  markerAulas.setMap(map);
    var radioDit = new google.maps.Circle({
      center:dit,
      radius:150, 
      strokeColor:"#0000FF",
      strokeOpacity:0.8,
      strokeWeight:2,
      fillColor:"#0000FF",
      fillOpacity:0.4
    });
    var radioAulas = new google.maps.Circle({
      center:aulas,
      radius:150, 
      strokeColor:"#0000FF",
      strokeOpacity:0.8,
      strokeWeight:2,
      fillColor:"#0000FF",
      fillOpacity:0.4
    });

  radioDit.setMap(map);
  radioAulas.setMap(map);
  }
  function initialize() {
    var mapProp = {
      center:center,
      zoom:ZOOM,
      mapTypeId:google.maps.MapTypeId.ROADMAP
    };
  map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
  marcar();

  
  }
function redibujar() {
  centro =new google.maps.LatLng(-43.2537476,-65.3093174);
  var mapProp = {
      center:centro,
      zoom:ZOOM,
      mapTypeId:google.maps.MapTypeId.ROADMAP
  };
  var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
  var center = map.getCenter();
  google.maps.event.trigger(map, "resize");
  map.setCenter(center); 
  marcar();
}
