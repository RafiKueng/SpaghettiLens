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
  var p1x = +dx/(targetGroup.depth/3+1);
  var p2x = -dx/(targetGroup.depth/3+1);
  var p1y = +dy/(targetGroup.depth/3+1);
  var p2y = p1y;

  var point2 = createGroup(targetGroup, p1x, p1y, false);
  var point3 = createGroup(targetGroup, p2x, p2y, false);
  
  //targetGroup.getChildren()[0].setAttribute("type", "saddle");
  //targetGroup.getChildren()[0].setAttribute("fill", "yellow");
  
  targetGroup.appendChild(point2);
  targetGroup.appendChild(point3);
  targetGroup.expanded = true;
  
  //helper lines for visualisation during developpment
  var line1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line1.setAttribute("x1", "0");
  line1.setAttribute("y1", "0");
  line1.setAttribute("x2", p1x);
  line1.setAttribute("y2", p1y);
  line1.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
  targetGroup.appendChild(line1);  

  var line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line2.setAttribute("x1", "0");
  line2.setAttribute("y1", "0");
  line2.setAttribute("x2", p2x);
  line2.setAttribute("y2", p2y);
  line2.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
  targetGroup.appendChild(line2);  
}

function collapsePoint(targetGroup) {
  var kids = targetGroup.childNodes;
  targetGroup.removeChild(kids[4]);
  targetGroup.removeChild(kids[3]);
  targetGroup.removeChild(kids[2]);
  targetGroup.removeChild(kids[1]);
  targetGroup.expanded=false;
}

var ngroups=0;

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

function moveGroup2(grp, pnt) {
  grp.setAttribute("transform", "translate("+pnt.y+","+pnt.y+")");
}

function createGroup(parent, dx, dy, isRoot) {
  
  //var x = parent.x + dx;
  //var y = parent.y + dy;
  //var name =  

  var group  = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("id", "grp"+ngroups);
  group.setAttribute("class", "contourgroup");
  group.setAttribute("transform", "translate("+dx+","+dy+")");
  group.setAttribute("dx", dx);
  group.setAttribute("dy", dy);
  group.expanded = false;
  group.isRoot = isRoot;
  if (isRoot) {group.depth = 0;}
  else {group.depth = parent.depth+1;}
  

  var point = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  point.setAttribute("class", "extremalpoint");
  point.setAttribute("cx", 0);
  point.setAttribute("cy", 0);
  point.setAttribute("r",  10);
  point.setAttribute("fill", "green");
  point.setAttribute("id", "point"+pointnr);
  point.setAttribute("type", "min");
  
  pointnr++;
  ngroups++;

  group.appendChild(point);
  //parent.appendChild(group);
  return group;
  
}
