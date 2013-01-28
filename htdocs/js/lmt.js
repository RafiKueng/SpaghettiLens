/****************************
 * Main file
 * 
 *****************************/

// this is the root namespace of my application
LMT = {};

//create namespaces
LMT.events = {};
LMT.ui = {
  html: {},       // all the html based interactions
  svg: {},        // all that happens on the svg moddeling layer (input)
  output: {},     // takes care of displaying the results
  };
LMT.objects = {}; // collection of all objects available
LMT.com = {};    // all the communication routines (websocket)
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



$(document).ready(function(){

  log = new LMT.utils.logger();
  log.write('init complete');



  LMT.events.startUp();
  LMT.events.assignHandlers();


  

  //for debug purposes, trigger some events manually


  var ch = [
    {r:1,g:0,b:0,contrast:1,brightness:0},
    {r:0,g:1,b:0,contrast:1,brightness:0},
    {r:0,g:0,b:1,contrast:1,brightness:0}
  ];
  var url = [
    "img/demo-ch1.png",
    "img/demo-ch2.png",
    "img/demo-ch3.png"
    ];
  LMT.modelData = {
    url: url,
    ch: ch
  };
  $.event.trigger('ReceivedModelData');

/*
  maybe switch to besser data structre like this
  modelData[i] = {
    short: 'K',
    name: 'near IR',
    color: {r:1, g:0, b:0},
    brightness: 0,
    contrast: 1;
    img_url: 'http:....',
  }
*/
  
  //----------------------  


  LMT.modelData.currentSimulationImageURLs = ["img/demo-ch1.png", "img/demo-ch2.png","img/demo-ch3.png","img/demo-ch3.png","img/demo-ch3.png"];
  $.event.trigger("ReceivedSimulation");  

  

	
});


