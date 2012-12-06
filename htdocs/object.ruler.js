/*
XXX.object.ruler class script file
*/



/*****************************************************************************
 represents a ruler
 
 @class ruler

 ******************************************************************************/



/**
 *	creates a new contour
 *	@constructor
 * 
 */
function Ruler(x, y, r, phi) {
	this.idnr = Ruler.n++;
	this.x = x;
	this.y = y;
	this.r = r || 50;
	this.phi = phi || Math.PI / 4;

	this.mid = null;
	this.circle = null;
	this.handle = null;

}


/**
 * 
 */
Ruler.prototype.init = function() {

}


/**
 * recursive update
 * update the coords of the handle
 */
Ruler.prototype.update = function() {
	this.hx = this.x + toRectX(this.phi, this.r);
	this.hy = this.y + toRectY(this.phi, this.r);
}



/**
 *  
 */
Ruler.prototype.createSVG = function() {

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ruler_mid_" + this.idnr);
  this.mid.setAttribute("class", "ruler_mid");
  this.mid.setAttribute("r", 7);
  this.mid.ruler = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ruler_circ_" + this.idnr);
  this.circle.setAttribute("class", "ruler_circ");
  this.circle.setAttribute("r", this.r);

  this.handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.handle.setAttribute("id", "ruler_hand_" + this.idnr);
  this.handle.setAttribute("class", "ruler_handle");
  this.handle.setAttribute("r", 5);
  this.handle.ruler = this;

	select.rulerLayer.appendChild(this.mid);
	select.rulerLayer.appendChild(this.circle);
	select.rulerLayer.appendChild(this.handle);
}


/**
 * 
 */
Ruler.prototype.updateSVG = function() {
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
	this.circle.setAttribute("r", this.r);

  this.handle.setAttribute("cx", this.hx);
  this.handle.setAttribute("cy", this.hy);  
}



Ruler.prototype.deleteSVG = function() {
	select.rulerLayer.removeChild(this.mid);
	select.rulerLayer.removeChild(this.circle);
	select.rulerLayer.removeChild(this.handle);
	this.mid = null;
	this.circle = null;
	this.handle = null;
}


/**
 * 
 */
Ruler.prototype.paint = function() {
	if (!this.mid){
		this.createSVG();
	}

	this.updateSVG();
}



/**
 * 
 */
Ruler.prototype.remove = function() {
	this.deleteSVG();
}


/**
 *	define json representation 
 */
Ruler.prototype.toJSON = function() {
	return {
		__type: "ruler",
		idnr: this.idnr,
		x: this.x,
		y: this.y,
		r: this.r,
		phi: this.phi,
	}
}



//static fncs

/**
 *  
 * @param {Object} obj
 */
Ruler.createFromJSONObj = function(obj) {
	return new Ruler(obj.idnr, obj.x, obj.y, obj.r, obj.phi);
};


Ruler.n = 0;