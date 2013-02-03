/*****************************************************************************
 Contour around an ExtremalPoint
 
 @class represents an contour with points and path

 ******************************************************************************/
/*(function() {*/


/**
 *	creates a new contour
 *	@constructor
 * 
 */
function Contour() {
	this.idnr = LMT.model.NrOf.Contours++;
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
			this.cpoints[i].init(this.idnr, this.extpnt);
		}
	}
}


/**
 * recursive update
 * there's nothing to update here in the js datastructre
 */
Contour.prototype.update = function() {

	this.cpoints[this.cpoints.length-1].update();

	
	for (var i =0; i<this.cpoints.length-1; ++i){ // do the last seperatly, because of angle check..
		this.cpoints[i].update();		
		// check if we need to change the order because the user messes up the contour points
		var dp1=this.cpoints[i].d_phi; 
		var dp2=this.cpoints[i+1].d_phi; 

		if (dp2-dp1 < 0) {
			var tmp = this.cpoints[i];
			this.cpoints[i] = this.cpoints[i+1];
			this.cpoints[i+1] = tmp;
		}		
		
		// check if 2 points close together, then delete one
		var d = LMT.utils.dist2(this.cpoints[i], this.cpoints[i+1]);
		if (d<3) {
		  //$.event.trigger("DeleteContourPoint");
			var rem = this.cpoints.splice(i,1);
			rem[0].remove();
			this.nContourPoints--;
		}
	}
	
}


/**
 * creates a new set of countpur points with default settings
 */
Contour.prototype.createCPs = function() {

	this.cpoints = new Array();
	var nPnts = LMT.settings.nPointsPerContour;
	var d_phi = Math.PI * 2 / nPnts;
	
	for (var i = 1; i < nPnts; i++) {
		var r_fac = Math.abs(i - nPnts / 2.) / (0.5 * nPnts); //gives a number 0..1
    r_fac = r_fac * 0.25 + 0.50; //makes the radi between 50% and 75% of dist to parent

		var cpnt = new LMT.objects.ContourPoint(r_fac, d_phi*i, this);
		cpnt.init(this.idnr, this.extpnt);
		cpnt.update();
		this.cpoints.push(cpnt);
		this.nContourPoints++;
	}
	this.createSVG();
}



Contour.prototype.doublicateCP = function(pnt) {
	var newCp = new LMT.objects.ContourPoint(pnt.r_fac, pnt.d_phi+0.1, this);
	newCp.init(this.idnr, this.extpnt);
	newCp.update();
	var i = this.cpoints.indexOf(pnt);
	this.cpoints.splice(i+1, 0, newCp);
	this.nContourPoints++;
}


/**
 *  
 */
Contour.prototype.createSVG = function() {
  this.path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  this.path.setAttribute("id", "cpath" + this.idnr);
  this.path.setAttribute("class", "contourpath");
  this.path.setAttribute("d", "M0,0");
  //this.path.setAttribute("style", "stroke: blue; fill: none; stroke-width: 1");

	LMT.ui.svg.layer.contourlines.appendChild(this.path);
}


Contour.prototype.updateSVG = function(pathstr) {
  this.path.setAttribute("d", pathstr);
}

Contour.prototype.deleteSVG = function() {
	LMT.ui.svg.layer.contourlines.removeChild(this.path);
	this.path = null;
}


/**
 * 
 */
Contour.prototype.paint = function() {
	
	var n = this.nContourPoints;
	var pathstr = "";
	
	//goto first pos (parent of this contours extr point)
	pathstr += "M" + this.extpnt.parent.x+","+ this.extpnt.parent.y+" ";
	
	
	//generate first control point
	//
	
	if (this.extpnt.parent.childrenInsideEachOther){
		//is this the outer or the inner point?
		if (LMT.utils.dist2(this.extpnt, this.extpnt.parent) < LMT.utils.dist2(this.extpnt.sibling, this.extpnt.parent)) {
			// inner
			
			var cp_first = {
				x: this.extpnt.parent.x + 0.4 * (this.extpnt.x - this.extpnt.parent.x),
				y: this.extpnt.parent.y + 0.4 * (this.extpnt.y - this.extpnt.parent.y)
			};
		  var cp_last = cp_first;
		}
		else {
			//outer
			// set helper point perpendicular to |extpnt, extpnt.parent|
			var dx = this.extpnt.x - this.extpnt.parent.x;
			var dy = this.extpnt.y - this.extpnt.parent.y;
			
			var cp_first = {
				x: this.extpnt.parent.x + 0.3 * dy,
				y: this.extpnt.parent.y - 0.3 * dx
			};
		  var cp_last = {
				x: this.extpnt.parent.x - 0.3 * dy,
				y: this.extpnt.parent.y + 0.3 * dx
			};
			
		}
	}
	else {
		var cp_first = {
			x: this.extpnt.parent.x - 0.2 * (this.extpnt.parent.x - this.cpoints[0].x),
			y: this.extpnt.parent.y - 0.2 * (this.extpnt.parent.y - this.cpoints[0].y)
		};
	  var cp_last = {
			x: this.extpnt.parent.x - 0.2 * (this.extpnt.parent.x - this.cpoints[n-1].x),
			y: this.extpnt.parent.y - 0.2 * (this.extpnt.parent.y - this.cpoints[n-1].y)
		};

	}


	
	pathstr += "C" + cp_first.x + "," + cp_first.y + " ";

	for (var i = 0; i<this.nContourPoints; i++){
		this.cpoints[i].paint();
		//pathstr += this.cpoints[i].getPathStr();
		
		// create helper points for bezier curve

		var that = this.cpoints[i];
		var prev = (i==0)   ? this.extpnt.parent : this.cpoints[i-1]; //implement cyclic array
		var next = (i==n-1) ? this.extpnt.parent : this.cpoints[i+1]; //implement cyclic array
		
		var cp = {
			x: that.x + 0.2 * (prev.x - next.x),
			y: that.y + 0.2 * (prev.y - next.y)
		}
		
		pathstr += "" + cp.x + "," + cp.y + " " + that.x + "," + that.y + " S";
	}
		
	//close path / last control point

	pathstr += "" + cp_last.x + "," + cp_last.y + " " + this.extpnt.parent.x + "," + this.extpnt.parent.y + " Z";
		
	

	
	if (!this.path){
		this.createSVG();
	}

	this.updateSVG(pathstr);

	
	if (LMT.settings.display.paintContours){
		this.path.setAttribute("class", "contourpath");
	}
	else {
		this.path.setAttribute("class", "invisible");
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
		cpoints: this.cpoints
	}
}




/*******************************************
 * static fncs
 ******************************************/


/**
 *  
 * @param {Object} obj
 */
Contour.createFromJSONObj = function(obj) {
	var c = new Contour();
	
	for (var key in obj){
		c[key] = obj[key];
	}
	
	if (c.cpoints){
		c.nContourPoints = c.cpoints.length;
	}
	
	// recreate path
	//c.createPathSVG();

	return c;
		
};






LMT.objects.Contour = Contour;
/*})();*/