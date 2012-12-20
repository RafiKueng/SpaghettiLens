/*
  demo-ui.ui-svg.js script file
  
  handels all the ui interactions with the canvas element
*/

var canvas = {}; //will be a html canvas element with additional attributes

canvas.init = function() {
  canvas.c = document.getElementById('ui_bg_canvas');
  canvas.width = canvas.c.width;
  canvas.height = canvas.c.height;
  canvas.ctx = canvas.c.getContext('2d');
}

canvas.loadImages = function(urls) {
	canvas.images = [];
	canvas.nImages = urls.length; //TODO use channel information later
	canvas.nImgLoaded = 0;
	for (var i = 0; i<urls.length;++i) {
		var img = new Image;
		img.onload = canvas.imgLoaded;
		img.src = urls[i];
	}
}


/**
 * function that will be called upon an image element, as soon as its loaded
 * this = loaded image
 */
canvas.imgLoaded = function() {
	//var tmp = this;
	canvas.ctx.clearRect(0,0,canvas.width, canvas.height);
	canvas.ctx.drawImage(this, 0, 0);
	
	var img = canvas.ctx.getImageData(0, 0, canvas.width, canvas.height);
	img.jsImage = this;
	canvas.images.push(img);
	canvas.waitForLoadToCompelte();
}


canvas.waitForLoadToCompelte = function() {
	canvas.nImgLoaded++;
	if (canvas.nImgLoaded == canvas.nImages){
		canvas.repaint();
		ui.popup._graphicssettings.oninit();
	}
}



canvas.repaint = function() {

  var width = canvas.width;
  var height = canvas.height;
  var pixels = width * height;

	canvas.ctx.clearRect(0,0,canvas.width, canvas.height);
	var img = canvas.ctx.getImageData(0, 0, canvas.width, canvas.height);
  var imgdata = img.data;

	//original parameters are between 0..1, where 0.5 is default value
	// b has a range -128...+128
	// c has a range 1/10 ... 10
	var b = (model.brightness-0.5) * 256;
	var c = Math.pow(10,model.contrast*2)/10;
  
  // for every pixel do:
  //set cursor to working
  $sel.body.style.cursor = 'wait';
  //$sel.svguilayer.style.cursor = 'wait';
  
  
  
  while (pixels--) {
  	dbg.write(pixels);
  	// for every subpixel do: (r, g, b; loop throu every color of final picture)
  	for (var i = 0; i<3; ++i){
  		var val = 0;
  		
  		for (var cnl = 0; cnl < canvas.images.length; ++cnl){
  			val += canvas.images[cnl].data[pixels*4+i] * model.channels[cnl].color.rgb[i] * model.channels[cnl].alpha;
  			//val += canvas.images[cnl].data[pixels*4+i];
  		}
 
 			// adjust brighness and contrast
 			// formula according to: http://pippin.gimp.org/image_processing/chap_point.html
			val = (val - 128) * c + 128 + b;
  		
  		//clamp the range
  		val = val > 255 ? 255 : val;
  		val = val <   0 ?   0 : val;
  		
  		//save the subpixel
	  	imgdata[pixels*4+i] = val; 
		}
		
  	//a: set transparency
  	imgdata[pixels*4+3] = 255;
  }
  img.data = imgdata;
  canvas.ctx.putImageData(img, 0, 0);

	//reset cursor
  $sel.body.style.cursor = 'auto';
  //$sel.svguilayer.style.cursor = 'auto';
}




function loadImage(uri) {
  //var uri = "hubble-udf.jpg" //later get this message from backend
  
  var canvas = document.getElementById('ui_bg_canvas');
  var ctx = canvas.getContext('2d');
  var img = new Image;
  img.onload = function(){ //play save, wait with draw till fully loaded
    blendImage(canvas, ctx, img);
    //ctx.drawImage(img,0,0);
    //addBG(); //TODO fix this, for some reason the bg doesn't show up in the canvas.. now i just use css to put svg ontop of canvas
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

