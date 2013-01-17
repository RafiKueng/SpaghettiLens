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



intel.CreateRootPoint = function(evt, coord){
	var p = new ExtremalPoint(coord.x, coord.y);
	p.init();
	p.depth = 0;
	p.setType("min");
	p.update();
	++model.NrOf.Sources;
	model.Sources.push(p);
	model.repaint();
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