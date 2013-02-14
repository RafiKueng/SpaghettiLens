/**
 * creates and handles the mode Menu
 * in the top right
 */



function init_ModeMenu() {
	ui.modeMenu = new Widget(
		"modeMenu",
		"demo-ui.svg.mode_sel.svg",
		-10, 10,
		Widget.h_pos.right | Widget.v_pos.top,
		Widget.Animation(Widget.aniType.none)
	);

  ui.modeMenu.addHandler("massMode",  Widget.event.click, ui.mm.onclick.massMode);
  ui.modeMenu.addHandler("rulerMode", Widget.event.click, ui.mm.onclick.rulerMode);
  ui.modeMenu.addHandler("imageMode", Widget.event.click, ui.mm.onclick.imageMode);

  ui.modeMenu.addHandler("_init", Widget.event.init, ui.mm.oninit);
  
  ui.modeMenu.init();
}


/**
 * just a random object to store the functions
 * those are only used direcly above 
 */
ui.mm = {
	
	oninit: function() {
		  settings.mode=0;
			ui.modeMenu.buttons.imageMode._bg.setAttribute('class', 'btn active');
	},
	
	onclick: {
	
		massMode: function(evt) {
			settings.mode=1;
			ui.modeMenu.buttons.massMode._bg.setAttribute('class', 'btn active');
			ui.modeMenu.buttons.rulerMode._bg.setAttribute('class', 'btn');
			ui.modeMenu.buttons.imageMode._bg.setAttribute('class', 'btn');
		},
		
		rulerMode: function(evt) {
			settings.mode=2;
			ui.modeMenu.buttons.massMode._bg.setAttribute('class', 'btn');
			ui.modeMenu.buttons.rulerMode._bg.setAttribute('class', 'btn active');
			ui.modeMenu.buttons.imageMode._bg.setAttribute('class', 'btn');
		},
		
		imageMode: function(evt) {
			settings.mode=0;
			ui.modeMenu.buttons.massMode._bg.setAttribute('class', 'btn');
			ui.modeMenu.buttons.rulerMode._bg.setAttribute('class', 'btn');
			ui.modeMenu.buttons.imageMode._bg.setAttribute('class', 'btn active');

		}
	}
} 