/**
 * all the application intelligence
 * 
 * all the actions the application can do are defined here
 * 
 * this programm is event driven, so here you'll moslty react on custom events and
 * delegate the actions to the objects if nessesairy.
 * all handlers should ba attached to 'document' (but will be fired anonymously)
 *
 * note: important data is passed in the evt.data object 
 */



var intel = {};


/**
 * 
 *  
 * @param {Object} evt
 */
intel.CreateRuler = function(evt, coord){
  var newElem = new Ruler(coord.x, coord.y, 30);
  newElem.update();
  newElem.paint();
};


/**
 * creates a new external mass object
 * 
 * coord.x: x pos
 * coord.y: y pos
 */
intel.CreateExternalMass = function(evt, coord){
	var newElem = new ExtMass(coord.x, coord.y, 30);
	newElem.update();
	newElem.paint();
}



intel.CreateRootImagePoint = function(evt, coord){
	var p = new ExtremalPoint(coord.x, coord.y);
	p.init();
	p.depth = 0;
	p.setType("min");
	p.update();
	LMT.model.NrOf.Sources++;
	LMT.model.Sources.push(p);
	LMT.model.paint();
}
$(document).on('CreateRootImagePoint', intel.CreateRootImagePoint);




intel.ToggleExtremalPoint = function(evt, jsObj){
    if (jsObj.isExpanded) {
      intel.collapsePoint(jsObj);
    }
    else {
      intel.expandPoint(jsObj);
    }
}
$(document).on('ToggleExtremalPoint', intel.ToggleExtremalPoint);



/**
 *	expands an extremal point (into a saddle point and 2 children of the points former type) 
 *
 *	@param {Point} pointToExpand 
 */
intel.expandPoint = function(pointToExpand) {
	
	var dx = 50;
	var dy = 50;
	
	var p2e = pointToExpand;
	
	//claculate the new coordinates of the spawned points
  var p1x = p2e.x + dx / (p2e.depth / 3 + 1);
  var p2x = p2e.x - dx / (p2e.depth / 3 + 1);
  var pny = p2e.y + dy / (p2e.depth / 3 + 1);

	//create the points
	var child1 = new LMT.objects.ExtremalPoint(p1x, pny, p2e.depth+1, p2e.type);
	var child2 = new LMT.objects.ExtremalPoint(p2x, pny, p2e.depth+1, p2e.type);

	child1.init(p2e, child2);
	child2.init(p2e, child1);

	child1.updateCoord();
	child2.updateCoord();	
	
	pointToExpand.wasType = pointToExpand.type;
	pointToExpand.setType("sad");
	
	pointToExpand.setChildren(child1, child2);

	LMT.model.update();
	LMT.model.paint();
}


/**
 * this collapses a point and all sub points
 */
intel.collapsePoint = function(pnt) {
	
	pnt.collapse(true);
	//update is not needed here
	//model.update();
	LMT.model.repaint();
}



/**
 * An object is moved
 * jsTarget: the js object that is moved
 * svgTarget: the svg element that was actually moved
 * coord: to where (canvas coordinates)
 */
intel.MoveObject = function(evt, jsTarget, svgTarget, coord){
	
	jsTarget.move(coord, svgTarget);
}



intel.SwitchMode = function(evt, newMode){
	LMT.settings.mode = newMode;
	$.event.trigger("ModeSwitched");
	log.append("mode switched to " + newMode);
}
$(document).on('SwitchMode', intel.SwitchMode);


intel.UpdateModel = function(evt){
	
};


/**
 * keeps track of changes
 * 
 * maintains the undo / redo function. pushes the sack each time something happend 
 */
intel.ModelChanged = function(evt){
	
}



/**
 * assign the event handler 
 */


$(document).on('CreateRuler', intel.CreateRuler);
$(document).on('CreateExternalMass', intel.CreateExternalMass);
$(document).on('MoveObject', intel.MoveObject);




LMT.intel = intel;