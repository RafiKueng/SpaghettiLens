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


LMT.settings = {
	mode: 'ruler',  // 'none'for doing nothing; 'image' for images; 'ruler' for adding rulers; 'mass' to add external masses 
	
	display: {
		Contours: true,
		paintContourPoints: true,
		paintConnectingLines: true,
		
		// translation vector and scale for the canvas
		zoompan: {x:0, y:0, scale: 1}
	},
	
	nPointsPerContour: 8, //how many points does one contour initially have
	
	nUndoActions: 20, //how many actions can be undone?
	nRedoActions: 20, //same for redo
	
	
	tmp: 0
}



function onBodyInit() {

  log = new LMT.utils.logger();
  log.write('init complete');

  /*
  var ep = new LMT.objects.ExtremalPoint(5);
  ep.write();
  */
	LMT.ui.svg.init();
	LMT.ui.svg.initBG();
}