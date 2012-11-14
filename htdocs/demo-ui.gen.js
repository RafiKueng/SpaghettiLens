/*
  demo-ui.gen.js script file
  
  some general routines that donät fit in to other js files
*/

/*
  global variables
*/
var dbg; //the logging device
var $_GET; //the passed (HTTP GET) arguments


/*
  general init function, is called, as soon as the document is loaded
  and the inital DOM is built
  [body onload]
*/
function onBodyInit() {
  initUI();
  
  // init the references
  select.modehighlight = document.getElementById("ui_modehighlight");
  
  
  //init the logging device
  dbg = new logger();
  dbg.init();
  
  initGetVars();
  var log = "got the following arguments: <br/>";
  for (var i =0; i < $_GET.nArgs; i++) {
    log += $_GET.array[i] + "<br/>";
  }
  dbg.write(log);
  
  //check if id supplied
  if (! $_GET.id) {
    alert("imageid in url is missing (add ?id=1 to url)");
  }
  
  getBGImageUrls($_GET.id);
}




/*
this fnc saves the arguments attached to the url to an $_GET object
(similar to php)
*/
function initGetVars() {
  var parts = window.location.search.substr(1).split("&");
  $_GET = {};
  $_GET['nArgs'] = parts.length;
  $_GET['array'] = new Array();

  for (var i = 0; i < parts.length; i++) {
      var temp = parts[i].split("=");
      $_GET[decodeURIComponent(temp[0])] = decodeURIComponent(temp[1]);
      $_GET['array'].push(parts[i]);
  }
}


/*
  provides central logging facility
*/
function logger () {

  this.init = function(){
    this.log = document.getElementById("debug.log");
  };
  
  this.write = function(txt) {
    this.log.innerHTML = txt;
  };
  
  this.append = function(txt) {
    this.log.innerHTML += (txt + '<br/>'); 
  };
  
  this.clear = function() {
    this.log.innerHTML = ""; 
  }
}



var settings = {
  mode: 0 // the current operating mode: 0:img mode, 1: pointmass mode, 2: ruler mode
  
}


// some application constants
var constants = {
  
  // where to place the hilighter for the selected mode (mode = array index)
  highliter_pos: new Array(
    "translate(0,652.3)",
    "translate(-50,652.3)",
    "translate(-112,652.3)"),
  modeImg:   0,
  modeMass:  1,
  modeRuler: 2
}

//references to some objects that are often used (will be set on init)
var select = {
  modehighlight: null
}