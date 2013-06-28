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
function Ruler2(coords) {
	this.x = coords.x;
	this.y = coords.y;
	this.idnr = 0;
	this.mid = null;
	this.circle = null;
}


/**
 * 
 */
Ruler2.prototype.init = function() {

}


/**
 * recursive update
 * update the coords of the handle
 */
Ruler2.prototype.update = function() {
}



/**
 *  
 */
Ruler2.prototype.createSVG = function() {

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ruler_mid_" + this.idnr);
  this.mid.setAttribute("class", "ruler mid");
  this.mid.setAttribute("r", Ruler.r_def.mid / LMT.settings.display.zoompan.scale);
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);
  this.mid.setAttribute("r", Ruler.r_def.mid / LMT.settings.display.zoompan.scale);
  this.mid.jsObj = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ruler_circ_" + this.idnr);
  this.circle.setAttribute("class", "ruler circ");
  this.circle.setAttribute("r", 0);
  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
  this.circle.jsObj = this;

	LMT.ui.svg.layer.rulers.appendChild(this.mid);
	LMT.ui.svg.layer.rulers.appendChild(this.circle);
}


/**
 * 
 */
Ruler2.prototype.updateSVG = function() {

	this.circle.setAttribute("r", this.r);
	this.circle.setAttribute("stroke-width", Ruler2.strokeWidth_def / LMT.settings.display.zoompan.scale);
}



Ruler2.prototype.deleteSVG = function() {
	LMT.ui.svg.layer.rulers.removeChild(this.mid);
	LMT.ui.svg.layer.rulers.removeChild(this.circle);
	this.mid = null;
	this.circle = null;
}


/**
 * 
 */
Ruler2.prototype.paint = function() {
	if (!this.mid){
		this.createSVG();
	}

	this.updateSVG();
}



/**
 * 
 */
Ruler2.prototype.remove = function() {
	this.deleteSVG();
}


/**
 * increases the rulers size
 */
Ruler2.prototype.move = function(coord) {
	
	var dx = -this.x + coord.x;
	var dy = -this.y + coord.y;
	this.r = LMT.utils.toPolarR(dx,dy);
	this.phi = LMT.utils.toPolarAng(dx,dy);

	//this.update();
	this.paint();

}


//static fncs

Ruler2.r_def = {mid: 7, handle: 5, r: 50}; //default radii of mid section and handle (before scaling)
Ruler2.strokeWidth_def = 1.5;


LMT.objects.Ruler2 = Ruler2;
/*})();*/