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

  ui.settingstab.init();  
}


ui.st = {
	onclick: {
		displaySettings: function(evt) {
			alert('clicked display settings');
		},
	},
} 