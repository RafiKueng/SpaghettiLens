/*****************************************************************************
 * LMT.object.ruler class script file
 * represents a ruler
 * 
 * @class ruler
 * 
 ******************************************************************************/
/*(function() {*/


/**
 *	creates a new contour
 *	@constructor
 * 
 */
function Ruler(x, y, r, phi, id) {
	this.idnr = id || Ruler.n++;
	this.x = x;
	this.y = y;
	this.r = r || Ruler.r_def.r / LMT.settings.display.zoompan.scale;
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
	this.hx = this.x + LMT.utils.toRectX(this.phi, this.r);
	this.hy = this.y + LMT.utils.toRectY(this.phi, this.r);
}



/**
 *  
 */
Ruler.prototype.createSVG = function() {

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ruler_mid_" + this.idnr);
  this.mid.setAttribute("class", "ruler_mid");
  this.mid.setAttribute("r", Ruler.r_def.mid / LMT.settings.display.zoompan.scale);
  this.mid.jsObj = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ruler_circ_" + this.idnr);
  this.circle.setAttribute("class", "ruler_circ");
  this.circle.setAttribute("r", this.r);

  this.handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.handle.setAttribute("id", "ruler_hand_" + this.idnr);
  this.handle.setAttribute("class", "ruler_handle");
  this.handle.setAttribute("r", Ruler.r_def.handle / LMT.settings.display.zoompan.scale);
  this.handle.jsObj = this;

	LMT.ui.svg.layer.rulers.appendChild(this.mid);
	LMT.ui.svg.layer.rulers.appendChild(this.circle);
	LMT.ui.svg.layer.rulers.appendChild(this.handle);
}


/**
 * 
 */
Ruler.prototype.updateSVG = function() {
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);
	this.mid.setAttribute("r", Ruler.r_def.mid / LMT.settings.display.zoompan.scale);

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
	this.circle.setAttribute("r", this.r);

  this.handle.setAttribute("cx", this.hx);
  this.handle.setAttribute("cy", this.hy);  
  this.handle.setAttribute("r", Ruler.r_def.handle / LMT.settings.display.zoompan.scale);  
}



Ruler.prototype.deleteSVG = function() {
	LMT.ui.svg.layer.rulers.removeChild(this.mid);
	LMT.ui.svg.layer.rulers.removeChild(this.circle);
	LMT.ui.svg.layer.rulers.removeChild(this.handle);
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
 * moves either the whole ruler, or only the handle (making the circle bigger)
 * depending on the target 
 */
Ruler.prototype.move = function(coord, target) {
	
	if (target.classList[0] == "ruler_mid") {
		this.x = coord.x;
		this.y = coord.y;
	}	
	else if (target.classList[0] == "ruler_handle") {
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

Ruler.n = 0; //counter
Ruler.r_def = {mid: 7, handle: 5, r: 50}; //default radii of mid section and handle (before scaling)

/**
 *  
 * @param {Object} obj
 */
Ruler.createFromJSONObj = function(obj) {
	return new Ruler(obj.x, obj.y, obj.r, obj.phi, obj.idnr);
};



LMT.objects.Ruler = Ruler;
/*})();*/