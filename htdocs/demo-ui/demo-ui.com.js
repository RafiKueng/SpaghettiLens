/*
  this script contains all the communication routines

*/

function calculateModel() {
  //set cursor to busy
  //open socket
  //get points
  //send points
  //on message: statusreport -> update
  //            picture url -> load picture, close socket
  


  var onopen = function () {
    //dbg.write("Connected to " + wsuri);
    var points = getPoints();
    var serialised_points = JSON.stringify(points);
    sock.send(serialised_points);
    //dbg.write("Sent: " + serialised_points);
  };
  var sock = openSocket(onopen, null, null);

}



var port = 8080;
var server_url = window.location.hostname;


function openSocket(onopen_fn, onclose_fn, onmessage_fn) {
  var wsuri;
  var sock;
  if (window.location.protocol === "file:") {
     wsuri = "ws://localhost:8080";
  } else {
     wsuri = "ws://" + server_url + ":" + port;
  }

  if ("WebSocket" in window) {
     sock = new WebSocket(wsuri);
  } else if ("MozWebSocket" in window) {
     sock = new MozWebSocket(wsuri);
  } else {
     alert("Browser does not support WebSocket!");
  }

  if (sock) {
     sock.onopen = onopen_fn;

     sock.onclose = function(e) {
        dgb.write("Connection closed (wasClean = " + e.wasClean + ", code = " + e.code + ", reason = '" + e.reason + "')");
        sock = null;
     }

     sock.onmessage = function(e) {
        dbg.write("Got echo: " + e.data);
     }
  }
  return sock;
}