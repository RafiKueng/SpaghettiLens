/*****************************************************************************
 ContourPoints that form the contour around an ExtremalPoint
 
 @class represents an contour point

 ******************************************************************************/
/*(function() {*/


/**
 *	creates a new contourpoint
 *	@constructor
 * 
 */
function ContourPoint(r_fac, d_phi, parent) {
	this.idnr = LMT.model.NrOf.ContourPoints++;

	this.parent = parent;

	//constructor
	this.r_fac = r_fac;
	this.d_phi = (d_phi + 20*Math.PI ) % (2*Math.PI); // make sure its between [0 ... 2pi]

	//directly set with init
	this.c_idnr = -1; //the id of the contour this one belongs to
	this.extpnt = null;
	
	//indirectly set with init

	//svg object
  this.circle = null;
  this.inv_circle = null;
	
	this.layer = LMT.ui.svg.layer.contourpoints;
}



/**
 * 
 */
ContourPoint.prototype.init = function(c_idnr, extpnt, parent){
	this.c_idnr = c_idnr;
	this.extpnt = extpnt;
	this.parent = this.parent || parent;
}



/**
 * 
 */
ContourPoint.prototype.createSVG = function() {
	if (!this.circle){
		this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
	  this.circle.setAttribute("class", "contourpoint");
	  this.circle.setAttribute("id", "cpnt" + (this.idnr));

    this.inv_circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    this.inv_circle.setAttribute("class", "contourpoint, almostinvis");
    this.inv_circle.setAttribute("id", "cpnt_inv" + (this.idnr));

	  
    this.inv_circle.jsObj = this;
    this.layer.appendChild(this.inv_circle);

    this.circle.jsObj = this;
    this.layer.appendChild(this.circle);
	}
}

/**
 * 
 */
ContourPoint.prototype.updateSVG = function() {
  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
  this.circle.setAttribute("r", ContourPoint.r_def / LMT.settings.display.zoompan.scale);

  this.inv_circle.setAttribute("cx", this.x);
  this.inv_circle.setAttribute("cy", this.y);
  this.inv_circle.setAttribute("r", ContourPoint.r_inv_def / LMT.settings.display.zoompan.scale);
}


/**
 * 
 */
ContourPoint.prototype.deleteSVG = function() {
  this.layer.removeChild(this.circle);
  this.circle = null;
  this.layer.removeChild(this.inv_circle);
  this.inv_circle = null;
}



/**
 * 
 */
ContourPoint.prototype.remove = function() {
  this.deleteSVG();
}



/**
 * 
 */
ContourPoint.prototype.update = function() {

  var cp_ang = this.d_phi + this.extpnt.dphi;
  var cp_rad = this.r_fac * this.extpnt.dr;
  this.x = this.extpnt.x + LMT.utils.toRectX(cp_ang, cp_rad);
  this.y = this.extpnt.y + LMT.utils.toRectY(cp_ang, cp_rad);
}


/**
 * 
 */
ContourPoint.prototype.paint = function() {
	
  if (!this.circle) {
  	this.createSVG();
  }
  this.updateSVG();
  
  /*
  if (LMT.settings.display.paintContourPoints) {
    this.circle.classList.remove("invisible");
  }
  else {
    this.circle.classList.add("invisible");
  }
  */
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
	
	var r = LMT.utils.toPolarR(dx, dy);
	var phi = LMT.utils.toPolarAng(dx, dy);
	
	this.d_phi = phi - this.extpnt.dphi;
	this.d_phi = (this.d_phi >=0 && this.d_phi <= Math.PI*2) ? this.d_phi : (this.d_phi + 10*Math.PI) % (Math.PI*2); 
	this.r_fac = r / this.extpnt.dr;
} 


/**
 * 
 */
ContourPoint.prototype.move = function(coord) {
	this.updateCoord(coord.x, coord.y);
	LMT.model.update();
	LMT.model.paint();
} 




/**
 *	define json representation 
 */
ContourPoint.prototype.toJSON = function() {
	return {
		__type: "cpnt",
		idnr: this.idnr,
		r_fac: LMT.utils.round(this.r_fac,4),
		d_phi: LMT.utils.round(this.d_phi,4)
	}
}


/************************************
 * static fncs 
 ************************************/

ContourPoint.r_def = 3;
ContourPoint.r_inv_def = 6; //invisible catch area


/**
 * event handler
 *  
 */
ContourPoint.Doublicate = function(evt, jsObj){
  jsObj.parent.doublicateCP(jsObj); //actually, the contour takes care of the cp's
  $.event.trigger("UpdateRepaintModel");
}





/**
 * 
 * @param {Object} obj
 */
ContourPoint.createFromJSONObj = function(obj) {
	var cp = new ContourPoint();
	
	for (var key in obj){
		cp[key] = obj[key];
	}
	
	return cp;
		
};




LMT.objects.ContourPoint = ContourPoint;
/*})();*/
