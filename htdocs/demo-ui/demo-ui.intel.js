/*
  this script contains all the buisiness intelligence

*/

function onBodyInit() {
  initUI();
}


var pointnr = 0;

function expandPoint(targetGroup) {
  
  var dx = 50;
  var dy = 50;
  
  //if (targentGroup.parentElement.class == "contourgroup") {
    //make custom dx, dy depending on the parent group
  //}
  var p1x = targetGroup.x + dx/(targetGroup.depth/3+1);
  var p2x = targetGroup.x - dx/(targetGroup.depth/3+1);
  var p1y = targetGroup.y + dy/(targetGroup.depth/3+1);
  var p2y = p1y;

  var point2 = createGroup(targetGroup, p1x, p1y, false);
  var point3 = createGroup(targetGroup, p2x, p2y, false);
  
  //targetGroup.getChildren()[0].setAttribute("type", "saddle");
  //targetGroup.getChildren()[0].setAttribute("fill", "yellow");
  
  targetGroup.appendChild(point2);
  targetGroup.appendChild(point3);
  targetGroup.isExpanded = true;  
  
  createContour(point2);
  

}

function collapsePoint(targetGroup) {
  var kids = targetGroup.childNodes;
  var i = targetGroup.isRoot ? 1 : 0; //compensate for root that has no line as child
  targetGroup.removeChild(kids[3-i]);
  targetGroup.removeChild(kids[2-i]);
  //targetGroup.removeChild(kids[1]);
  targetGroup.isExpanded=false;
}

var ngroups=0;


function moveExtremalPoint(pnt, x, y) {
  var pGrp = pnt.parentElement; //parentGroup
  
  pnt.setAttribute("cx", x);
  pnt.setAttribute("cy", y);
  pGrp.x = x;
  pGrp.y = y;
  
  //update debug lines
  if (!pGrp.isRoot) {
    var line = pnt.nextSibling;
    line.setAttribute("x1", x);
    line.setAttribute("y1", y);
  }
  if (pGrp.isExpanded) {
    var j = pGrp.isRoot ? 1 : 0; //offset for root node, he has no line
    for (var i=2; i<=3; i++) {
      var line = pGrp.childNodes[i-j].childNodes[1];
      line.setAttribute("x2", x);
      line.setAttribute("y2", y);
    }
  }
}
/*
function moveGroup(grp, dx, dy) {
  var x = parseInt(grp.getAttribute("dx"));
  var y = parseInt(grp.getAttribute("dy"));
  grp.setAttribute("transform", "translate("+(x+dx)+","+(y+dy)+")");
  grp.setAttribute("dx", x+dx);
  grp.setAttribute("dy", y+dy);
  
  var kids = grp.parentNode.childNodes;
  //if (kids[3] && kids[4]) {
  if (grp.parentNode.expanded) {
    var i = 0;
    if (kids[1].id == grp.id) {i=0;}
    else {i=1;}
    var line = kids[3+i];
    line.setAttribute("x1", "0");
    line.setAttribute("y1", "0");
    line.setAttribute("x2", (x+dx));
    line.setAttribute("y2", (y+dy));
  }
}
*/


function createGroup(parent, x, y, isRoot) {
  
  //var x = parent.x + dx;
  //var y = parent.y + dy;
  //var name =  

  var group  = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("id", "grp"+ngroups);
  group.setAttribute("class", "contourgroup");
  group.x = x;
  group.y = y;
  group.r = 0; //distance to parent
  group.phi = 0; //angle of parent
  group.isExpanded = false;
  group.isRoot = isRoot;
  if (isRoot) {group.depth = 0;}
  else {group.depth = parent.depth+1;}
  

  var point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  point.setAttribute("class", "extremalpoint");
  point.setAttribute("cx", x);
  point.setAttribute("cy", y);
  point.setAttribute("r",  10);
  point.setAttribute("fill", "green");
  point.setAttribute("id", "point"+pointnr);
  point.setAttribute("type", "min");
  group.appendChild(point);
  
  
  if (!isRoot) {
    var line = document.createElementNS("http://www.w3.org/2000/svg", "line");
    line.setAttribute("x1", x);
    line.setAttribute("y1", y);
    line.setAttribute("x2", parent.x);
    line.setAttribute("y2", parent.y);
    line.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
    group.appendChild(line);
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
  
  var dx = parent.x - grp.x;
  var dy = parent.y - grp.y;
  var ang = toPolarAng(dx, dy);
  var rad = toPolarR(dx, dy);
  
  var cgrp = document.createElementNS("http://www.w3.org/2000/svg", "g");
  cgrp.setAttribute("id", "cgrp"+(ncgroups++));
  cgrp.setAttribute("class", "contourpoint_group");
  grp.appendChild(cgrp);
  
  for (var i = 1; i<n_cp; i++) { //no need to draw the first point
    var r_fac = Math.abs(i-n_cp/2.)/(0.5*n_cp); //gives a number 0..1
    r_fac = r_fac *0.25 + 0.50; //makes the radi between 50% and 75% of dist to parent
    var cp_ang = ang+i*dAng;
    var cp_rad = rad * r_fac;
    cp_x = grp.x + toRectX(cp_ang, cp_rad);
    cp_y = grp.y + toRectY(cp_ang, cp_rad);
    
    
    var point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    point.setAttribute("class", "contourpoint");
    point.setAttribute("cx", cp_x);
    point.setAttribute("cy", cp_y);
    point.setAttribute("r",  5);
    point.setAttribute("fill", "black");
    point.setAttribute("id", "cpnt"+(cpnt_nr++));
    
    point.ang = cp_ang;
    point.rad = cp_rad;
    
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
  var parent = grp.parentElement;
  // var j = grp.isRoot ? 1 : 0; //offset for root node, he has no line
  var j = grp.isExtended ? 0 : 2; //if not expanded, then two groups are missing
  var contGrp = grp.childNodes[4-j];
  var path = grp.childNodes[5-j];
  var pathstr = "";
  
  pathstr += "M" + parent.x + "," + parent.y + " "; //move to start pos
  
  for (var i=0; i<contGrp.childNodes.length; i++) {
    var pnt = contGrp.childNodes[i];
    var cp_x = grp.x + toRectX(pnt.ang, pnt.rad);
    var cp_y = grp.y + toRectY(pnt.ang, pnt.rad);
    pnt.setAttribute("cx", cp_x);
    pnt.setAttribute("cy", cp_y);
    pathstr += "L"+cp_x + ","+cp_y+" ";
  }
  
  pathstr += "Z"; //close path
  path.setAttribute("d", pathstr);
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