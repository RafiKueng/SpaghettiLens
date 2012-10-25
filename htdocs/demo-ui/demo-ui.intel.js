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
