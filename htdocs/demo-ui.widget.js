

/**
 *	This initialises and returns a new UI Widget designed in svg
 * 	(buttons)
 * 	make sure the svg contains two layers with id layer1 and layer2
 * 	layer1: conains all the background
 *  layer2: contains as children all the buttons
 * 		each button is a group with at least children[0]
 * 
 * ******************
 * 
 * create a new widget
 * 
 * 	myWidget = new Widget(name, pathToSVG, dx, dy, positioning)
 * 
 * with dx, dy: x/y coordinates (either rel or abs)
 * positioning = Widget.h_pos.left | Widget.v_pos.top;
 * 
 * *******************
 * 
 * then add the function handlers, according to the buttons names
 * from the svg file (id attribute) to an event type (widget.event)
 * 
 * myWidget.addHandler('buttonID', eventtype, func);
 * 
 * the callback function is called with the svg button element as this
 * to change a style of a button you could use:
 * 
 * var func = function(evt) {this.style.fill = '#0000ff';}
 * 
 * you can add events to the background (id bg) too
 * 
 * var eventtype = 
 * 
 * ***********************
 * 
 * and then initalise it
 * myWidget.init();
 * 
 *  
 * @param {Object} name
 * @param {Object} path
 * @param {Object} x
 * @param {Object} y
 * @param {Object} positioning optional positioning object (default absolute pos)
 */
function Widget(name, path, x, y, positioning) {
	this.name = name;
	this.path = path;
	this.x = x;
	this.y = y;
	this.pos = positioning || 0;
	
	this.grp = null; //the whole group with all the layout elements
	this.bg = null;
	this.btns = null;
	
	this.handlers = {}; //the handlers to be added
}


Widget.prototype.init = function() {
	
	//this fnc makes sure, that addToDOM of/on this element is called
	var fnc = (function (obj) {
		return function(svgDoc) {
			obj.addToDOM(svgDoc)
		}
	})(this)
	
	importSVG(this.path, fnc);
}


/**
 *	will be called automatically by init upon load complete of svg object
 * selects the needed layers from the loaded svg and imports it to
 * the ui
 * 
 * addiditionally sets the handlers for the buttons
 */
Widget.prototype.addToDOM = function(svgDoc) {
	//alert('got svg doc');

	this.grp  = document.createElementNS("http://www.w3.org/2000/svg", "g");

	this.bg   = svgDoc.getElementById('layer1'); //background layer
	this.btns = svgDoc.getElementById('layer2'); //buttons layer
	
	//debug
	if (!this.bg) {
		var xx = 1;
	}
	
	this.grp.appendChild(this.bg);
	this.grp.appendChild(this.btns);
	
	
	//register the handlers for the buttons previously added by addHandler
	// look for each button whether there is an event handler
	var children = this.btns.children;
	var log = "";
	
	this.buttons = {};
	
	for (var i=0; i<children.length; ++i){
		var child = children[i];
		this.buttons[child.id] = child;
		
		// save .bg for easy access and styling
		if (child.children[0]) { //if child is a group and has at least one child (the backgroubd)
			this.buttons[child.id]['bg'] = child.children[0]; // expose a bg element
		}
		else { //child is a simple svg figure (rectangle?)
			this.buttons[child.id]['bg'] = child[0];
		}
		
		// set class, remove styles that are taken care of by css
		this.buttons[child.id]['bg'].style.fill = '';
		this.buttons[child.id]['bg'].setAttribute('class', 'btn');
		
		
		if (this.handlers[child.id]) {
			if (this.handlers[child.id][Widget.event.click]) {child.onclick = this.handlers[child.id][Widget.event.click];}
			if (this.handlers[child.id][Widget.event.mouseover]) {child.onmouseover = this.handlers[child.id][Widget.event.mouseover];}
			if (this.handlers[child.id][Widget.event.mouseout]) {child.onmouseout = this.handlers[child.id][Widget.event.mouseout];}
			if (this.handlers[child.id][Widget.event.mousemove]) {child.onmousemove = this.handlers[child.id][Widget.event.mousemove];}
		}
		else {
			log += "no event handler for: " + child.id+'<br>';
		}
	}
	dbg.write(log);

	
	//add handler to the background
	if (this.handlers['bg']){
		if (this.handlers['bg'][Widget.event.click]) {this.bg.onclick = this.handlers['bg'][Widget.event.click];}
		if (this.handlers['bg'][Widget.event.mouseover]) {this.bg.onmouseover = this.handlers['bg'][Widget.event.mouseover];}
		if (this.handlers['bg'][Widget.event.mouseout]) {this.bg.onmouseout = this.handlers['bg'][Widget.event.mouseout];}
		if (this.handlers['bg'][Widget.event.mousemove]) {this.bg.onmousemove = this.handlers['bg'][Widget.event.mousemove];}
		
		// run init handler
	}
	
	//run init handler
	if (this.handlers['_init']){
		this.handlers['_init'][Widget.event.init](null);		
	}

	//move to the right place
	var x = 0;
	var y = 0;

	//widgets dimensions
	var w_w = svgDoc.documentElement.width.baseVal.value;
	var w_h = svgDoc.documentElement.height.baseVal.value;

	//parent dimensions	
	var p = $sel.svg; //get the parent element
	var p_w = p.width.baseVal.value;
	var p_h = p.height.baseVal.value;
	
	//first vertical (bitwise op: 3 = 0b0011 gets the last 2 binary digits)
	switch (this.pos & 3) {
		case Widget.v_pos.abs:
		case Widget.v_pos.top:
			y = this.y;
			break;
		case Widget.v_pos.mid:
			y = p_h / 2 - w_h / 2 + this.y;
			break;
		case Widget.v_pos.bot:
			y = p_h - w_h + this.y;
			break;
	};

	// ...and horizontally (12 = 0b1100)
	switch (this.pos & 12) {
		case Widget.h_pos.abs:
		case Widget.h_pos.left:
			x = this.x;
			break;
		case Widget.h_pos.mid:
			x = p_w / 2 - w_w / 2 + this.x;
			break;
		case Widget.h_pos.right:
			x = p_w - w_w + this.x;
			break;
	};
	
	var tmp = 3;
	this.grp.setAttribute('transform', 'translate(' + x + ',' + y + ')');
		
	$sel.svguiLayer.appendChild(this.grp);		
}

 
Widget.prototype.addHandler = function(name, eventtype, fnc) {
	if ( ! this.handlers[name] ){
		this.handlers[name] = {};
	}
	this.handlers[name][eventtype] = function (evt) {
		fnc.apply(this, evt);
		if (evt) {
			evt.stopPropagation();
		}
	}
}



Widget.prototype.move = function(x,y) {
	this.x = x;
	this.y = y;
	this.grp.setAttribute('transform', 'translate(' +this.x + ',' + this.y + ')');
}



/**
 * some definitions / constants for easy use 
 */
Widget.event = {
	init:     -1,
	click:     0,
	mouseover: 1,
	mouseout:  2,
	mousemove: 3
}

/**
 * the positioning of the widget.
 * if absolute, x/y are abolute, otherwise rel to the corresponding corner
 * first 2 bits represent vertical, second 2 horizontal orientation 
 * 
 * assign pos like:
 * pos = Widget.v_pos.bot | Widget.h_pos.right;
 */
Widget.v_pos = {
	abs: 0,
	top: 1,
	mid: 2,
	bot: 3	
}

Widget.h_pos = {
	abs:   0 << 2,
	left:  1 << 2,
	mid:   2 << 2,
	right: 3 << 2
}
