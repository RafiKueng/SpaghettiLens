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
function ExtMass(x, y, r, phi, id) {
	this.idnr = id || ExtMass.n++;
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
  
  var scale = LMT.settings.display.zoompan.scale;
  var def = ExtMass.def;
  var txtx = this.x + def.txt_dx / scale;

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ext_mass_mid_" + this.idnr);
  this.mid.setAttribute("class", "ext_mass mid");
  this.mid.setAttribute("r", def.r_mid / scale);
  this.mid.jsObj = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ext_mass_circ_" + this.idnr);
  this.circle.setAttribute("class", "ext_mass circ");
  this.circle.setAttribute("r", this.r);
  this.circle.setAttribute("stroke-width", def.circle_stroke / scale);
  this.circle.jsObj = this;

  this.handle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.handle.setAttribute("id", "ext_mass_hand_" + this.idnr);
  this.handle.setAttribute("class", "ext_mass handle");
  this.handle.setAttribute("r", def.r_handle / scale);
  this.handle.jsObj = this;


  this.text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  this.text.setAttribute("id", "extmass_txt_" + this.idnr);
  this.text.setAttribute("class", "ext_mass text invisible");
  this.text.setAttribute("x", txtx);
  this.text.setAttribute("y", this.y);
  this.text.setAttribute("font-size", def.txt_size / scale);
  this.text.setAttribute("stroke-width", def.txt_stroke / scale);
  this.text.jsObj = this;
  
  //this.textnode1 = document.createTextNode(' ');
  //this.text.appendChild(this.textnode1);
  
  this.tspan1 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
  this.tspan1.setAttribute("id", "extmass_tspan1_" + this.idnr);
  this.tspan1.setAttribute("x", txtx);
  this.tspan1.setAttribute("dy", '0em');
  this.textnode1 = document.createTextNode('Mass (in units of Einsteinradius)');
  this.tspan1.appendChild(this.textnode1);
  this.tspan1.jsObj = this;

  this.tspan2 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
  this.tspan2.setAttribute("id", "extmass_tspan2_" + this.idnr);
  this.tspan2.setAttribute("x", txtx);
  this.tspan2.setAttribute("dy", '1em');
  this.textnode2 = document.createTextNode('pixels: ');
  this.tspan2.appendChild(this.textnode2);
  this.tspan2.jsObj = this;

  this.tspan3 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
  this.tspan3.setAttribute("id", "extmass_tspan2_" + this.idnr);
  this.tspan3.setAttribute("x", txtx);
  this.tspan3.setAttribute("dy", '1em');
  this.textnode3 = document.createTextNode('~ arcsec: ');
  this.tspan3.appendChild(this.textnode3);
  this.tspan3.jsObj = this;

  
  this.text.appendChild(this.tspan1);
  this.text.appendChild(this.tspan2);
  this.text.appendChild(this.tspan3);



  this.svglayer.appendChild(this.text);
	this.svglayer.appendChild(this.mid);
	this.svglayer.appendChild(this.circle);
  this.svglayer.appendChild(this.handle);
}


/**
 * 
 */
ExtMass.prototype.updateSVG = function() {
  
  var scale = LMT.settings.display.zoompan.scale;
  var def = ExtMass.def;
  var pxScale = LMT.model.Parameters.pxScale || 0.01;
  var arcsec = this.r * pxScale;
  var txtx = this.x + def.txt_dx / scale;
  
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);
	this.mid.setAttribute("r", def.r_mid / scale);

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
	this.circle.setAttribute("r", this.r);
  this.circle.setAttribute("stroke-width", def.circle_stroke / scale);

  this.handle.setAttribute("cx", this.hx);
  this.handle.setAttribute("cy", this.hy);  
  this.handle.setAttribute("r", def.r_handle / scale); 
  
  
  this.text.setAttribute("x", txtx);
  this.text.setAttribute("y", this.y);
  this.text.setAttribute("stroke-width", def.txt_stroke / scale);
  this.text.setAttribute("font-size", def.txt_size / scale);
  
  this.tspan1.setAttribute("x", txtx);
  this.tspan2.setAttribute("x", txtx);
  this.tspan3.setAttribute("x", txtx);

  
  this.textnode2.nodeValue = 'pixels: ' + this.r.toFixed(2);
  this.textnode3.nodeValue = '~ arcsec: ' + arcsec.toFixed(2);  
  
}



ExtMass.prototype.deleteSVG = function() {
	this.svglayer.removeChild(this.mid);
	this.svglayer.removeChild(this.circle);
	this.svglayer.removeChild(this.handle);
  this.svglayer.removeChild(this.text);
	this.mid = null;
	this.circle = null;
	this.handle = null;
  this.tspan1 = null;
  this.tspan2 = null;
  this.tspan3 = null;
  this.text = null;
	
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
	if (target.classList.contains("mid")) {
		this.x = coord.x;
		this.y = coord.y;
	}	
	else if (target.classList.contains("handle")) {
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

/*
ExtMass.r_def = {mid: 7, handle: 5, r: 50}; //default radii of mid section and handle (before scaling)
ExtMass.strokeWidth_def = 1.5;

ExtMass.def_text = {stroke:0.75, size:15, dx:8};
*/

ExtMass.def = {
  r_mid: 7,
  r_handle: 5,
  r_circle: 50,
  circle_stroke: 1.5,
  txt_stroke: 0.75,
  txt_size: 15,
  txt_dx: 8,
};

/**
 *  
 * @param {Object} obj
 */
ExtMass.createFromJSONObj = function(obj) {
	return new ExtMass(obj.x, obj.y, obj.r, obj.phi, obj.idnr);
};


ExtMass.n = 0;
LMT.objects.ExternalMass = ExtMass;