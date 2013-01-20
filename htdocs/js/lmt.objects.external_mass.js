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
	this.r = r || ExtMass.r_def.r / LMT.settings.display.zoompan.scale;;
	this.phi = phi || Math.PI / 4;

	this.mid = null;
	this.circle = null;
	this.handle = null;
	
	this.svglayer = LMT.ui.svg.layer.masses;

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
	this.hx = this.x + LMT.utils.toRectX(this.phi, this.r);
	this.hy = this.y + LMT.utils.toRectY(this.phi, this.r);
}



/**
 *  
 */
ExtMass.prototype.createSVG = function() {

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ext_mass_mid_" + this.idnr);
  this.mid.setAttribute("class", "ext_mass_mid");
  this.mid.setAttribute("r", 7);
  this.mid.jsObj = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ext_mass_circ_" + this.idnr);
  this.circle.setAttribute("class", "ext_mass_circ");
  this.circle.setAttribute("r", this.r);

  this.handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.handle.setAttribute("id", "ext_mass_hand_" + this.idnr);
  this.handle.setAttribute("class", "ext_mass_handle");
  this.handle.setAttribute("r", 5);
  this.handle.jsObj = this;

	this.svglayer.appendChild(this.mid);
	this.svglayer.appendChild(this.circle);
	this.svglayer.appendChild(this.handle);
}


/**
 * 
 */
ExtMass.prototype.updateSVG = function() {
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);
	this.mid.setAttribute("r", ExtMass.r_def.mid / LMT.settings.display.zoompan.scale);

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
	this.circle.setAttribute("r", this.r);

  this.handle.setAttribute("cx", this.hx);
  this.handle.setAttribute("cy", this.hy);  
  this.handle.setAttribute("r", ExtMass.r_def.handle / LMT.settings.display.zoompan.scale); 
}



ExtMass.prototype.deleteSVG = function() {
	this.svglayer.removeChild(this.mid);
	this.svglayer.removeChild(this.circle);
	this.svglayer.removeChild(this.handle);
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
 * moves either the whole ruler, or only the handle (making the circle bigger)
 * depending on the target 
 */
ExtMass.prototype.move = function(coord, target) {
	if (target.classList[0] == "ext_mass_mid") {
		this.x = coord.x;
		this.y = coord.y;
	}	
	else if (target.classList[0] == "ext_mass_handle") {
		var dx = -this.x + coord.x;
		var dy = -this.y + coord.y;
		this.r = LMT.utils.toPolarR(dx,dy);
		this.phi = LMT.utils.toPolarAng(dx,dy);
	}
	else {
		//alert('sould not happen in moveRuler');
		//return
	}

	this.update();
	this.paint();
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


ExtMass.n = 0; //counter
ExtMass.r_def = {mid: 7, handle: 5, r: 50}; //default radii of mid section and handle (before scaling)

/**
 *  
 * @param {Object} obj
 */
ExtMass.createFromJSONObj = function(obj) {
	return new ExtMass(obj.idnr, obj.x, obj.y, obj.r, obj.phi);
};


ExtMass.n = 0;