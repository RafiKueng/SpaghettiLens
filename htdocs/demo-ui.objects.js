/*
demo-ui.objects.js script file

contains all the objects and definitions
*/

/*****************************************************************************
 Point
 represents an extremalpoint

 x,y:    abs. coordinates
 dx, dy  rel coordinates
 dr, dphi  rel coordinates in complex

 type
 isRoot
 isExpanded

 parent
 sibling
 child1
 child2

 ******************************************************************************/
function Point(x, y, parent) {
	this.x = parseInt(x) || 0;
	this.y = parseInt(y) || 0;

	if (parent) {
		this.parent = parent;
		this.isRoot = false;
	} else {
		this.parent = null;
		this.isRoot = true;
	}
	this.update();

	/*
	 this.setType = function(type) {
	 this.type = type;
	 };

	 this.switchType = function() {
	 if (this.type!='sad') {
	 this.type = this.type=='min' ? 'max' : 'min';
	 }
	 };

	 this.getDistTo = function(pnt) {
	 var x = this.x-pnt.x;
	 var y = this.y-pnt.y;

	 return Math.sqrt(x*x + y*y);
	 };

	 this.getRelCoordTo = function(pnt) {
	 var pnt = new Point( pnt.x-this.x, pnt.y - this.y);
	 pnt.setType(this.type);
	 return pnt;
	 };

	 this.getAngleTo = function (pnt) {
	 var dx = this.x-pnt.x;
	 var dy = this.y-pnt.y;
	 return Math.atan2(dy, dx);
	 }

	 this.toString = function() {
	 var txt = "[x:" + this.x + " y:" + this.y + "]";
	 return txt;
	 };
	 */
}

Point.prototype.update = function() {
	if (this.parent) {
		this.dx = this.parent.x - this.x;
		this.dy = this.parent.y - this.y;
		this.dr = Math.sqrt(this.dx * this.dx + this.dy * this.dy);
		this.dphi = Math.atan2(this.dy, this.dx);
	}
}
/*
 (setter) update the coordinates of a point
 */
Point.prototype.setCoord = function(x, y) {
	this.x = x;
	this.y = y;
	this.update();
}

Point.prototype.setType = function(type) {
	this.type = type;
};

Point.prototype.getRelCoordTo = function(pnt) {
	var pnt = new Point(pnt.x - this.x, pnt.y - this.y);
	pnt.setType(this.type);
	return pnt;
}
/*
 sets the relations ship to other points and updates them to if possible..
 */
Point.prototype.setRelationship = function(parent, sibling, child1, child2) {
	if (parent) {
		this.parent = parent;
		this.isRoot = false;
	} else if (this.parent) {
	} else {
		this.parent = null;
		this.isRoot = true;
	}

	if (sibling) {
		this.sibling = sibling;
		sibling.sibling = this;
	}

	if (chil1 && child2) {
		this.child1 = child1;
		this.child2 = child2;
		child1.sibling = child2;
		child2.sibling = child1;
		child1.parent = this;
		child2.parent = this;
	}

	this.update();
}

Point.prototype.paint = function() {

	if (!this.circle) {
		this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
		this.circle.setAttribute("id", "point"+pointnr);
		this.circle.setAttribute("r",  10);
		this.circle.setAttribute("class", "extremalpoint_" + this.type);
		select.extremalPointsLayer.appendChild(this.circle);
	}

	this.circle.setAttribute("cx", this.x);
	this.circle.setAttribute("cy", this.y);
		
	//get rid of this later and use css for styling
	var color = "";
	if (this.type == "sad") {color="red";}
	else if (this.type == "min") {color="green";}
	else {color = "blue";}
	this.circle.setAttribute("fill", color);

	if (settings.paintContour) {
		if (!this.contour) {
			//create contour	
		}
		//update contour
	}
		
	if (settings.paintConnectingLines) {
		if (!this.line) {
			this.line = document.createElementNS("http://www.w3.org/2000/svg", "line");
			this.line.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
			select.connectiorLinesLayer.appendChild(this.line);
		}
	    line.setAttribute("x1", this.x);
	    line.setAttribute("y1", this.y);
	    line.setAttribute("x2", this.parent.x);
	    line.setAttribute("y2", this.parent.y);
	}
}

