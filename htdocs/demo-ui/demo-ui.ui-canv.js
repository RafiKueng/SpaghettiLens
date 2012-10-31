/*
  demo-ui.ui-svg.js script file
  
  handels all the ui interactions with the canvas element
*/



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