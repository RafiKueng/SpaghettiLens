/**
 * creates and handles the Settingstab
 * in the bottom right
 */



function init_SettingsTab() {
	ui.settingstab = new Widget(
		"actionMenu",
		"demo-ui.svg.settingstab.svg",
		0, 0,
		Widget.h_pos.left | Widget.v_pos.bot,
		Widget.Animation(Widget.aniType.sliding, 70,0)
	);

  ui.settingstab.addHandler("displaySettings", Widget.event.click, ui.st.onclick.displaySettings);
  ui.settingstab.addHandler("graphicsSettings", Widget.event.click, ui.st.onclick.graphicsSettings);

  ui.settingstab.init();  
}


ui.st = {
	onclick: {
		
		displaySettings: function(evt) {
			if (ui.popup.displaysettings.isShown){
				ui.st.close_all();
			}
			else {
				ui.st.close_all();
				ui.popup.displaysettings.show();
			}
		},
		
		graphicsSettings: function(evt) {
			if (ui.popup.graphicssettings.isShown){
				ui.st.close_all();
			}
			else {
				ui.st.close_all();
				ui.popup.graphicssettings.show();
			}
		},
	},
	
	
	close_all: function() {
		ui.popup.graphicssettings.hide();
		ui.popup.displaysettings.hide();
	}
	
}