/**
 * creates and handles the Un/ReDo buttons
 * in the bottom right
 */



function init_UnReDoBtns() {
	ui.unredobtns = new Widget(
		"actionMenu",
		"demo-ui.svg.xxdo.svg",
		10, 10,
		Widget.h_pos.left | Widget.v_pos.top,
		Widget.Animation(Widget.aniType.none)
	);

  ui.unredobtns.addHandler("undo", Widget.event.click, ui.do.onclick.undo);
  ui.unredobtns.addHandler("redo", Widget.event.click, ui.do.onclick.redo);

	ui.unredobtns.addHandler("_init", Widget.event.init, ui.do.oninit);

  ui.unredobtns.init();  
}


ui.do = {
	oninit: function() {
		$sel.redoBtn = ui.unredobtns.buttons.redo;
		$sel.undoBtn = ui.unredobtns.buttons.undo;
		
		ui.unredobtns.buttons.undo.setAttribute('class', 'invisible');
		ui.unredobtns.buttons.redo.setAttribute('class', 'invisible');
	},
	
	onclick: {
		
		undo: function(evt) {
	    var m = actionstack.undo();
	    if (m) { //if valid return value (a model from stack) 
	    	//delete old
	    	model.remove();
	    	//install new
	    	model = m;
	    }
		},
		
		
		redo: function(evt) {
	    var m = actionstack.redo();
	    if (m) { //if valid return value (a model from stack) 
	    	//delete old
	    	model.remove();
	    	//install new
	    	model = m;
	    }
		},
		
		
		
	},
} 