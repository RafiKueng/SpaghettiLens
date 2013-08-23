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

  var def = Ruler2.def;
  var scale = LMT.settings.display.zoompan.scale;
  var pxScale = LMT.model.Parameters.pxScale || 0.01;
  var arcsec = this.r * pxScale;
  var txtx = this.x + def.txt_dx / scale;

  this.mid = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.mid.setAttribute("id", "ruler_mid_" + this.idnr);
  this.mid.setAttribute("class", "ruler mid");
  this.mid.setAttribute("r", def.r_mid / scale);
  this.mid.setAttribute("cx", this.x);
  this.mid.setAttribute("cy", this.y);
  this.mid.jsObj = this;

  this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  this.circle.setAttribute("id", "ruler_circ_" + this.idnr);
  this.circle.setAttribute("class", "ruler circ");
  this.circle.setAttribute("r", 0);
  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
  this.circle.jsObj = this;
  
  this.text = document.createElementNS("http://www.w3.org/2000/svg", "text");
  this.text.setAttribute("id", "ruler_txt_" + this.idnr);
  this.text.setAttribute("class", "ruler text");
  this.text.setAttribute("x", txtx);
  this.text.setAttribute("y", this.y);
  this.text.setAttribute("font-size", def.txt_size / scale);
  this.text.setAttribute("stroke-width", def.txt_stroke / scale);
  
  //this.textnode1 = document.createTextNode(' ');
  //this.text.appendChild(this.textnode1);
  
  this.tspan1 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
  this.tspan1.setAttribute("id", "ruler_tspan1_" + this.idnr);
  this.tspan1.setAttribute("x", txtx);
  this.tspan1.setAttribute("dy", '0em');
  this.textnode1 = document.createTextNode('Radius:');
  this.tspan1.appendChild(this.textnode1);

  this.tspan2 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
  this.tspan2.setAttribute("id", "ruler_tspan2_" + this.idnr);
  this.tspan2.setAttribute("x", txtx);
  this.tspan2.setAttribute("dy", '1em');
  this.textnode2 = document.createTextNode('pixels: ');
  this.tspan2.appendChild(this.textnode2);

  this.tspan3 = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
  this.tspan3.setAttribute("id", "ruler_tspan2_" + this.idnr);
  this.tspan3.setAttribute("x", txtx);
  this.tspan3.setAttribute("dy", '1em');
  this.textnode3 = document.createTextNode('~ arcsec: ');
  this.tspan3.appendChild(this.textnode3);

  
  this.text.appendChild(this.tspan1);
  this.text.appendChild(this.tspan2);
  this.text.appendChild(this.tspan3);

	LMT.ui.svg.layer.rulers.appendChild(this.mid);
  LMT.ui.svg.layer.rulers.appendChild(this.circle);
  LMT.ui.svg.layer.rulers.appendChild(this.text);
}


/**
 * 
 */
Ruler2.prototype.updateSVG = function() {

  var def = Ruler2.def;
  var scale = LMT.settings.display.zoompan.scale;
  var pxScale = LMT.model.Parameters.pxScale || 0.01;
  var arcsec = this.r * pxScale;
  var txtx = this.x + def.txt_dx / scale;

	this.circle.setAttribute("r", this.r);
	this.circle.setAttribute("stroke-width", def.circle_stroke / scale);
	
	this.text.setAttribute("stroke-width", def.txt_stroke / scale);
  this.text.setAttribute("font-size", def.txt_size / scale);
  
  this.textnode2.nodeValue = 'pixels: ' + this.r.toFixed(2);
  this.textnode3.nodeValue = '~ arcsec: ' + arcsec.toFixed(2);
}



Ruler2.prototype.deleteSVG = function() {
	LMT.ui.svg.layer.rulers.removeChild(this.mid);
  LMT.ui.svg.layer.rulers.removeChild(this.circle);
  LMT.ui.svg.layer.rulers.removeChild(this.text);
	this.mid = null;
	this.circle = null;
	this.text = null;
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
/*
Ruler2.r_def = {mid: 7, handle: 5, r: 50}; //default radii of mid section and handle (before scaling)
Ruler2.strokeWidth_def = 1.5;
Ruler2.def_text = {stroke:0.75, size:15, dx:8};
*/
Ruler2.def = {
  r_mid: 7,
  r_handle: 5,
  r_circle: 50,
  circle_stroke: 1.5,
  txt_stroke: 0.75,
  txt_size: 15,
  txt_dx: 8,
}



LMT.objects.Ruler2 = Ruler2;
/*})();*/