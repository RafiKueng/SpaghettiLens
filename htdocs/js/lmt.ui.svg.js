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
svg.init = function() {
	var parent = document.getElementById("inp");
	svg.root = document.createElementNS(svg.ns, "svg");
	
	svg.root.setAttribute("version", "1.2");
		
	// create the layers
	svg.layer = {};

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

	svg.root.appendChild(svg.layer.zoompan);
	
	parent.appendChild(svg.root);
	
	
	
}


/**
 * initialises the background images
 * sets up the filter chain for correct blending 
 */
svg.initBG = function(urls) {
	var rect = document.createElementNS(svg.ns, "rect");
	
	rect.setAttribute('x', '0px');
	rect.setAttribute('y', '0px');
	rect.setAttribute('width', '100%');
	rect.setAttribute('height', '100%');
	rect.setAttribute('fill', 'black');
	
	
	svg.layer.bg.appendChild(rect);
}


/**
 * event handlers for interaction with the svg canvas 
 */
svg.events = {
	state: 'none', //none, drag, pan
	dragTarget: null,
	preventClick: false,
	someElementWasDragged: false,
	
	
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
	  	//TODO panning logic, use SVGPan library as vorlage
	  	/*
	  	var p = LMT.ui.svg.coordTrans(evt).matrixTransform(svg.events.stateTf);
			svg.setCTM(svg.layer.zoompan, svg.events.stateTf.inverse().translate(p.x - svg.events.stateOrigin.x, p.y - svg.events.stateOrigin.y));
			*/
			//var x = LMT.settings.display.zoompan.x + evt.screenX - svg.events.stateOrigin.x;
			//var y = LMT.settings.display.zoompan.y + evt.screenY - svg.events.stateOrigin.y;
			svg.events.newState = {	x: LMT.settings.display.zoompan.x + dx,
															y: LMT.settings.display.zoompan.y + dy,
															scale: LMT.settings.display.zoompan.scale};
			/*
			LMT.settings.display.translate.x += translate.x;
			LMT.settings.display.translate.y += translate.y;
			*/
			svg.setTransform(svg.layer.zoompan, svg.events.newState);
			
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
			//actionstack.push(model);
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
		
		// delegate click on middle button
		// 1 according to w3c, 4 according to ms... (but this time, the ms solution is actually better...)
		if (evt.button == 1 || evt.button == 4) {
			svg.events.onMiddleClick(evt);
			return;
		}
		
	  var target = evt.target;
	  var parent = evt.target.parentElement;
	  
	  var somethinghappend = false;
	  
	  //click on background
		if ( target.id == 'svgroot' || parent.id == 'bg') {
			
      var coord = svg.coordTrans(evt);			
			
			if (LMT.settings.mode == 'image') {
				createRootPoint(coord.x, coord.y);
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
      if (pnt.isExpanded) {
        collapsePoint(pnt);
	    }
      else {
        expandPoint(pnt);
      }
      somethinghappend = true;
  	}
  	
  	//is it something with an assigned js object? (rulers, pointmasses)
  	else if (target.jsObj) {
  		target.jsObj.remove();
      somethinghappend = true;
  	}


	  //push the new model to the undo / action stack
	  if (somethinghappend) {
	  	//actionstack.push(model);
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
		LMT.settings.display.zoompan.scale *= 1 + delta*0.1;
		svg.setTransform(svg.layer.zoompan, LMT.settings.display.zoompan);
		
		if (evt.stopPropagation) {evt.stopPropagation();}
		if (evt.preventDefault) {evt.preventDefault();}
		
	},

	/**
	 * reset zoom and pan to default
	 */	
	onMiddleClick: function(evt) {
		LMT.settings.display.zoompan = {x:0, y:0, scale:1};
		svg.setTransform(svg.layer.zoompan, LMT.settings.display.zoompan);
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

	/*
  var m = evt.target.getScreenCTM();
  var p = svg.root.createSVGPoint(); 

  p.x = evt.clientX;
  p.y = evt.clientY;
  p = p.matrixTransform(m.inverse());
  p.x = Math.round(p.x);
  p.y = Math.round(p.y);

	log.write(''+p.x+' / '+p.y);
	*/
	
	var pt = svg.root.createSVGPoint();
	pt.x = evt.clientX;
	pt.y = evt.clientY;
	var globalPoint = pt.matrixTransform(svg.root.getScreenCTM().inverse());
	var globalToLocal = svg.layer.zoompan.getTransformToElement(svg.root).inverse();
	var inObjectSpace = globalPoint.matrixTransform( globalToLocal );
	
  return inObjectSpace;
}


/**
 * Sets the current transform matrix of an element.
 */
/* OUTDATED
svg.setCTM = function(element, matrix) {
	var s = "matrix(" + matrix.a + "," + matrix.b + "," + matrix.c + "," + matrix.d + "," + matrix.e + "," + matrix.f + ")";

	element.setAttribute("transform", s);
}
*/

/**
 * sets the translate / scale values of the zoompan layer (ie the whole svg canvas) 
 */
svg.setTransform = function(element, state) {

	var s = "translate(" + (state.x) + "," +
												 (state.y) + ") " + 
					"scale(" + state.scale + ")";
	element.setAttribute("transform", s);
	LMT.objects.Ruler.r = {	mid:    LMT.objects.Ruler.r_def.mid * 1/state.scale,
													handle: LMT.objects.Ruler.r_def.handle * 1/state.scale};
}


LMT.ui.svg = svg;


/*})();*/
