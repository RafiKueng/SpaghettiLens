/*
demo-ui.objects.js script file

contains all the objects and definitions
*/

/*****************************************************************************
 Point
 @class represents an extremalpoint

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

/**
 *	creates n new point 
 *	@constructor
 * 
 *	@param {Number} x the x coodrinate
 *  @param {Number} y the y coordinate
 * 	@param {Object} [parent=None] the parent object
 */
function Point(x, y, parent) {
	
	this.idnr = ++Point.counter;
	
  this.x = parseInt(x) || 0;
  this.y = parseInt(y) || 0;

  if (parent) {
    this.parent = parent;
    this.isRoot = false;
  }
  else {
    this.parent = null;
    this.isRoot = true;
  }
  this.isExpanded = false;
  //this.update();

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
	this.updateCoord();
	this.updateType();
	this.paint();
}

/**
 * repaint all children 
 */
Point.prototype.updateAll = function() {
	this.update();
	if(this.isExpanded){
		this.child1.updateAll();
		this.child2.updateAll();
	}
}

Point.prototype.updateCoord = function() {
  if (this.parent) {
    this.dx = this.parent.x - this.x;
    this.dy = this.parent.y - this.y;
    this.dr = Math.sqrt(this.dx * this.dx + this.dy * this.dy);
    this.dphi = Math.atan2(this.dy, this.dx);
  }
}


/**
 * updates the type of this points *children* (after moving)
 * recursive 
 */
Point.prototype.updateType = function() {
	
	if (!this.isExpanded) {return;}
	
  var c1 = this.child1;
  var c2 = this.child2;

  var dphi = Math.abs(c1.dphi - c2.dphi);
  var r1 = c1.dr;
  var r2 = c2.dr;

  dphi = dphi > Math.PI ? Math.PI * 2 - dphi : dphi;

	// check if close together, then the types should be different from each other
  if (dphi < model.MinMmaxSwitchAngle) {
    
	  var cng_grp = null;
	  var oth_grp = null;
	
	  if (r1 > r2) {
	    cng_grp = c2;
	    oth_grp = c1;
	  }
	  else {
	    cng_grp = c1;
	    oth_grp = c2;
	  }
    
    var newtype = (this.wasType == 'min' ? 'max' : 'min');
    
    if (cng_grp.isExpanded) { //if this point has children, we need to check them too
      cng_grp.wasType = newtype;
      cng_grp.updateType();
    }
    else {
      cng_grp.setType(newtype);
    }
    
    if (oth_grp.isExpanded) {
      oth_grp.wasType = this.wasType;
      oth_grp.updateType();
    }
    else {
      oth_grp.setType(this.wasType);
    }
  }

	// they are not close together, so both have the same type (same as this.wasType)
  else {
    if (c1.isExpanded) {
      c1.wasType = this.wasType;
      c1.updateType(); //recurse
    }
    else {
      c1.setType(this.wasType);
    }
    if (c2.isExpanded) {
      c2.wasType = this.wasType;
      c2.updateType();
    }
    else {
      c2.setType(this.wasType);
    }
  }
}


/**
 * (setter) update the coordinates of a point
 * @param {Number} x the x coord
 * @param {Number} y the y coord
 * 
 */
Point.prototype.setCoord = function(x, y) {
  this.x = x;
  this.y = y;
  this.updateCoord();
}

Point.prototype.setType = function(type) {
  this.type = type;
}

Point.prototype.setRoot = function(isRoot) {
	this.isRoot = isRoot;
} 

/**
 * returns the relative coordinates to pnt
 * (used for creation of correct order for modelling backend)
 */
Point.prototype.getRelCoordTo = function(pnt) {
  var pnt = new Point(pnt.x - this.x, pnt.y - this.y);
  pnt.setType(this.type);
  return pnt;
}

/**
 sets the relations ship to other points and updates them to if possible..
 */
Point.prototype.setRelationship = function(parent, sibling, child1, child2) {
  if (parent) {
    this.parent = parent;
    this.isRoot = false;
  }
  else if (this.parent) {
  }
  else {
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

/**
 *	sets the children of a point
 * and the childrens siblings flag to each other
 * flags the point as expanded
 * 
 * @param {Point} child1
 * @param {Point} child2
 */
Point.prototype.setChildren = function(child1, child2) {
  if (child1 && child2) {
    this.child1 = child1;
    this.child2 = child2;
    child1.sibling = child2;
    child2.sibling = child1;
    //child1.parent = this;
    //child2.parent = this;
    
    this.isExpanded = true;
  }
}


/**
 *	Delete self
 * (recursivly remove all assosiated svg elements)
 */
Point.prototype.removeSelf = function() {
	if (this.isExpanded){
		this.child1.removeSelf();
		this.child2.removeSelf();
		this.child1 = null;
		this.child2 = null;
		this.isExpanded = false;
	}
	if (this.contour) {	//remove contour
		
	}
	
	if (this.line) { //remove line
		select.connectiorLinesLayer.removeChild(this.line);
		this.line = null;
	}
	
	if (this.circle) { //remove the circle
		select.extremalPointsLayer.removeChild(this.circle);
		this.circle = null;
	}
}



/**
 * Paint updates the underlying svg objects and repaints it 
 */
Point.prototype.paint = function() {

  if (!this.circle) {
    this.circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    this.circle.setAttribute("id", "point" + this.idnr);
    this.circle.setAttribute("r", 10);
    select.extremalPointsLayer.appendChild(this.circle);
    this.circle.pnt = this;
  }

  this.circle.setAttribute("cx", this.x);
  this.circle.setAttribute("cy", this.y);
	this.circle.setAttribute("class", "extremalpoint_" + this.type);
	
  //TODO get rid of this later and use css for styling
  var color = "";
  if (this.type == "sad") {
    color = "red";
  }
  else if (this.type == "min") {
    color = "green";
  }
  else {
    color = "blue";
  }
  this.circle.setAttribute("fill", color);

	if (!this.isRoot) {
	  if (!this.contour) {
	    this.contour = new Contour(this) //create contour
	    this.contour.create();
	  }
	  this.contour.paint();
	}

  if (settings.paintConnectingLines && !this.isRoot) {
    if (!this.line) {
      this.line = document.createElementNS("http://www.w3.org/2000/svg", "line");
      this.line.setAttribute("style", "stroke:rgb(0,0,0);stroke-width:1");
      select.connectiorLinesLayer.appendChild(this.line);
    }
    this.line.setAttribute("x1", this.x);
    this.line.setAttribute("y1", this.y);
    this.line.setAttribute("x2", this.parent.x);
    this.line.setAttribute("y2", this.parent.y);
  }
}


// static vars
Point.counter = 0;
