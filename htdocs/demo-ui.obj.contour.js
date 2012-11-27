/*
XXX.obj.Contourjs script file
*/



/*****************************************************************************
 Contour around an ExtremalPoint
 
 @class represents an contour with points and path

 ******************************************************************************/



/**
 *	creates a new contour
 *	@constructor
 * 
 */
function Contour() {
	this.idnr = model.NrOf.Contours++;
	this.nContourPoints = 0;

	this.extpnt = null;
	this.cpoints = null;
	
	this.path = null; //the svg path object
}


/**
 * 
 */
Contour.prototype.init = function(extpnt) {
	
	this.extpnt = extpnt;
	if (!this.cpoints) {
		this.createCPs();
	}
	else { //if the points are there, but this fn is called, that means they come from json and are not initialiesed
		for (var i =0; i<this.cpoints.length; ++i){
			this.cpoints[i].init();
		}
	}
}


/**
 * recursive update
 * there's nothing to update here in the js datastructre
 */
Contour.prototype.update = function() {
	for (var i =0; i<this.cpoints.length; ++i){
		this.cpoints[i].update();
	}
}


/**
 * creates a new set of countpur points with default settings
 */
Contour.prototype.createCPs = function() {

	this.cpoints = new Array();
	var nPnts = settings.nPointsPerContour;
	var d_phi = Math.PI * 2 / nPnts;
	
	for (var i = 1; i < nPnts; i++) {
		var r_fac = Math.abs(i - nPnts / 2.) / (0.5 * nPnts); //gives a number 0..1
    r_fac = r_fac * 0.25 + 0.50; //makes the radi between 50% and 75% of dist to parent

		var cpnt = new ContourPoint(r_fac, d_phi*i);
		cpnt.init(this.idnr, this.extpnt);
		cpnt.update();
		this.cpoints.push(cpnt);
		this.nContourPoints++;
	}
	this.createSVG();
}


/**
 *  
 */
Contour.prototype.createSVG = function() {
  this.path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  this.path.setAttribute("id", "cpath" + this.idnr);
  this.path.setAttribute("class", "contourpath");
  this.path.setAttribute("d", "");
  this.path.setAttribute("style", "stroke: blue; fill: none; stroke-width: 1");

	select.contourLinesLayer.appendChild(this.path);
}


Contour.prototype.updateSVG = function(pathstr) {
  this.path.setAttribute("d", pathstr);
}

Contour.prototype.deleteSVG = function() {
	select.contourLinesLayer.removeChild(this.path);
	this.path = null;
}


/**
 * 
 */
Contour.prototype.paint = function() {
	
	var pathstr = "";
	
	//goto first pos (parent of this contours extr point)
	pathstr += "M" + this.extpnt.parent.x+","+ this.extpnt.parent.y+" ";
	
	for (var i = 0; i<this.nContourPoints; i++){
		this.cpoints[i].paint();
		pathstr += this.cpoints[i].getPathStr();
	}
		
	pathstr += "Z"; //close path

	
	if (settings.paintContour && this.path) {
		this.updateSVG(pathstr);
	}
	else if (settings.paintContour && !this.path) {
		this.createSVG();
		this.updateSVG(pathstr);
	}
	else if (!settings.paintContour && this.path) {
		this.deleteSVG();
	}
	else if (!settings.paintContour && !this.path) {
		//nothing to do
	}
	else {
		alert("strange error in Contour.paint");
	}
	
	
	//TODO: better use css for formating and change class / name
	if (settings.paintContour){
		this.path.setAttribute("style", "stroke: blue; fill: none; stroke-width: 1");
	}
	else {
		this.path.setAttribute("style", "stroke: blue; fill: none; stroke-width: 0");
	}
}



/**
 * 
 */
Contour.prototype.remove = function() {
	while (this.cpoints.length>0){
		var elem = this.cpoints.shift();
		elem.remove();
	}
	this.deleteSVG();
}


/**
 *	define json representation 
 */
Contour.prototype.toJSON = function() {
/*
	var obj = {__type: "contour"};
	
	for (var key in this){ //filter out certain keys
		var i= key;
		if (key===undefined) {
			continue;
			} //prevents recursion
		switch (key) {
			case "path":
			case "":
				continue;
			default:
				obj[key] = this[key];
		}
	}	
	
	return obj;
*/	
	return {
		__type: "contour",
		idnr: this.idnr,
		cpnts: this.cpoints
	}
}



//static fncs

/**
 *  
 * @param {Object} obj
 */
Contour.createFromJSONObj = function(obj) {
	var c = new Contour();
	
	for (var key in obj){
		c[key] = obj[key];
	}
	
	// recreate path
	//c.createPathSVG();

	return c;
		
};
