/*
  demo-ui.gen.js script file
  
  some general routines that don�t fit in to other js files
*/

/*
  global variables
*/
var dbg; //the logging device
var $_GET; //the passed (HTTP GET) arguments
var model;
var actionstack;

 
/*
  general init function, is called, as soon as the document is loaded
  and the inital DOM is built
  [body onload]
*/
function onBodyInit() {
  initUI();
  
  // init the references
	initRefs();
  
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
  // otherwise coose random 
  if (! $_GET.id) {
  	var tmp = Math.random() * $const.nImages;
    $_GET.id = Math.floor(tmp) + 1;
    alert("imageid in url is missing (add ?id=1 to url)\nusing random mode: "+$_GET.id);
  }
  
  getBGImageUrls($_GET.id);
  
  //init the model
  model = new Model();
  model.init();
  
  actionstack = new ActionStack();
  actionstack.push(model); //init commit of empty state
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


/*
  this saves all the settings of the programm, that are not relevant for the model
*/
var settings = {
  mode: 0, // the current operating mode: 0:img mode, 1: pointmass mode, 2: ruler mode

  paintContour: true,
  paintContourPoints: true,
  paintConnectingLines: true,

	nPointsPerContour: 8, //how many points does one contour initially have

	nUndoActions: 20, //how many actions can be undone?
	nRedoActions: 20, //same for redo

	tmp: 0
}

var $set = settings;

// some application constants
var constants = {
  
  // where to place the hilighter for the selected mode (mode = array index)
  highliter_pos: new Array(
    "translate(0,0)",
    "translate(-50,0)",
    "translate(-100,0)"),
  modeImg:   0,
  modeMass:  1,
  modeRuler: 2,
  
  nImages: 2, //how many images are on the server (dev feature of randomly selecting an image requires this)
  tmp: 0
}

//shortcut
var $const = constants;

//references to some objects that are often used (will be set on init)
var select = {
	svg: null, // the root svg element
	bg_canv: null, //the background canvas behind svg
	img_canv:null, //the imgae display canvas to the right
	
  connectiorLinesLayer: null,
  contourLinesLayer: null,
  contourPointsLayer: null,
  extremalPointsLayer: null,
  
  modehighlight: null, //this item / group highlights the selected mode in ui
  
  undoBtn: null,
  redoBtn: null,
  
  tmp: 0
}

var $sel = select;


function initRefs() {
	select.svg = document.getElementById("ui_svg");
	select.bg_canv = document.getElementById("ui_bg_canvas");
	select.img_canv = document.getElementById("ui_img_canvas");
	
  select.connectiorLinesLayer = document.getElementById("ConnectorLinesLayer");
  select.contourLinesLayer = document.getElementById("ContourLinesLayer");
  select.contourPointsLayer = document.getElementById("ContourPointsLayer");
  select.extremalPointsLayer = document.getElementById("ExtremalPointsLayer");
  
  select.modehighlight = document.getElementById("ui_modehighlight");
  
  select.undoBtn = document.getElementById("ui_btn_undo");
  select.redoBtn = document.getElementById("ui_btn_redo");
}
