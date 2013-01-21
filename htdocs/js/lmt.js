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
		paintContours: true,
		paintContourPoints: true,
		paintConnectingLines: false,
		
		// translation vector and scale for the canvas
		zoompan: {x:0, y:0, scale: 1}
	},
	
	nPointsPerContour: 4, //how many points does one contour initially have
	
	nUndoActions: 20, //how many actions can be undone?
	nRedoActions: 20, //same for redo
	
	
	tmp: 0
}

LMT.addEventListener = document.addEventListener;


function onBodyInit() {
}


$(document).ready(function(){

  log = new LMT.utils.logger();
  log.write('init complete');

  /*
  var ep = new LMT.objects.ExtremalPoint(5);
  ep.write();
  */
	LMT.ui.svg.init();
	LMT.ui.svg.initBG();
	LMT.ui.html.loadAllSVG();
	
	LMT.model = new Model();
	LMT.model.init();
	
	LMT.out = new LMT.ui.out();
	LMT.out.init();
	
	LMT.out.load(["img/demo-ch1.png", "img/demo-ch2.png","img/demo-ch3.png","img/demo-ch3.png","img/demo-ch3.png"]);
	
	
});



/*gets fires as soon as all button svg elements are loaded*/
$(document).on('loadedButtons', function(evt){

	//alert("loadedButtons was triggered:");
});



/* gets fires as soon as connection to server is established and infos for model are received*/
$(document).on('loadedModelData', function(){
	
});


/* gets fires as soon as the images for the model are loaded */
$(document).on('loadedModelData', function(){
	
});


/* gets fired as soon as everything is ready to be used */
$(document).on('AppReady', function(){
	
});