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
  createContour(point3);
  
  
  targetGroup.wasType = targetGroup.type;
  targetGroup.type = "sad";
  targetGroup.pnt.type = "sad";
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
  pGrp.x = x;
  pGrp.y = y;
  pGrp.pnt.x = x;
  pGrp.pnt.y = y;
  
  
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
  if (pGrp.isRoot) {
    checkType(pGrp);
  }
  else {
    checkType(pGrp.parentElement);
  }

}


function checkType(grp){
  if (grp.isExpanded) {
    var ppnt = grp.pnt;
    var j = (grp.isRoot) ? root_off : 0;
    var child1 = grp.childNodes[g1_id+j];
    var child2 = grp.childNodes[g2_id+j];
    var cpnt1 = child1.pnt;
    var cpnt2 = child2.pnt;
    
    var phi1 = ppnt.getAngleTo(cpnt1);
    var phi2 = ppnt.getAngleTo(cpnt2);
    var r1 = ppnt.getDistTo(cpnt1);
    var r2 = ppnt.getDistTo(cpnt2);
    var dphi = Math.abs(phi1-phi2);
    dphi = dphi>Math.PI ? Math.PI*2 - dphi : dphi;    
    
    if (dphi<Math.PI/3.) {
      var cng_grp = null;
      var oth_grp = null;
      
      if (r1>r2) {
        cng_grp = child2;
        oth_grp = child1;
      }
      else {
        cng_grp = child1;
        oth_grp = child2;
      }
      var newtype = grp.wasType=='min' ? 'max' : 'min';
      if (cng_grp.isExpanded) {
        cng_grp.wasType = newtype;
        checkType(cng_grp);

      }
      else {
        cng_grp.type = newtype;
        cng_grp.pnt.setType(newtype);
        cng_grp.childNodes[circ_id].setAttribute("fill", cng_grp.type=="min" ? "green" : "blue");

      }
      if (oth_grp.isExpanded){
        oth_grp.wasType = grp.wasType;
        checkType(oth_grp);     
      }
      else {
        oth_grp.type = grp.wasType;
        oth_grp.pnt.type = grp.wasType;
        oth_grp.childNodes[circ_id].setAttribute("fill", oth_grp.type=="min" ? "green" : "blue");      
      }
    }
    else {
      if (child1.isExpanded) {
        child1.wasType = grp.wasType;
        checkType(child1);
      }
      else {
        child1.type = grp.wasType;
        child1.pnt.type - grp.wasType;
        child1.childNodes[circ_id].setAttribute("fill", child1.type=="min" ? "green" : "blue");
      }
      if (child2.isExpanded) {
        child2.wasType = grp.wasType;
        checkType(child2);
      }
      else {
        child2.type = grp.wasType;
        child2.pnt.type - grp.wasType;
        child2.childNodes[circ_id].setAttribute("fill", child2.type=="min" ? "green" : "blue");
      }
    
    }
    
  }
}

/*
  func that checks whether the type of an extremalpoints has changed
  min <-> max
*/
/*
function checkType(grp) {
  var ppnt = grp.pnt;
  var j = (grp.isRoot) ? root_off : 0;
  var child1 = grp.childNodes[g1_id+j];
  var child2 = grp.childNodes[g2_id+j];
  var cpnt1 = child1.pnt;
  var cpnt2 = child2.pnt;
  
  var phi1 = ppnt.getAngleTo(cpnt1);
  var phi2 = ppnt.getAngleTo(cpnt2);
  var r1 = ppnt.getDistTo(cpnt1);
  var r2 = ppnt.getDistTo(cpnt2);
  var dphi = Math.abs(phi1-phi2);
  dphi = dphi>2*Math.PI ? dphi-2*Math.PI : dphi;
  
  if (dphi<Math.PI/2.) {
    var cng_grp = null;
    var cng_pnt = null;
    
    if (r1>r2) {
      cng_grp = child2;
      cng_pnt = cpnt2;
    }
    else {
      cng_grp = child1;
      cng_pnt = cpnt1;
    }
    var par_type = grp.wasType;
    
    
    
      // cpnt2.switchType();
      // child2.type = cpnt2.type;
      // var circ = child2.childNodes[circ_id];
      // var color = "black";
      // if (cpnt2.type=='sad') {color='red';}
      // else if (cpnt2.type=='min') {color='green';}
      // else if (cpnt2.type=='max') {color='blue';}
      // circle.setAttribute("fill", color);
      
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
  group.pnt = new Point(x,y);
  group.r = 0; //distance to parent
  group.phi = 0; //angle of parent
  group.isExpanded = false;
  group.isRoot = isRoot;
  if (isRoot) {
    group.depth = 0;
    group.type = "min";
    group.pnt.setType("min");
  }
  else {
    group.depth = parent.depth+1;
    group.type = parent.type;
    group.pnt.setType(parent.type);
  }
  

  var point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  point.setAttribute("id", "point"+pointnr);
  point.setAttribute("cx", x);
  point.setAttribute("cy", y);
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
    var cp_x = grp.x + toRectX(cp_ang, cp_rad);
    var cp_y = grp.y + toRectY(cp_ang, cp_rad);
    
    
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
  var parent = grp.parentElement;
  
  var dAng = Math.PI * 2 / n_cp;
  
  var dx = parent.x - grp.x;
  var dy = parent.y - grp.y;
  var ang = toPolarAng(dx, dy);
  var rad = toPolarR(dx, dy);
  
  // var j = grp.isRoot ? 1 : 0; //offset for root node, he has no line
  var j = grp.isExtended ? 0 : 2; //if not expanded, then two groups are missing
  var contGrp = grp.childNodes[4-j];
  var path = grp.childNodes[5-j];
  var pathstr = "";
  
  pathstr += "M" + parent.x + "," + parent.y + " "; //move to start pos
  
  for (var i=0; i<contGrp.childNodes.length; i++) {
    var pnt = contGrp.childNodes[i];
    
    var cp_ang = ang + pnt.d_ang;
    var cp_rad = rad * pnt.s_rad;
    var cp_x = grp.x + toRectX(cp_ang, cp_rad);
    var cp_y = grp.y + toRectY(cp_ang, cp_rad);
    
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
    
    var str = 'point: '+grp.id+" "+ps.toString() ;
    dbg.append(str);
    dbg.append('point: '+p1.id+" "+p1.pnt.toString() );
    dbg.append('point: '+p2.id+" "+p2.pnt.toString() );
    
    
    //maintain postorder traversal, nodes sortet by distance
    if (ps.getDistTo(p1.pnt) < ps.getDistTo(p2.pnt)) {
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
      //pnt = SVGtoPoint(grp.childNodes[circ_id]);
      pnt = grp.pnt;
    }
    else {
      //pnt = SVGtoPoint(grp.childNodes[circ_id]);
      pnt = grp.pnt;
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


function SVGtoPoint(circle) {
  return new Point(circle.getAttribute("cx"), circle.getAttribute("cy"));
}
