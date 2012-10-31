/*
  this script contains all the buisiness intelligence

*/

var circ_id = 0; //position of the graphical element
var g1_id = 4; //position of the first child group
var g2_id = 5; //position of the second child group
var l_id = 1; //position of the connecting line
var p_id = 3; // position of the contour path
var cp_id = 2; // position of the contour path point group
var root_off = -3; //offset for the root node



var pointnr = 0;

function expandPoint(targetGroup) {
  
  var dx = 50;
  var dy = 50;
  
  //if (targentGroup.parentElement.class == "contourgroup") {
    //make custom dx, dy depending on the parent group
  //}
  var p1x = targetGroup.pnt.x + dx/(targetGroup.depth/3+1);
  var p2x = targetGroup.pnt.x - dx/(targetGroup.depth/3+1);
  var p1y = targetGroup.pnt.y + dy/(targetGroup.depth/3+1);
  var p2y = p1y;

  var point2 = createGroup(targetGroup, p1x, p1y, false);
  var point3 = createGroup(targetGroup, p2x, p2y, false);
  
  //targetGroup.getChildren()[0].setAttribute("type", "saddle");
  //targetGroup.getChildren()[0].setAttribute("fill", "yellow");
  
  targetGroup.appendChild(point2);
  targetGroup.appendChild(point3);
  targetGroup.isExpanded = true;  
  
  createContour(point2);
  createContour(point3);
  
  targetGroup.type = "sad";
  var circle = targetGroup.childNodes[circ_id];
  circle.setAttribute("fill", "red");
  circle.setAttribute("class", "extremalpoint_sad");
}

function collapsePoint(targetGroup) {
  var kids = targetGroup.childNodes;
  var i = targetGroup.isRoot ? root_off : 0; //compensate for root that has no line as child
  targetGroup.removeChild(kids[g2_id+i]);
  targetGroup.removeChild(kids[g1_id+i]);
  //targetGroup.removeChild(kids[1]);
  targetGroup.isExpanded=false;
  if (targetGroup.isRoot) {
    targetGroup.type = "min";
    var circle = targetGroup.childNodes[circ_id];
    circle.setAttribute("fill", "green");
    circle.setAttribute("class", "extremalpoint_"+targetGroup.type);
  }
  else {
    targetGroup.type = getOtherSiblingGrp(targetGroup).type;
    var circle = targetGroup.childNodes[circ_id];
    circle.setAttribute("fill", targetGroup.type=="min" ? "green" : "blue");
    circle.setAttribute("class", "extremalpoint_"+targetGroup.type);
  }
}

var ngroups=0;


function moveExtremalPoint(pnt, x, y) {
  var pGrp = pnt.parentElement; //parentGroup
  
  pnt.setAttribute("cx", x);
  pnt.setAttribute("cy", y);
  // pGrp.x = x;
  // pGrp.y = y;
  // pGrp.pnt.x = x;
  // pGrp.pnt.y = y;
  pGrp.pnt.update(x,y);
  
  
  //update debug lines and this contour
  if (!pGrp.isRoot) {
    var line = pnt.nextSibling;
    line.setAttribute("x1", x);
    line.setAttribute("y1", y);
    updateContourOf(pGrp);
  }
  
  if (pGrp.isExpanded) {
    var j = pGrp.isRoot ? g1_id+root_off : g1_id; //offset for root node, he has no line
    for (var i=0; i<2; i++) {
      var child = pGrp.childNodes[i+j];
      var line = child.childNodes[1];
      line.setAttribute("x2", x);
      line.setAttribute("y2", y);
      
      updateContourOf(child);
    }
  }
  
  //check for change of type of extremalpoint
  var oGrp = getOtherSiblingGrp(pGrp);
  if (pGrp.phi - oGrp.phi) {
  
  }

}



function createGroup(parent, x, y, isRoot) {
  
  // create svg objects and add svg attributes
  var group  = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("id", "grp"+ngroups);
  group.setAttribute("class", "contourgroup");
  group.type = "min";
  
  var point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  point.setAttribute("id", "point"+pointnr);
  // point.setAttribute("cx", x);
  // point.setAttribute("cy", y);
  point.setAttribute("r",  10);
  if (group.type == "min") {
    point.setAttribute("fill", "green");
    point.setAttribute("class", "extremalpoint_min");
  }
  else {
    point.setAttribute("fill", "blue");
    point.setAttribute("class", "extremalpoint_max");  
  }
  group.appendChild(point);

  //add debug helper lines
  if (!isRoot) {
    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x);
    line.setAttribute("y1", y);
    line.setAttribute("x2", parent.pnt.x);
    line.setAttribute("y2", parent.pnt.y);
    line.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
    group.appendChild(line);
  }

  
  // add js attributes
  
  // group.x = x;
  // group.y = y;
  // group.pnt = new Point(x,y);
  // group.r = 0; //distance to parent
  // group.phi = 0; //angle of parent
  group.isExpanded = false;
  group.isRoot = isRoot;
  
  if (isRoot) {
    group.depth = 0;
    group.type = "min";
    group.pnt = new Point(x,y, point);
  }
  else {
    group.depth = parent.depth+1;
    group.type = parent.type;
    group.pnt = new Point(x,y, point, parent.pnt); //parent can be null / unfedined
  }
  


  
  pointnr++;
  ngroups++;


  //parent.appendChild(group);
  return group;
  
}

var n_cp = 8; //number of contour points (including saddle point) per contour
var ncgroups = 0;
var cpnt_nr = 0;
var cpath_nr = 0;

function createContour(grp) {
  var parent = grp.parentElement;

  var dAng = Math.PI * 2 / n_cp;
  
  //var dx = grp.pnt.dx; //parent.x - grp.x;
  //var dy = grp.pnt.dx; //parent.y - grp.y;
  //var ang = toPolarAng(dx, dy);
  //var rad = toPolarR(dx, dy);
  var ang = grp.pnt.phi+Math.PI;
  var rad = grp.pnt.r;
  
  var cgrp = document.createElementNS("http://www.w3.org/2000/svg", "g");
  cgrp.setAttribute("id", "cgrp"+(ncgroups++));
  cgrp.setAttribute("class", "contourpoint_group");
  grp.appendChild(cgrp);
  
  for (var i = 1; i<n_cp; i++) { //no need to draw the first point
    var r_fac = Math.abs(i-n_cp/2.)/(0.5*n_cp); //gives a number 0..1
    r_fac = r_fac *0.25 + 0.50; //makes the radi between 50% and 75% of dist to parent
    var cp_ang = ang+i*dAng;
    var cp_rad = rad * r_fac;
    //TODO: this is a hack, switch to using the point objects here
    var cp_x = grp.pnt.x + toRectX(cp_ang, cp_rad);
    var cp_y = grp.pnt.y + toRectY(cp_ang, cp_rad);
    
    
    var point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    point.setAttribute("class", "contourpoint");
    point.setAttribute("cx", cp_x);
    point.setAttribute("cy", cp_y);
    point.setAttribute("r",  5);
    point.setAttribute("fill", "black");
    point.setAttribute("id", "cpnt"+(cpnt_nr++));
    
    point.ang = cp_ang;
    point.d_ang = i*dAng;
    point.rad = cp_rad;
    point.s_rad = r_fac;
    
    cgrp.appendChild(point);
    
  }
  var path = document.createElementNS("http://www.w3.org/2000/svg", "path");
  path.setAttribute("id", "cpath"+(cpath_nr++));
  path.setAttribute("class", "contourpath");
  path.setAttribute("d",  "");
  path.setAttribute("style", "stroke: blue; fill: none; stroke-width: 1");
  
  grp.appendChild(path);    
    
  updateContourOf(grp);
  
}

function updateContourOf(grp) {
  var pPnt = grp.parentElement.pnt;
  
  var dAng = Math.PI * 2 / n_cp;
  
  // var dx = parent.x - grp.x;
  // var dy = parent.y - grp.y;
  // var ang = toPolarAng(dx, dy);
  // var rad = toPolarR(dx, dy);
  var ang = grp.pnt.phi+Math.PI;
  var rad = grp.pnt.r;
  
  // var j = grp.isRoot ? 1 : 0; //offset for root node, he has no line
  var j = grp.isExtended ? 0 : 2; //if not expanded, then two groups are missing
  var contGrp = grp.childNodes[4-j];
  var path = grp.childNodes[5-j];
  var pathstr = "";
  
  pathstr += "M" + pPnt.x + "," + pPnt.y + " "; //move to start pos
  
  for (var i=0; i<contGrp.childNodes.length; i++) {
    var pnt = contGrp.childNodes[i];
    
    var cp_ang = ang + pnt.d_ang;
    var cp_rad = rad * pnt.s_rad;
    var cp_x = grp.pnt.x + toRectX(cp_ang, cp_rad);
    var cp_y = grp.pnt.y + toRectY(cp_ang, cp_rad);
    
    //var cp_x = grp.x + toRectX(pnt.ang, pnt.rad);
    //var cp_y = grp.y + toRectY(pnt.ang, pnt.rad);
    pnt.setAttribute("cx", cp_x);
    pnt.setAttribute("cy", cp_y);
    pathstr += "L"+cp_x + ","+cp_y+" ";
  }
  
  pathstr += "Z"; //close path
  path.setAttribute("d", pathstr);
}



//returns the other subgroup
function getOtherSiblingGrp(grp) {
  if (grp.nextSibling) {
    if (grp.nextSibling.id.substring(0,3)=="grp") {
      return grp.nextSibling;
    }
  }
  else if (grp.previousSibling) {
    if (grp.previousSibling.id.substring(0,3)=="grp") {
      return grp.previousSibling;
    }
  }
}

/* recursive function returning all the points coordinates for ONE source
 relative to origin
 origin is the max of the root group (or the point more close to the saddle
 point)
 the desired order is: (postorder)
  1. point futher away from saddlepoint
  2. point closer
  3. saddle point
*/
function getExtremaArray(grp, origin) {
  
  var res = new Array();
  if (grp.isExpanded) {

    var ps = grp.pnt;
    var j = (grp.isRoot) ? root_off : 0;
    var p1 = grp.childNodes[g1_id+j];
    var p2 = grp.childNodes[g2_id+j];
     
    dbg.append('point: '+grp.id+" "+ps.toString());
    dbg.append('point: '+p1.id+" "+p1.pnt.toString() );
    dbg.append('point: '+p2.id+" "+p2.pnt.toString() );
    
    
    // maintain postorder traversal, nodes sortet by distance
    // p1.pnt.r is distance p1 to ps
    if (p1.pnt.r < p2.pnt.r) {
      var tmp = p1;
      p1 = p2;
      p2 = tmp;
    }
    
    var skiporigin = false;
    if (origin==null) {
      origin = p2.pnt;
      skiporigin = true;
      var p2arr = getExtremaArray(p2, origin);
      res = res.concat(p2arr);
    }
    var p1arr = getExtremaArray(p1, origin);
    res = res.concat(p1arr);
    if (!skiporigin) { 
      var p2arr = getExtremaArray(p2, origin);
      res = res.concat(p2arr);
    }
    res = res.concat(new Array(ps.getRelCoordTo(origin)));
  }

  else {
    var pnt = null;
    if (origin==null) {
      pnt = SVGtoPoint(grp.childNodes[circ_id]);
    }
    else {
      pnt = SVGtoPoint(grp.childNodes[circ_id]);
      pnt = pnt.getRelCoordTo(origin);
    }
    res = Array(pnt);
  }
  
  return res;
  
}


/*
  this starts the recursive function to get all the points from all the sources
  TODO only gets the 1st source
*/
function getPoints() {
  var root = document.getElementById("layer2");
  var src1 = root.childNodes[0];
  dbg.clear();
  var res = new Array();
  if (src1) {
    var tmp = getExtremaArray(src1, null);
    res = res.concat(tmp);
  }
  
  return res;
  
}



/********************
 * math helper
 ********************/

function toPolarAng(xdiff,ydiff) {
   var direction = (Math.atan2(ydiff,xdiff));
   return(direction);
}

function toPolarR(xdiff,ydiff) {
   var distance = Math.sqrt(xdiff * xdiff + ydiff * ydiff);
   return(distance);
}
function toRectX(direction,distance) {
   var x = distance * Math.cos(direction);
   return(x);
}

function toRectY(direction,distance) {
   y = distance * Math.sin(direction);
   return(y);
}


/*
  Object, represents a point with
   .x, .y absolute cooridinates on canvas
   .dx, dy relative coordinates to parent
   .r .phi rel coords polar
   .parent reference to parent point object
   .svg link to the actual svg circle object representing this point
   
   and some helper functions
   
   doesn't need to have a parent, but then only .x and .y are set
*/
function Point(x, y, svg, parent) {
  //constructor
  
  // see http://stackoverflow.com/questions/148901/is-there-a-better-way-to-do-optional-function-parameters-in-javascript
  //this would be better, but that handling of default values I use here should be alright in our usecase
  this.x = parseInt(x) || 0;
  this.y = parseInt(y) || 0;
  
  this.parent = parent || null;
  this.svg = svg || null;
  
  this.updateRel();  
  this.updateSVG();
};
  
//methods for point object
//****************
  
  // internal update function. expects new x, y are already set
Point.prototype.updateRel = function () {
    if (this.parent) {
      var dx = this.x - this.parent.x;
      var dy = this.y - this.parent.y;
      
      this.dx = dx;
      this.dy = dy;
      this.r = Math.sqrt(dx*dx+dy*dy);
      this.phi = Math.atan2(dy,dx);
    }
    else {
      this.dx = null;
      this.dy = null;
      this.r = null;
      this.phi = null;
    }
  };
  
  //external update function, setting new abs coords
  // or updating structure, if no x, y are passed
Point.prototype.update = function (x,y) {
    this.x = x || this.x;
    this.y = y || this.y;
    this.updateRel();
    this.updateSVG();
  };

  // internal: this updates the bound svg opject
Point.prototype.updateSVG = function () {
    if (this.svg) {
      this.svg.setAttribute("cx",this.x);
      this.svg.setAttribute("cy",this.y);
    }
  };
  
  /*
  this.getDistTo = function(pnt) {
    var x = this.x-pnt.x;
    var y = this.y-pnt.y;
    
    return Math.sqrt(x*x + y*y);
  };
  */ 
  
Point.prototype.getRelCoordTo = function(pnt) {
    return new Point( this.x - pnt.x, this.y - pnt.y);
  };
  
Point.prototype.toString = function() {
    var txt = "[x:" + this.x + " y:" + this.y + "]";
    return txt;
  };


function SVGtoPoint(circle) {
  return new Point(circle.getAttribute("cx"), circle.getAttribute("cy"));
}
