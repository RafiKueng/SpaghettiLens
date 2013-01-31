/*
XXX.object.external_mass class script file
*/



/*****************************************************************************
 represents a external_mass
 
 @class external_mass

 ******************************************************************************/



/**
 *	creates a new contour
 *	@constructor
 * 
 */
function ExtMass(x, y, r, phi) {
	this.idnr = ExtMass.n++;
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
ExtMass.prototype.init = function() {

}


/**
 * recursive update
 * update the coords of the handle
 */
ExtMass.prototype.update = function() {
	this.hx = this.x + toRectX(this.phi, this.r);
	this.hy = this.y + toRectY(this.phi, this.r);
}



/**
 *  
 */
ExtMass.prototype.createSVG = function() {

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ext_mass_mid_" + this.idnr);
  this.mid.setAttribute("class", "ext_mass_mid");
  this.mid.setAttribute("r", 7);
  this.mid.extmass = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ext_mass_circ_" + this.idnr);
  this.circle.setAttribute("class", "ext_mass_circ");
  this.circle.setAttribute("r", this.r);

  this.handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.handle.setAttribute("id", "ext_mass_hand_" + this.idnr);
  this.handle.setAttribute("class", "ext_mass_handle");
  this.handle.setAttribute("r", 5);
  this.handle.extmass = this;

	select.massLayer.appendChild(this.mid);
	select.massLayer.appendChild(this.circle);
	select.massLayer.appendChild(this.handle);
}


/**
 * 
 */
ExtMass.prototype.updateSVG = function() {
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
	this.circle.setAttribute("r", this.r);

  this.handle.setAttribute("cx", this.hx);
  this.handle.setAttribute("cy", this.hy);  
}



ExtMass.prototype.deleteSVG = function() {
	select.massLayer.removeChild(this.mid);
	select.massLayer.removeChild(this.circle);
	select.massLayer.removeChild(this.handle);
	this.mid = null;
	this.circle = null;
	this.handle = null;
}


/**
 * 
 */
ExtMass.prototype.paint = function() {
	if (!this.mid){
		this.createSVG();
	}

	this.updateSVG();
}



/**
 * 
 */
ExtMass.prototype.remove = function() {
	this.deleteSVG();
}


/**
 *	define json representation 
 */
ExtMass.prototype.toJSON = function() {
	return {
		__type: "ext_mass",
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
ExtMass.createFromJSONObj = function(obj) {
	return new ExtMass(obj.idnr, obj.x, obj.y, obj.r, obj.phi);
};


ExtMass.n = 0;