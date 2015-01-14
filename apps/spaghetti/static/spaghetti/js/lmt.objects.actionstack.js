/*
 * This object represent the action stack
 * 
 * used for the undo / redo function,
 * it saves each state up to a certain number
 * 
 * it contains a doubly lined list with all string states
 * 
 *          next
 *         ---->       ---->
 *  [state]     [state]     [state]
 *        <----        <---- 
 *    ^    prev   ^           ^
 *    |           |           |
 *  tail        current     head
 * 
 *  <--- old             new --->
 * 
 *   current is the last saved action, the first one that can be returned to
 * 
 * 
 * the stack element object converts a model into string representation and
 * back
 * 
 */


function ActionStack() {
	this.current = null;
	this.head = null; // most of the time the newest action that was done\
	this.tail = null; // the oldest action in the stack
	this.undoSize = 0; //counts only how many actions can be undone (length from tail to current)
	this.redoSize = 0;
	//this.redoPossible = false;
	//this.undoPossible = false;
}



ActionStack.prototype.push = function(model) {
	var se = new StackElement(model);
	
	//update pointers
	
	if (!this.tail) { //is this the first push? special case..
	  this.tail = se;
	  this.undoSize = -1;
  }
	
	var oldnext = null;
	if (this.current){ //if stack not empty
		if (this.current.next){ //if there are some actions to be redone
			var oldnext = this.current.next;
		}
		this.current.next = se;
		se.prev = this.current;
	}
	this.current = se;
	
	// if there are any actions that could be redone, they'll be deleted after a push
	while (oldnext) { //make sure the garbage collector works, clean up all refs to non exizsting objects (this is probably not nessecairy??)
		var tmp = oldnext;
		oldnext = oldnext.next;
		tmp.prev = null;
		tmp.next = null;
	}
	this.head = this.current;
	this.redoSize=0;
	this.undoSize++;
	
	//if there are too many objects in stack, delete oldest
	if (this.undoSize > LMT.settings.nUndoActions){
		this.tail = this.tail.next;
		this.undoSize--;
	}
	
	//this.updateUIBtn();
}



ActionStack.prototype.undo = function() {
	
	var ret;
	
	//if (this.nUndoActionsPossible()>0) {
	if (this.undoSize>0 && this.current.prev) {
		//var state = this.current;
		this.current = this.current.prev;
		this.redoSize++;
		this.undoSize--;
		ret = this.current.getModel();
	}
	else {ret = null;}
	
	//this.updateUIBtn();
	
	return ret;
}



ActionStack.prototype.redo = function() {
	var ret;
	if (this.redoSize>0 && this.current.next) {
		this.current = this.current.next;
		this.redoSize--;
		this.undoSize++;
		ret = this.current.getModel();
	}
	else {ret = null;}
	
	//this.updateUIBtn();
	
	return ret;
}


/**
 * returns the number of actions that can be undone
 * 0=no undo is possible 
 */
ActionStack.prototype.nUndoActionsPossible = function() {
	//return !(this.current === null);
	return this.undoSize;
}



ActionStack.prototype.nRedoActionsPossible = function() {
	//return !(this.current === this.head);
	return this.redoSize;
}



/**
 * This updates the display of the accoring UI buttons
 */
/*
ActionStack.prototype.updateUIBtn = function() {
	
	if (!$sel.undoBtn | !$sel.redoBtn ) {return;} // the buttons are not yet loaded
	 
	if (this.nUndoActionsPossible()>1) {
		$sel.undoBtn.setAttribute("class", "btn");
	}
	else {
		$sel.undoBtn.setAttribute("class", "btn invisible");
	}
	if (this.nRedoActionsPossible()>0) {
		$sel.redoBtn.setAttribute("class", "btn");
	}
	else {
		$sel.redoBtn.setAttribute("class", "btn invisible");
	}
}
*/


/*********************
 * static functions 
 */

/**
 * event handlers
 */
ActionStack.SaveModelState = function(evt) {
  LMT.actionstack.push(LMT.model);
  $.event.trigger("ActionStackUpdated");
}
ActionStack.Undo = function(evt) {
  var m = LMT.actionstack.undo();
  if (m) {
    LMT.model.remove();
    LMT.model = m;
    $.event.trigger("UpdateRepaintModel");
    $.event.trigger("ActionStackUpdated");
    return true;
  }
  else {
    log('ActionStack | undo | failed');
    return false;
  }
}
ActionStack.Redo = function(evt) {
  var m = LMT.actionstack.redo();
  if (m) {
    LMT.model.remove();
    LMT.model = m;
    $.event.trigger("UpdateRepaintModel");
    $.event.trigger("ActionStackUpdated");
    return true;
  }
  else {
    log('ActionStack | Redo | failed');
    return false;
  }}




/**
 * this expects and returns Model-objects
 * saves them internally as JSON strings 
 * @param {Object} model
 */

function StackElement(model) {
	this.stateStr = model.getStateAsString();
	this.prev = null;
	this.next = null;
}


StackElement.prototype.getModel = function(){
	return Model.getModelFormJSONString(this.stateStr);
}


LMT.objects.ActionStack = ActionStack;
LMT.objects.StackElement = StackElement;
