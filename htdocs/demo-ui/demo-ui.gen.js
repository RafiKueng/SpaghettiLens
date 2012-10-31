/*
  demo-ui.gen.js script file
  
  some general routines that donät fit in to other js files
*/

/*
  global variables
*/
var dbg; //the logging device



/*
  general init function, is called, as soon as the document is loaded
  and the inital DOM is built
  [body onload]
*/
function onBodyInit() {
  initUI();
  
  //init the logging device
  dbg = new logger()
  dbg.init();
}




/*
this fnc saves the arguments attached to the url to an $_GET object
(similar to php)
*/
function initGetVars() {
  var parts = window.location.search.substr(1).split("&");
  var $_GET = {};
  for (var i = 0; i < parts.length; i++) {
      var temp = parts[i].split("=");
      $_GET[decodeURIComponent(temp[0])] = decodeURIComponent(temp[1]);
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