/*
  demo-ui.js script file
*/

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