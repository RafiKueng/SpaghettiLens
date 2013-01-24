/*************************************
 * lmt.ui.svg.js
 * this takes care of all the svg ui interactions
 * 
 *  only takes care of the setup and low level user interactions,
 * translates them to highlevel custom events that will be fired
 * and react on in the app intelligence part
 */
/*(function(){*/


/**
 * set some constants and expose structure 
 */
var svg = {
	ns: "http://www.w3.org/2000/svg",
	xlinkns: "http://www.w3.org/1999/xlink",
	
	layer: {
		zoompan: null,
		bg: null,
		masses: null,
		models: null,
		connectorlines: null,
		contourlines: null,
		contourpoints: null,
		extremalpoints: null,
		rulers: null
	}
};



/**
 * creates and initalises the svg input area 
 */
svg.initCanvas = function() {
	var parent = document.getElementById("inp");
	svg.root = document.createElementNS(svg.ns, "svg");
	
	svg.root.setAttribute("version", "1.2");
		
	// create the layers
	svg.layer = {};
	
	svg.layer.defs = document.createElementNS(svg.ns, "defs");

	svg.layer.zoompan = document.createElementNS(svg.ns, "g");
		svg.layer.bg = document.createElementNS(svg.ns, "g");
		svg.layer.masses = document.createElementNS(svg.ns, "g");
		svg.layer.models = document.createElementNS(svg.ns, "g");
			svg.layer.connectorlines = document.createElementNS(svg.ns, "g");
			svg.layer.contourlines = document.createElementNS(svg.ns, "g");
			svg.layer.contourpoints = document.createElementNS(svg.ns, "g");
			svg.layer.extremalpoints = document.createElementNS(svg.ns, "g");
		svg.layer.rulers = document.createElementNS(svg.ns, "g");

	
	//set attributes	
	svg.root.setAttribute('id', 'svgroot');
	svg.root.setAttribute('width', '100%');
	svg.root.setAttribute('height', '100%');
	svg.root.setAttribute('xmlns:xlink', svg.xlinkns);
	svg.layer.bg.setAttribute('id', 'bg');

	//set event listeners
	svg.root.addEventListener('click', LMT.ui.svg.events.onClick);
	svg.root.addEventListener('mousedown', LMT.ui.svg.events.onMouseDown);
	svg.root.addEventListener('mouseup', LMT.ui.svg.events.onMouseUp);
	svg.root.addEventListener('mouseout', LMT.ui.svg.events.onMouseOut);
	
	if (svg.root.addEventListener) {
		// IE9, Chrome, Safari, Opera
		svg.root.addEventListener("mousewheel", LMT.ui.svg.events.onMouseWheel, false);
		// Firefox
		svg.root.addEventListener("DOMMouseScroll", LMT.ui.svg.events.onMouseWheel, false);
	}
	// IE 6/7/8
	else svg.root.attachEvent("onmousewheel", LMT.ui.svg.events.onMouseWheel);
	
	
	
	// add everything to DOM
	svg.layer.zoompan.appendChild(svg.layer.bg);
	svg.layer.zoompan.appendChild(svg.layer.masses);

	svg.layer.models.appendChild(svg.layer.connectorlines);
	svg.layer.models.appendChild(svg.layer.contourlines);
	svg.layer.models.appendChild(svg.layer.contourpoints);
	svg.layer.models.appendChild(svg.layer.extremalpoints);

	svg.layer.zoompan.appendChild(svg.layer.models);
	svg.layer.zoompan.appendChild(svg.layer.rulers);

	svg.root.appendChild(svg.layer.defs);
	svg.root.appendChild(svg.layer.zoompan);
	
	parent.appendChild(svg.root);
}





/**
 * initialises the background to nothing
 */
/*
svg.initBG = function(urls) {
	var rect = document.createElementNS(svg.ns, "rect");
	
	rect.setAttribute('x', '0px');
	rect.setAttribute('y', '0px');
	rect.setAttribute('width', '100%');
	rect.setAttribute('height', '100%');
	rect.setAttribute('fill', 'black');
	
	
	svg.layer.bg.appendChild(rect);
}
*/

/**
 * event handler:
 * switch the input mode
 * (what kind of object does a click into nothing create) 
 */
svg.SwitchMode = function(evt, newMode){
  LMT.settings.mode = newMode;
  $.event.trigger("ModeSwitched");
  log.append("mode switched to " + newMode);
}






/**
 * event handlers for interaction with the svg canvas
 * 
 * this grabs the low level system events and converts it to contextual high level events
 */
svg.events = {
	state: 'none', //none, drag, pan
	dragTarget: null,
	preventClick: false,
	someElementWasDragged: false,
	lastMouseMove: 0,
	
	
	onMouseDown: function(evt) {
		
	  evt.stopPropagation();
	  evt.preventDefault();
	
		dragTargetStr = evt.target.id.substring(0,4)
		if (dragTargetStr=="poin"
			|| dragTargetStr=="cpnt"
			|| dragTargetStr=="ext_"
			|| dragTargetStr=="rule") {
			svg.events.dragTarget = evt.target;
			svg.events.state = 'drag';
		}
		else {
			svg.events.state = 'pan';
			/*
			svg.events.stateTf = svg.layer.zoompan.getCTM().inverse();
			svg.events.stateOrigin = LMT.ui.svg.coordTrans(evt).matrixTransform(svg.events.stateTf);
			*/
			svg.events.stateOrigin = {x: evt.screenX, y: evt.screenY, scale: LMT.settings.display.zoompan.scale};
		}
		svg.root.addEventListener('mousemove', LMT.ui.svg.events.onMouseMove);
	
	},
	
	
	
	onMouseMove: function(evt) {
	  evt.stopPropagation();
	  evt.preventDefault();
	  
	  //prevent to high refresh rate (only each 50ms)
	  if (evt.timeStamp - svg.events.lastMouseMove < 20) {return;}
	  svg.events.lastMouseMove = evt.timeStamp;
	  
		var dx = evt.screenX - svg.events.stateOrigin.x;
		var dy = evt.screenY - svg.events.stateOrigin.y;
		
		/**
		 * did really something happen? break otherwise 
		 */
		if (dx==0 && dy==0) {
			return;
		}
	  
	  if (svg.events.state == 'drag') {
	    var coord = LMT.ui.svg.coordTrans(evt);
	    
	    $.event.trigger('MoveObject', [svg.events.dragTarget.jsObj, svg.events.dragTarget, coord]);
	    
			svg.events.someElementWasDragged = true;
	  	svg.events.preventClick = true;
	  }
	  
	  else if (svg.events.state == 'pan') {
      // create a temporary state and move the layer to the new state
      // only on mouse up the newstate will become the current state
			svg.events.newState = {	x: LMT.settings.display.zoompan.x + dx,
															y: LMT.settings.display.zoompan.y + dy,
															scale: LMT.settings.display.zoompan.scale};
			
			$.event.trigger('Pan', [svg.events.newState]);
			
			svg.events.someElementWasDragged = false;
	  	svg.events.preventClick = true;
	  }
	},
	
	
	
	onMouseUp: function(evt) {
		if (svg.events.state == 'pan') {
			if (svg.events.newState) {
				LMT.settings.display.zoompan = svg.events.newState;
			}
		}
		if (svg.events.someElementWasDragged) {
			$.event.trigger("SaveModelState");
		  evt.stopPropagation();
		  evt.preventDefault();
		}
		svg.events.someElementWasDragged = false;
		svg.root.removeEventListener('mousemove', LMT.ui.svg.events.onMouseMove);
	},
	
	
	
	onClick: function(evt) {
		if (svg.events.preventClick) {
			svg.events.preventClick = false;
			return;
		}
		
		// click on middle button
		// 1 according to w3c, 4 according to ms... (but this time, the ms solution is actually better...)
		if (evt.button == 1 || evt.button == 4) {
			/**
      * reset zoom and pan to default
      */ 
      $.event.trigger('ZoomPanReset');
      if (evt.stopPropagation) {evt.stopPropagation();}
      if (evt.preventDefault) {evt.preventDefault();}
			return;
		}
		
	  var target = evt.target;
	  var parent = evt.target.parentElement;
	  
	  var somethinghappend = false;
	  
	  //click on background
		if ( target.id == 'svgroot' || parent.id == 'bg') {
			
      var coord = svg.coordTrans(evt);			
			
			if (LMT.settings.mode == 'image') {
				$.event.trigger('CreateRootMinima', [coord]);
			}
			
			else if (LMT.settings.mode == 'mass') {
				$.event.trigger('CreateExternalMass', [coord]);
			}
			
			else if (LMT.settings.mode == 'ruler') {
				$.event.trigger('CreateRuler', [coord]);
      }

      somethinghappend = true;
		}	  

	  //click on an extremalPoint
	  else if (target.id.substring(0,5) == "point") {
			var pnt = target.jsObj;
			$.event.trigger('ToggleExtremalPoint', [pnt]);
      somethinghappend = true;
  	}
  	
  	//click on contour points
  	else if (target.id.substring(0,4) == "cpnt") {
			var pnt = target.jsObj;
  		$.event.trigger('CreateContourPoint', [pnt]);
      somethinghappend = true;
  	}
  	
  	//is it something with an assigned js object? (rulers, pointmasses)
  	else if (target.jsObj) {
  		$.event.trigger('DeleteObject', [target.jsObj]);
      somethinghappend = true;
  	}


	  //push the new model to the undo / action stack
	  if (somethinghappend) {
	  	$.event.trigger("SaveModelState");
	  } 
	},

	
	/**
	 * adds zooming function
	 * based on this post:  http://www.sitepoint.com/html5-javascript-mouse-wheel/
	 */
	onMouseWheel: function(evt) {
		// cross-browser wheel delta
		var e = window.event || evt; // old IE support
		var delta = Math.max(-1, Math.min(1, (e.wheelDelta || -e.detail)));
		
		$.event.trigger('Zoom', [delta]);

		if (evt.stopPropagation) {evt.stopPropagation();}
		if (evt.preventDefault) {evt.preventDefault();}
		
	},

	
	/**
	 * abort all operations on mouse out of svg area 
	 */
	onMouseOut: function(evt) {
		/*
		if (evt.target.farthestViewportElement.id != "svgroot") {
			svg.events.onMouseUp(evt);
		}
		*/
	}
}
	
/**
 * transforms the optained raw coordines in the coordinate system of the zoomed / panned layer 
 */
svg.coordTrans = function(evt) {

	var pt = svg.root.createSVGPoint();
	pt.x = evt.clientX;
	pt.y = evt.clientY;
	var globalPoint = pt.matrixTransform(svg.root.getScreenCTM().inverse());
	var globalToLocal = svg.layer.zoompan.getTransformToElement(svg.root).inverse();
	var inObjectSpace = globalPoint.matrixTransform( globalToLocal );
	
  return inObjectSpace;
}



/**
 * Loads & Blends the background imgage(s) for the input canvas
 * using a svg filter chain 
 */
svg.bg = {
  init: function() {
  
    var url = LMT.modelData.url;
    var ch = LMT.modelData.ch;
    
  	var filter = document.createElementNS(svg.ns, "filter");
  	filter.setAttribute("id","fBG");
  
  	// the black background
  	var floodfilter = document.createElementNS(svg.ns, "feFlood");
  	floodfilter.setAttribute("flood-color","#000000");
  	floodfilter.setAttribute("flood-opacity","1");
  	floodfilter.setAttribute("result","comp");
  	filter.appendChild(floodfilter);
  	svg.bgCmatrix = [];
  
  	//for each background image...
  	for (var i = 0; i<url.length; i++){
  		
  		//.. load the image
  		var img = document.createElementNS(svg.ns, "feImage");
  		img.setAttributeNS(svg.xlinkns,"href", url[i]);
  		img.setAttribute("x","0");
  		img.setAttribute("y","0");
  		img.setAttribute("width","100%");
  		img.setAttribute("height","100%");
  		img.setAttribute("result","img"+i);
  		filter.appendChild(img);
  		
  		//apply the color matrix transform
  		var cmatrix = document.createElementNS(svg.ns, "feColorMatrix");
  		cmatrix.setAttribute("type", "matrix");
  		cmatrix.setAttribute("in", "img"+i);
  		cmatrix.setAttribute("result", "cimg"+i);
  		cmatrix.setAttribute("values", svg.generateColorMatrix(ch[i]));
  		filter.appendChild(cmatrix);
  		svg.bgCmatrix.push(cmatrix);
  		
  		//blend to others using porter-diff
  		var comp = document.createElementNS(svg.ns, "feComposite");
  		comp.setAttribute("in", "comp");
  		comp.setAttribute("in2", "cimg"+i);
  		comp.setAttribute("result", "comp");
  		comp.setAttribute("operator", "arithmetic");
  		comp.setAttribute("k1", "0");
  		comp.setAttribute("k2", "1");
  		comp.setAttribute("k3", "1");
  		comp.setAttribute("k4", "0");
  		filter.appendChild(comp);
  	}
  
  	var bgrect = document.createElementNS(svg.ns, "rect");
  	bgrect.setAttribute("x","0");
  	bgrect.setAttribute("y","0");
  	bgrect.setAttribute("width","100%");
  	bgrect.setAttribute("height","100%");
  	bgrect.setAttribute("filter","url(#fBG)");
  	
  	
  	svg.layer.defs.appendChild(filter);
  	svg.layer.bg.appendChild(bgrect);
  },
  
  updateColor: function(evt, i){
  	svg.bgCmatrix[i].setAttribute("values", svg.generateColorMatrix(LMT.modelData.ch[i]));
  },
  
  
  /**
   * sets the model view zoom and pan status
   * if state: to this coord and zoom factor, otherwise to the settings 
   */
  updateZoomPan: function(evt, state){
    var s;
    if (state){
      s = "translate(" + (state.x) + "," +
                             (state.y) + ") " + 
              "scale(" + state.scale + ")";
    }
    else {
      s = "translate(" + (LMT.settings.display.zoompan.x) + "," +
                         (LMT.settings.display.zoompan.y) + ") " + 
              "scale(" + LMT.settings.display.zoompan.scale + ")";
    }
    svg.layer.zoompan.setAttribute("transform", s);
    //no RepaintModel should be needed, only in zoom case, whats already taken care of below
  },
  
  zoom: function(evt, delta){
    LMT.settings.display.zoompan.scale *= 1 + delta*0.1;
    LMT.ui.svg.bg.updateZoomPan();
    $.event.trigger("RepaintModel"); //is needed to change the radii of the masses, rulers ect..
  },
  
  zoomPanReset: function() {
    LMT.settings.display.zoompan.x = 0;
    LMT.settings.display.zoompan.y = 0;
    LMT.settings.display.zoompan.scale = 1;
    LMT.ui.svg.bg.updateZoomPan();
    $.event.trigger("RepaintModel"); //is needed to change the radii of the masses, rulers ect..
  }
  
  
}


/**
 * generates the value string / ColorMatrix for channel ch 
 * ch = {
 * 	r, g, b: color values [0 ... 255]
 *  contrast: [0.1 ... 1 ... 10]
 *  brightness: [-1 ... 0 ... 1]
 * }
 * 
 * col vector: [r, g, b, a, 1]
 * 
 * col_new' = mat * col'
 * 
 * C in (r, g, b)
 * C_i = M_i0 * r + M_i1 * g + M_i2 * b + M_i3 * a + M_i4
 * 
 * since input image is pure grayscale, only M_ii and M_i4 matter
 * 
 * M_ii = contrast * c_ii
 * 
 * ***************
 * for brightness / contrast:
 * new_val(old_val) = m * old_val + q
 * 
 * contrast adj: this is an eq through fixpoint 0.5/0.5:
 * q = (1-m) / 2
 * 
 * brightness shifts this curve by adding some value to q:
 * q' = (1-m) / 2 + br
 * 
 * so you get the summand you have to add (the a_i4 column), i.e:
 * 
 * M_i4 = (1-contrast) / 2 + brightness
 * 
 */
svg.generateColorMatrix = function(ch) {
	var r = ch.r;
	var g = ch.g;
	var b = ch.b;
	var co = ch.contrast;
	var br = ch.brightness;
	
	var i = (1-co)/2 + (br);

	var a00 = co * r;
	var a11 = co * g;
	var a22 = co * b;
	
	var a04 = i * r;
	var a14 = i * g;
	var a24 = i * b;
	var a34 = 0;
	
	var str = "" + 
		a00   + " 0"  + " 0"  + " 0 " + a04 + "\n" +
		" 0 " +  a11  + " 0"  + " 0 " + a14 + "\n" +
		" 0"  + " 0 " +  a22  + " 0 " + a24 + "\n" +
		" 1"  + " 0"  + " 0"  + " 0 " + a34 ;
		
	return str;
}


LMT.ui.svg = svg;


/*})();*/
