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
function Contour(extpnt) {
	this.extpnt = extpnt;
	this.idnr = Contour.counter++;
	
	this.nContourPoints = 0;
	this.cpoints = new Array();
	
	this.path = null;
}

/**
 * 
 */
Contour.prototype.create = function() {
	
	var nPnts = settings.nPointsPerContour;
	var d_phi = Math.PI * 2 / nPnts;
	
	for (var i = 1; i < nPnts; i++) {
		var r_fac = Math.abs(i - nPnts / 2.) / (0.5 * nPnts); //gives a number 0..1
    r_fac = r_fac * 0.25 + 0.50; //makes the radi between 50% and 75% of dist to parent

		var cpnt = new ContourPoint(this.idnr, this.extpnt, r_fac, d_phi*i);
		cpnt.create();
		cpnt.update();
		this.cpoints.push(cpnt);
		this.nContourPoints++;
	}
	
  this.path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  this.path.setAttribute("id", "cpath" + this.idnr);
  this.path.setAttribute("class", "contourpath");
  this.path.setAttribute("d", "");
  this.path.setAttribute("style", "stroke: blue; fill: none; stroke-width: 1");

	select.contourLinesLayer.appendChild(this.path);
}


/**
 * 
 */
Contour.prototype.paint = function() {
	
	var pathstr = "";
	
	//goto first pos (parent of this contours extr point)
	pathstr += "M" + this.extpnt.parent.x+","+ this.extpnt.parent.y+" ";
	
	for (var i = 0; i<this.nContourPoints; i++){
		this.cpoints[i].update();
		this.cpoints[i].paint();
		pathstr += this.cpoints[i].getPathStr();
	}
	
	//close path
	pathstr += "Z";
	this.path.setAttribute("d", pathstr);
	
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
	select.contourLinesLayer.removeChild(this.path);
	this.path = null;
}


/**
 *	define json representation 
 */
Contour.prototype.toJSON = function() {
	return {
		id: "cnt",
		idnr: this.idnr,
		cpnts: this.cpoints
	}
}


Contour.counter = 0;