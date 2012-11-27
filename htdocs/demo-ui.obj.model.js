/*
  this saves all the relevant modelling parameters with default values
  and corresponds to one state
  
  can be stringified and reparsed (for loading and saving)
*/
function Model() {
	//__type: "model", //identifier for object type, used for json  

  this.NrOf = { // some counters
  	Sources:0,// how many sources are modelled? (equals the number of contour groups)
  	ExtremalPoints:0,
  	Contours:0,
  	ContourPoints:0
	};

  this.Sources = new Array(); //this contains all the modeled sources (of length nSources)

  this.MinMmaxSwitchAngle = Math.PI / 3.; //limit angle between two children, when the children will switch to different type (min/min to min/max; max/max to min/max)
}


/**
 * updates the whole model
 */
Model.prototype.update = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].update();
	}
}


Model.prototype.repaint = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].paint();
	}
}


/**
 * 
 * @param {Object} obj
 */
Point.createFromJSONObj = function(obj) {
	var m = new Model();
	
	for (var key in obj){
		var tmp = obj[key];
		p[key] = obj[key];
	}
	
	m.update();
	
	return m;
		
};
