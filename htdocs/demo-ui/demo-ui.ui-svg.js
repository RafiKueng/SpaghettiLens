/*
  demo-ui.ui.js script file
  
  handels all the ui interactions with the svg layer
*/

var selectedPoint = false;


/****************************************************
 * UI CODE
 ****************************************************/

function initUI() {
  //alert("initUI");
  var element = document.getElementById("ui.svg.settings_menu");
  element.isVisible = false;
  //alert("done");
  
}

// this is called when specific elements are hoovered over
function mouseOver(evt) {
  var target = evt.target.parentElement; //the elements are supposed to be in a goup.
  
  if (!(target.isVisible) && !(target.getAttribute("visability")=="never")) {
    var trans =  "translate" + target.getAttribute("translate_vect_over");
    target.setAttribute("transform", trans);
    target.isVisible = true;
  }
}

// this is called when mouse leaves elements
function mouseOut(evt) {
  var target = evt.target.parentElement; //the elements are supposed to be in a goup.
  
  if ( (target.isVisible) && !(target.getAttribute("visability")=="always")) {
    var trans =  "translate" + target.getAttribute("translate_vect_out");
    target.setAttribute("transform", trans);
    target.isVisible = false;
  }
}

// clicks on a UI element, but not on a button
function onClickUI(evt) {
  var target = evt.target;
  alert("clicked on a tab, but no button: "+target.id);
  evt.stopPropagation();
}

// handler for all button clicks
function onClickBtn(evt) {
  var target = evt.target;
  
  switch(target.id) {
    case "m1_btn1":
    alert("click on bnt1");
    break;

    case "m1_btn2":
    alert("click on bnt2");
    break;

    case "m1_btn3":
    alert("click on bnt3");
    break;
    
    default:
    alert("click to no where (BAD): "+target.id);
    break;
  }
  evt.stopPropagation();
}


/****************************************************
 * Curve Code (layer2)
 ****************************************************/


// this handles all the clicks on the background to no element
function onClickSVG(evt){
  var target = evt.target;
  //alert("click on svg: " + target.id);
  
  // doubleclick on background
  if (target.id=="ui.svg_layer" && evt.detail>=2) {
    var pnt = coordTrans(evt);
    var parent = document.getElementById("layer2");
    var newgroup = createGroup(parent, pnt.x.toFixed(0), pnt.y.toFixed(0));
    parent.appendChild(newgroup);
  }
  else if (evt.detail>=2){
    //alert("doubleclick on " + target.id);
    expandPoint(target.parentElement);
  }
}

var dragTarget = false;
var x_start;
var y_start;

function onMouseDownContours(evt) {
  //var target = evt.target;
  
  //start moving
  dragTarget = evt.target;
  x_start = evt.clientX;
  y_start = evt.clientY;
  //dragTarget.ownerSVGElement.addEventListener('mousemove', onMouseMove, false);
  //document.getElementById("ui.svg_layer").addEventListener('mousemove', onMouseMove, false);
  //document.getElementById("ui.svg_layer").setAttribute("onmousemove", "onMouseMove(evt)");
}

function onMouseUpContours(evt) {
  //dragTarget.ownerSVGElement.removeEventListener('mousemove', onMouseMove, false);
  dragTarget = false;
}

function onMouseMove(evt) {
  
  var log = document.getElementById("debug.log");
  var p1 = coordTrans(evt);
  var p2 = localCoordTrans(evt);
  log.innerHTML = "move: target:"+evt.target.id+"; evt=" + evt.clientX + "," + evt.clientY
                + "; regCT:" + p1.x + "," + p1.y
                + "; locCT:" + p2.x + "," + p2.y;
  

  if (dragTarget) {
    
    var dx = evt.clientX - x_start;
    var dy = evt.clientY - y_start;
    moveGroup(evt.target.parentElement, dx, dy);
    x_start = evt.clientX;
    y_start = evt.clientY;  
    
    //moveGroup2(evt.target.parentElement, coordTrans(evt));
  }
}



/*
// clicks on one contour element
function onMouseDownContours(evt) {
  var target = evt.target;
  //alert("click on contour: "+target.id );
  selectContourPoint(target, coordTrans(evt));
  evt.stopPropagation();
}
*/

/*
function onMouseUpContours(evt) {
  var target = evt.target;
  //alert("click on contour: "+target.id );
  if (selectedPoint==false) {
    addContour(coordTrans(evt));
  }
  else {
    unselectContourPoint(target, coordTrans(evt));
  }
  evt.stopPropagation();
}
*/

/*
function onMouseMove(evt) {
  if (selectedPoint) {
    //alert("click on contour: "+target.id );
    movePoint(coordTrans(evt));
  }
  evt.stopPropagation();  
}
*/



/****************************************************
 * Helper functions
 ****************************************************/
 
function coordTrans(evt) {

  var m = evt.target.getScreenCTM();

  var root = document.getElementById("ui.svg_layer");
  var p = root.createSVGPoint(); 

  p.x = evt.clientX;
  p.y = evt.clientY;
  p = p.matrixTransform(m.inverse());

  return p;
}

function localCoordTrans(evt) {

  var m = evt.target.parentElement.getScreenCTM();

  var root = document.getElementById("ui.svg_layer");
  var p = root.createSVGPoint(); 

  p.x = evt.clientX;
  p.y = evt.clientY;
  p = p.matrixTransform(m.inverse());

  return p;
}

// HELPER/DEBUG: this shows infos about an event (coordinates)
function eventInfo(evt) {
  //var myMapApp = new mapApp();
  var coords = coordTrans(evt);
  var msg = ".screenX="+evt.screenX+", .screenY="+evt.screenY+
    "\n.clientX="+evt.clientX+", .clientY="+evt.clientY+
    "\nviewBoxX="+coords.x.toFixed(1)+", viewBoxY="+coords.y.toFixed(1);
  alert(msg);

}



function dlog(txt) {
  var log = document.getElementById("debug.log");
  log.innerHTML = txt;
}



/*
var pointnr=0;


function addContour(point) {

  var shape = document.createElementNS("http://www.w3.org/2000/svg", "circle");
  shape.setAttribute("cx", point.x);
  shape.setAttribute("cy", point.y);
  shape.setAttribute("r",  10);
  shape.setAttribute("fill", "green");
  shape.setAttribute("id", "point"+pointnr);
  pointnr++;
  document.getElementById("layer2").appendChild(shape); //the layer2 is the layer containing the paths

}

function movePoint(point) {
  selectedPoint.setAttribute("cx", point.x);
  selectedPoint.setAttribute("cy", point.y);
}

var selectedPoint = false;

function selectContourPoint(target, point) {
  selectedPoint = target;
}

function unselectContourPoint(target, point) {
  selectedPoint = false;
}
*/










/*
var menu1open=false;

//this function converts windowcoordinates to viewbort coordinates
function coordTrans(evt, root) {
  var pnt = root.createSVGPoint();
  pnt.x = evt.pageX;
  pnt.y = evt.pageY;

  var ctm = evt.target.getScreenCTM();
  if (ctm = ctm.inverse()){
    pnt = pnt.matrixTransform(ctm);
  }
  pnt.x = Math.round(pnt.x);
  pnt.y = Math.round(pnt.y);
  return pnt;
}

function clickOnBG(evt) {
  alert("bg click");
  //var cx = evt.getClientX();
  //var cy = evt.getClientY();
  var px = evt.pageX;
  var py = evt.pageY;
  
  var target = evt.target;
  
  var pnt = coordTrans(evt, document.getElementById('ui'));
  //alert("click" + pnt.x + "-" + pnt.y);
  var fact = 1.5;
  var y_off = 600;
  var quad = document.createElementNS("http://www.w3.org/2000/svg", "rect");
  quad.setAttribute("x", (pnt.x)/fact);
  quad.setAttribute("y", (pnt.y-y_off)/fact);
  quad.setAttribute("height", 10);
  quad.setAttribute("width", 10);
  
  var svg_ui=document.getElementById("layer1");
  svg_ui.appendChild(quad);
  
}

function importCanvas(sourceCanvas, targetSVG) {
  var image = sourceCanvas.toDataURL("image/png"); // get base64 encoded png from Canvas
  var svgimg = document.createElementNS("http://www.w3.org/2000/svg", "image"); // Create new SVG Image element.  Must also be careful with the namespaces.
  svgimg.setAttributeNS("http://www.w3.org/1999/xlink", 'xlink:href', image);
  targetSVG.appendChild(svgimg); // Append image to SVG
}


function mouseOverMenu1(evt) {
  if (menu1open==false) {
    //alert("2nd try");
    var menu12=document.getElementById("ui.svg.settings_menu");
    menu12.setAttribute('transform','translate(90,0)');
    menu1open=true;
  }
}

function mouseOutMenu1(evt) {
  if (menu1open==true) {
    //alert("2nd try");
    var menu12=document.getElementById("ui.svg.settings_menu");
    menu12.setAttribute('transform','translate(0,0)');
    menu1open=false;
  }
}

function clickM1Btn1(evt) {
  alert("1st button clicked");
  loadImage();
}

function loadImage() {
  var uri = "hubble-udf.jpg" //later get this message from backend
  
  var canvas = document.getElementById('bg_canv');
  var ctx = canvas.getContext('2d');
  var img = new Image;
  img.onload = function(){ //play save, wait with draw till fully loaded
    blendImage(canvas, ctx, img);
    //ctx.drawImage(img,0,0);
  };
  img.src = uri;

}

function blendImage(canvas, ctx, img) {
  // see here:
  // http://stackoverflow.com/questions/3648312/blend-two-images-on-a-javascript-canvas  
  var width = canvas.width;
  var height = canvas.height;
  var pixels = 4 * width * height;
  
  ctx.drawImage(img, 0, 0);
  var img1 = ctx.getImageData(0, 0, width, height);
  var img1data = img1.data;
  
  while (pixels--) {
      img1data[pixels] = img1data[pixels] * 0.5 + 0.5; //add real blending formula here
  }
  img1.data = img1data;
  ctx.putImageData(img1, 0, 0);
}
*/