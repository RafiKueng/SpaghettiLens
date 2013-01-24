/*
  this saves all the relevant modelling parameters with default values
  and corresponds to one state
  
  can be stringified and reparsed (for loading and saving)
*/

/*(function() {*/

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
  this.ExternalMasses = null;
  this.Rulers = null;

  this.MinMmaxSwitchAngle = Math.PI / 3.; //limit angle between two children, when the children will switch to different type (min/min to min/max; max/max to min/max)
  
  //color and channel settings
  /*
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
  */
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

  if (this.ExternalMasses) {
    for (i = 0; i < this.ExternalMasses.length; ++i) {
      this.ExternalMasses[i].init();
    }
  }
  else {
    this.ExternalMasses = new Array();
  }

  if (this.Rulers) {
    for (i = 0; i < this.Rulers.length; ++i) {
      this.Rulers[i].init();
    }
  }
  else {
    this.Rulers = new Array();
  }


}

/**
 * updates the whole model
 */
Model.prototype.update = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].update();
	}
  for (i = 0; i < this.ExternalMasses.length; ++i) {
    this.ExternalMasses[i].update();
  }
  for (i = 0; i < this.Rulers.length; ++i) {
    this.Rulers[i].update();
  }
}


Model.prototype.paint = function() {
	for (i = 0; i < this.Sources.length; ++i) {
		this.Sources[i].paint();
	}
  for (i = 0; i < this.ExternalMasses.length; ++i) {
    this.ExternalMasses[i].paint();
  }
  for (i = 0; i < this.Rulers.length; ++i) {
    this.Rulers[i].paint();
  }
}


Model.prototype.remove = function() {
	for (var i = this.Sources.length-1; i >= 0 ; i--) {
		this.Sources[i].collapse(false);
	}
  for (var i = this.ExternalMasses.length-1; i>=0 ; i--) {
    this.ExternalMasses[i].remove();
  }
  for (var i = this.Rulers.length-1; i>=0 ; i--) {
    this.Rulers[i].remove();
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
 * eventhandler:
 * creates a new roo minima for the current model 
 */
Model.CreateRootMinima = function(evt, coord){
  var model = LMT.model;
  var p = new ExtremalPoint(coord.x, coord.y);
  p.init();
  p.depth = 0;
  p.setType("min");
  p.update();
  model.NrOf.Sources++;
  model.Sources.push(p);
  model.paint();
}



/**
 * eventhandler:
 *  
 * @param {Object} evt
 */
Model.CreateRuler = function(evt, coord){
  var model = LMT.model;

  var newElem = new Ruler(coord.x, coord.y, 30);
  newElem.update();
  newElem.paint();

  model.Rulers.push(newElem);  
};


/**
 *eventhandler: 
 * creates a new external mass object
 * 
 * coord.x: x pos
 * coord.y: y pos
 */
Model.CreateExternalMass = function(evt, coord){
  var model = LMT.model;
    
  var newElem = new ExtMass(coord.x, coord.y, 30);
  newElem.update();
  newElem.paint();
  
  model.ExternalMasses.push(newElem);
}


/**
 * eventhandler:
 * removes an arbitrary helper object (external mass, ruler) 
 */
Model.RemoveObject = function(evt, jsObj){

  var arr;
  if (jsObj.constructor.name == "Ruler") {
    arr = LMT.model.Rulers;
  }
  else if (jsObj.constructor.name == "ExtMass") {
    arr = LMT.model.ExternalMasses;
  }
  else {
    return false;
  }
  for(var i = arr.length; i>=0; i--){
    if(arr[i]==jsObj){
      arr.splice(i,1);
      jsObj.remove();
      return true;
    }
  }
}


/**
 * does only a repaint, no ew coordinates are calculated 
 */
Model.Repaint = function(evt){
  LMT.model.paint();
}



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
					var p = ExtremalPoint.createFromJSONObj(val);
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
				case "ruler":
				  var r = LMT.objects.Ruler.createFromJSONObj(val);
				  return r;
				case "ext_mass":
				  var r = LMT.objects.ExternalMass.createFromJSONObj(val);
				  return r;
				  
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

	return m;
};



LMT.objects.Model = Model;
/*})();*/