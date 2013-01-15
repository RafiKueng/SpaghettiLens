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
intel.createRuler = function(evt, coord){
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
intel.createExternalMass = function(evt, coord){
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








intel.updateModel = function(evt){
	
};


/**
 * keeps track of changes
 * 
 * maintains the undo / redo function. pushes the sack each time something happend 
 */
intel.modelChanged = function(evt){
	
}



/**
 * assign the event handler 
 */


$(document).on('CreateRuler', intel.createRuler);
$(document).on('CreateExternalMass', intel.createExternalMass);



LMT.intel = intel;