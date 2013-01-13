/****************************
 * Main file
 * 
 *****************************/

// this is the root namespace of my application
var LMT = {};

//create namespaces
LMT.ui = {
  html: {},       // all the html based interactions
  svg: {},        // all that happens on the svg moddeling layer (input)
  output: {},     // takes care of displaying the results
  };
LMT.objects = {}; // collection of all objects available
LMT.comm = {};    // all the communication routines (websocket)
LMT.utils = {};   // some utils




function onBodyInit() {

  log = new LMT.utils.logger();
  log.write('init complete');

  /*
  var ep = new LMT.objects.ExtremalPoint(5);
  ep.write();
  */
}