/*
  this script contains all the buisiness intelligence

*/

function onBodyInit() {
  initUI();
}


var pointnr = 0;

function expandPoint(targetGroup) {

  var dx = 30;
  var dy = 30;
  
  //if (targentGroup.parentElement.class == "contourgroup") {
    //make custom dx, dy depending on the parent group
  //}

  var point2 = createGroup(targetGroup, +dx, +dy);
  var point3 = createGroup(targetGroup, -dx, -dy);
  
  //targetGroup.getChildren()[0].setAttribute("type", "saddle");
  //targetGroup.getChildren()[0].setAttribute("fill", "yellow");
  
  targetGroup.appendChild(point2);
  targetGroup.appendChild(point3);
  
  //helper lines for visualisation during developpment
  var line1 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line1.setAttribute("x1", "0");
  line1.setAttribute("y1", "0");
  line1.setAttribute("x2", +dx);
  line1.setAttribute("y2", +dy);
  line1.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
  targetGroup.appendChild(line1);  

  var line2 = document.createElementNS("http://www.w3.org/2000/svg", "line");
  line2.setAttribute("x1", "0");
  line2.setAttribute("y1", "0");
  line2.setAttribute("x2", -dx);
  line2.setAttribute("y2", -dy);
  line2.setAttribute("style","stroke:rgb(0,0,0);stroke-width:1");
  targetGroup.appendChild(line2);  
  
}

var ngroups=0;

function moveGroup(grp, dx, dy) {
  var x = parseInt(grp.getAttribute("dx"));
  var y = parseInt(grp.getAttribute("dy"));
  grp.setAttribute("transform", "translate("+(x+dx)+","+(y+dy)+")");
  grp.setAttribute("dx", x+dx);
  grp.setAttribute("dy", y+dy);
}

function moveGroup2(grp, pnt) {
  grp.setAttribute("transform", "translate("+pnt.y+","+pnt.y+")");
}

function createGroup(parent, dx, dy) {
  
  //var x = parent.x + dx;
  //var y = parent.y + dy;
  //var name =  

  var group  = document.createElementNS("http://www.w3.org/2000/svg", "g");
  group.setAttribute("id", "grp"+ngroups);
  group.setAttribute("class", "contourgroup");
  group.setAttribute("transform", "translate("+dx+","+dy+")");
  group.setAttribute("dx", dx);
  group.setAttribute("dy", dy);
  

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
