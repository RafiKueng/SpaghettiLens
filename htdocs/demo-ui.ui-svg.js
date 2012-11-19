/*
  demo-ui.ui.js script file
  
  handels all the ui interactions with the svg layer
*/

var selectedPoint = false;


/****************************************************
 * UI CODE
 ****************************************************/

 var root = null;
 
function initUI() {
  
  root = document.getElementById("ui.svg_layer");
  
  //alert("initUI");
  var element = document.getElementById("ui.svg.settings_menu");
  element.isVisible = false;
  
  // disable default image dragging behaviour
  /*
  root.mousedown = "if (event.preventDefault) event.preventDefault()";
  root.onmousedown = "if (event.preventDefault) event.preventDefault()";
  root.mousemove = "if (event.preventDefault) event.preventDefault()";
  root.onmousemove = "if (event.preventDefault) event.preventDefault()";
  */
  
  //alert("init done");
  
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
  var target = evt.currentTarget;
  
  switch(target.id) {
    case "m1_btn1":
    alert("click on bnt1");
    evt.stopPropagation();
    break;

    case "m1_btn2":
    alert("click on bnt2");
    evt.stopPropagation();
    break;

    case "m1_btn3":
    alert("click on bnt3");
    evt.stopPropagation();
    break;
    
    case "ui_btn_go":
    calculateModel();
    //alert("clicked on go");
    evt.stopPropagation();
    break;
    
    case "ui_rulerMode":
    //alert("clicked on ruler mode");
    settings.mode=2;
    select.modehighlight.setAttribute("transform",constants.highliter_pos[settings.mode]);
    evt.stopPropagation();
    break;

    case "ui_massMode":
    //alert("clicked on ui_massMode");
    settings.mode=1;
    select.modehighlight.setAttribute("transform",constants.highliter_pos[settings.mode]);
    evt.stopPropagation();
    break;

    case "ui_imgMode":
    //alert("clicked on imgMode");
    settings.mode=0;
    select.modehighlight.setAttribute("transform",constants.highliter_pos[settings.mode]);
    evt.stopPropagation();
    break;

    case "ui_btn_undo":
    alert("clicked on undo");
    evt.stopPropagation();
    break;

    case "ui_btn_redo":
    alert("clicked on redo");
    evt.stopPropagation();
    break;
    
    default:
    alert("click to no where (BAD): "+target.id);
    break;
  }
}


/****************************************************
 * Curve Code (layer2)
 ****************************************************/


// this handles all the clicks on the background to no element
function onClickSVG(evt){
  var target = evt.target;
  var parent = evt.target.parentElement;
  var pnt = target.pnt;
  //alert("click on svg: " + target.id);
  
  
  switch(settings.mode) {
  
    case constants.modeImg:
      // doubleclick on background
      //if (target.id=="ui.svg_layer" && evt.detail>=2) {
      if (target.id=="bg" && evt.detail>=2) {
        
        var svgpnt = coordTrans(evt);
        //var parent = document.getElementById("layer2");
        //var newgroup = createGroup(parent, parseInt(pnt.x.toFixed(0)), parseInt(pnt.y.toFixed(0)), true);
        //parent.appendChild(newgroup);
        createRootPoint(svgpnt.x, svgpnt.y);
      }
      else if (evt.detail>=2 && target.id.substring(0,5)=="point"){
        //alert("doubleclick on " + target.id);
        if (pnt.isExpanded) {
          collapsePoint(pnt);
        }
        else {
          expandPoint(pnt);
        }
      }
    break;
      
    
    case constants.modeMass:
      //alert("clicked bg in mass mode");
      if (target.id=="bg") {
        var pnt = coordTrans(evt);
        var parent = document.getElementById("layer3");
        var newgroup = createMassPoint(parent, parseInt(pnt.x.toFixed(0)), parseInt(pnt.y.toFixed(0)));
      }
      else {
        var parent = document.getElementById("layer3");
        parent.removeChild(target);
      }
    break;
    
    case constants.modeRuler:
      alert("clicked bg in ruler mode");
    break;
  }
}

var dragTarget = false;
var dragTargetStr = "";
var x_start;
var y_start;

function onMouseDownContours(evt) {
  //var target = evt.target;
  
  //start moving
  dragTargetStr = evt.target.id.substring(0,4)
  if (dragTargetStr=="poin" || dragTargetStr=="cpnt") {
    dragTarget = evt.target;
  }

  //dragTarget.ownerSVGElement.addEventListener('mousemove', onMouseMove, false);
  //document.getElementById("ui.svg_layer").addEventListener('mousemove', onMouseMove, false);
  //document.getElementById("ui.svg_layer").setAttribute("onmousemove", "onMouseMove(evt)");
  evt.stopPropagation();
  evt.preventDefault();
}

function onMouseUpContours(evt) {
  //dragTarget.ownerSVGElement.removeEventListener('mousemove', onMouseMove, false);
  dragTarget = false;
}

function onMouseMove(evt) {
  
  var p1 =  coordTrans(evt);
  var log = "move: target:"+evt.target.id+"; dragtrg:"+dragTarget.id+"; evt=" + evt.clientX + "," + evt.clientY
                + "; regCT:" + p1.x.toFixed(1) + "," + p1.y.toFixed(1);
  dbg.write(log);

  if (dragTarget) {
    var pnt = coordTrans(evt);
    if (dragTargetStr=="poin") {
	    moveExtremalPoint(dragTarget.pnt, pnt.x, pnt.y);
		}
		else if (dragTargetStr=="cpnt") {
			moveContourPoint(dragTarget.pnt, pnt.x, pnt.y);
		}

  }
  evt.stopPropagation();

}





/****************************************************
 * Helper functions
 ****************************************************/
 
function coordTrans(evt) {

  var m = evt.target.getScreenCTM();

  var root = document.getElementById("ui_svg_layer");
  var p = root.createSVGPoint(); 

  p.x = evt.clientX;
  p.y = evt.clientY;
  p = p.matrixTransform(m.inverse());
  p.x = Math.round(p.x);
  p.y = Math.round(p.y);

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

function addBG() {
  var canv = document.getElementById('ui_canvas_layer');
  var svg = document.getElementById('ui_svg_layer');
  importCanvas(canv, svg);
  
}

// adds the canvas to the svg
function importCanvas(sourceCanvas, targetSVG) {
  var image = sourceCanvas.toDataURL("image/png"); // get base64 encoded png from Canvas
  var svgimg = document.createElementNS("http://www.w3.org/2000/svg", "image"); // Create new SVG Image element.  Must also be careful with the namespaces.
  svgimg.setAttributeNS("http://www.w3.org/1999/xlink", 'xlink:href', image);
  targetSVG.appendChild(svgimg); // Append image to SVG
  var tmp=0;
}
