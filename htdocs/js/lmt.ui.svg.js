/*************************************
 * lmt.ui.svg.js
 * this takes care of all the svg ui interactions
 * 
 *  
 */
/*(function(){*/


var svg = {
	ns: "http://www.w3.org/2000/svg",
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
	svg.layer.bg.setAttribute('id', 'bg');

	svg.layer.bg.setAttribute('onclick', 'LMT.ui.svg.events.onClick(evt);');
	
	
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
	rect.setAttribute('width', '500px');
	rect.setAttribute('height', '300px');
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
		}
	
	},
	
	
	
	onMouseMove: function(evt) {
	  evt.stopPropagation();
	  evt.preventDefault();
	  
	  if (svg.events.state == 'drag') {
	    var coord = coordTrans(evt);
			svg.events.dragTarget.jsObj.move(coord);

			svg.events.someElementWasDragged = true;
	  	svg.events.preventClick = true;
	  }
	  
	  else if (svg.events.state == 'pan') {
	  	//TODO panning logic, use SVGPan library as vorlage
	  }


	  
	},
	
	
	
	onMouseUp: function(evt) {
		if (svg.events.someElementWasDragged) {
			actionstack.push(model);
		  evt.stopPropagation();
		  evt.preventDefault();
		}
		svg.events.someElementWasDragged = false;
	},
	
	
	
	onClick: function(evt) {
		if (svg.events.preventClick) {
			svg.events.preventClick = false;
			return;
		}
		
	  var target = evt.target;
	  var parent = evt.target.parentElement;
	  
	  var somethinghappend = false;
	  
	  //click on background
		if (evt.currentTarget.id == 'bg') {
			
      var coord = svg.coordTrans(evt);			
			
			if (LMT.settings.mode == 'image') {
				createRootPoint(coord.x, coord.y);
			}
			
			else if (LMT.settings.mode == 'mass') {
 				var newElem = new ExtMass(coord.x, coord.y, 30);
			  newElem.update();
			  newElem.paint();
			}
			
			else if (LMT.settings.mode == 'ruler') {
	      var newElem = new Ruler(coord.x, coord.y, 30);
			  newElem.update();
			  newElem.paint();
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
  		jsObj.remove();
      somethinghappend = true;
  	}


	  //push the new model to the undo / action stack
	  if (somethinghappend) {
	  	actionstack.push(model);
	  } 
	}
}
	
	
svg.coordTrans = function(evt) {

  var m = evt.target.getScreenCTM();
  var p = svg.root.createSVGPoint(); 

  p.x = evt.clientX;
  p.y = evt.clientY;
  p = p.matrixTransform(m.inverse());
  p.x = Math.round(p.x);
  p.y = Math.round(p.y);

  return p;
}
	
LMT.ui.svg = svg;


/*})();*/
