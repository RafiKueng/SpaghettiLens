/**
 * creates and handles the mode Menu
 * in the top right
 */



function init_ModeMenu() {
	ui.modeMenu = new Widget("modeMenu", "demo-ui.svg.mode_sel.svg", 0, 0, Widget.h_pos.right | Widget.v_pos.top);

  ui.modeMenu.addHandler("massMode",  Widget.event.click, ui.mm.onclick.massMode);
  ui.modeMenu.addHandler("rulerMode", Widget.event.click, ui.mm.onclick.rulerMode);
  ui.modeMenu.addHandler("imageMode", Widget.event.click, ui.mm.onclick.imageMode);

  ui.modeMenu.addHandler("_init", Widget.event.init, ui.mm.oninit);
  
  ui.modeMenu.init();
}


ui.mm = {
	
	oninit: function() {
		  settings.mode=0;
			ui.modeMenu.buttons.massMode.children[0].style.fill = "#0000ff";
			ui.modeMenu.buttons.rulerMode.children[0].style.fill = "#0000ff";
			ui.modeMenu.buttons.imageMode.children[0].style.fill = "#aaaaff";	
	},
	
	onclick: {
		bg: function(evt) {alert('click on bg');},
		
		massMode: function(evt) {
			settings.mode=1;
			ui.modeMenu.buttons.massMode.children[0].style.fill = "#aaaaff";
			ui.modeMenu.buttons.rulerMode.children[0].style.fill = "#0000ff";
			ui.modeMenu.buttons.imageMode.children[0].style.fill = "#0000ff";
		},
		
		rulerMode: function(evt) {
			settings.mode=2;
			ui.modeMenu.buttons.massMode.children[0].style.fill = "#0000ff";
			ui.modeMenu.buttons.rulerMode.children[0].style.fill = "#aaaaff";
			ui.modeMenu.buttons.imageMode.children[0].style.fill = "#0000ff";
		},
		
		imageMode: function(evt) {
			settings.mode=0;
			ui.modeMenu.buttons.massMode.children[0].style.fill = "#0000ff";
			ui.modeMenu.buttons.rulerMode.children[0].style.fill = "#0000ff";
			ui.modeMenu.buttons.imageMode.children[0].style.fill = "#aaaaff";
		}
		
	}		

} 