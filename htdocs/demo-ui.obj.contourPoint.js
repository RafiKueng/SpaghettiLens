/*
XXX.obj.ContourPoint.js script file
*/



/*****************************************************************************
 ContourPoints that form the contour around an ExtremalPoint
 
 @class represents an contour point

 ******************************************************************************/



/**
 *	creates a new contourpoint
 *	@constructor
 * 
 */
function ContourPoint(cidnr, extpnt, r_fac, d_phi) {
	this.idnr = ContourPoint.counter++;
	this.cidnr = cidnr;

	this.extpnt = extpnt;
	this.r_fac = r_fac;
	this.d_phi = d_phi;
	
	this.circle = null;
}


/**
 * 
 */
ContourPoint.prototype.create = function() {
	this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("class", "contourpoint");
  this.circle.setAttribute("r", 5);
  this.circle.setAttribute("fill", "black");
  this.circle.setAttribute("id", "cpnt" + (this.idnr));
  
  this.circle.pnt = this;
  select.contourPointsLayer.appendChild(this.circle);

	this.paint();	
}

/**
 * 
 */
ContourPoint.prototype.remove = function() {
  select.contourPointsLayer.removeChild(this.circle);
  this.circle = null;
}

/**
 * 
 */
ContourPoint.prototype.update = function() {

  var cp_ang = this.d_phi + this.extpnt.dphi;
  var cp_rad = this.r_fac * this.extpnt.dr;
  this.x = this.extpnt.x + toRectX(cp_ang, cp_rad);
  this.y = this.extpnt.y + toRectY(cp_ang, cp_rad);
}


/**
 * 
 */
ContourPoint.prototype.paint = function() {
	this.update();

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
  
  //TODO use better vraiant: css...
	if (settings.paintContourPoints) {
	  this.circle.setAttribute("r", 5);
	}
	else {
	  this.circle.setAttribute("r", 0);
	}  
}


/**
 * 
 */
ContourPoint.prototype.getPathStr = function() {
	//TODO add bezier curve here	
	return "L" + this.x + "," + this.y + " ";
} 


/**
 * 
 */
ContourPoint.prototype.updateCoord = function(x,y) {
	var dx = x - this.extpnt.x;
	var dy = y - this.extpnt.y;
	
	var r = toPolarR(dx, dy);
	var phi = toPolarAng(dx, dy);
	
	this.d_phi = phi - this.extpnt.dphi;
	this.r_fac = r / this.extpnt.dr;
} 



/**
 *	define json representation 
 */
ContourPoint.prototype.toJSON = function() {
	return {
		id: "cpn",
		idnr: this.idnr,
		r_fac: round(this.r_fac,4),
		d_phi: round(this.d_phi,4)
	}
}

ContourPoint.counter = 0;