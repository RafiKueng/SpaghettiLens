/*
  demo-ui.objects.js script file
  
  contains all the objects and definitions
*/


/*****************************************************************************
  Point
  represents an extremalpoint 
******************************************************************************/
function Point(x, y, parent) {
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
    this.dr = Math.sqrt( this.dx*this.dx + this.dy*this.dy );
    this.dphi = Math.atan2(this.dy, this.dx);
  }
}

Point.prototype.setCoord = function(x,y) {
  this.x = x;
  this.y = y;
  this.update();
}

Point.prototype.setType = function(type) {
  this.type = type;
}

Point.prototype.getRelCoordTo = function(pnt) {
  var pnt = new Point( pnt.x-this.x, pnt.y - this.y);
  pnt.setType(this.type);
  return pnt;
};