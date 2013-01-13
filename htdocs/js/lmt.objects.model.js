/*
  this saves all the relevant modelling parameters with default values
  and corresponds to one state
  
  can be stringified and reparsed (for loading and saving)
*/

(function() {

function Model() {
	this.__type = "model"; //identifier for object type, used for json  

  this.NrOf = { // some counters
  	__type: "counters",
  	Sources:0,// how many sources are modelled? (equals the number of contour groups)
  	ExtremalPoints:0,
  	Contours:0,
  	ContourPoints:0
	};

  this.Sources = null; //this contains all the modeled sources (of length nSources)

  this.MinMmaxSwitchAngle = Math.PI / 3.; //limit angle between two children, when the children will switch to different type (min/min to min/max; max/max to min/max)
  
  //color and channel settings
  this.brightness = 0.5;
  this.contrast = 0.5;
  this.channels = [
  	//array of channel objects containing the options for each channel, like:
  	//TODO comment this out
  	{ short: 'K',
  		name: 'near IR',
  		color: new Color(255, 0, 0),
  		alpha: 1,
  		img_url: '',
  		//img_obj: null,
  		//ctx_data: null
  	}
  ]
  
  this.brightness = 0.5;
  this.contrast = 0.5;
}


Model.prototype.init = function() {
	if (this.Sources) {
		for (i = 0; i < this.Sources.length; ++i) {
			this.Sources[i].init();
		}
	}
	else {
		this.Sources = new Array();
	}
}

/**
 * updates the whole model
 */
Model.prototype.update = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].update();
	}
}


Model.prototype.paint = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].paint();
	}
}


Model.prototype.remove = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].collapse(false);
	}
}



/**
 * 
 */
Model.prototype.getStateAsString = function() {
	return JSON.stringify(this);
}





/***********************************************
 * Static methods
 ***********************************************/


/**
 * 
 */
Model.getModelFormJSONString = function(str) {
	
	// helper fnc to convert the json object to actual object
	var h_fnc = function(key, val) {
		if (val instanceof Array) {
			return val;
		}
		
		// list the keys of all anonymous objects here
		//else if (key == "NrOf") {return val;}
		else if (val && typeof(val) == "object") {
			switch (val.__type) {
				case "counters":
					return val;
					break; 
				case "extpnt":
					var p = Point.createFromJSONObj(val);
					return p;
					break;
				case "cpnt":
					var cp = ContourPoint.createFromJSONObj(val);
					return cp;
					break;
				case "contour":
					var c = Contour.createFromJSONObj(val);
					return c;
					break;
				case "model":
					var m = Model.createFromJSONObj(val);
					return m;
					break;
				default:
					alert("Invalid object in json string..");
			}
		}
		return val;
	}
	// END helper function
	
	var m = JSON.parse(str, h_fnc);	
	return m;
}


/**
 * 
 * @param {Object} obj
 */
Model.createFromJSONObj = function(obj) {
	var m = new Model();
	
	for (var key in obj){
		//var tmp = obj[key];
		m[key] = obj[key];
	}
	
	
	m.init();
	m.update();
	m.repaint();
	
	return m;
};



LMT.objects.Model = Model;
})();