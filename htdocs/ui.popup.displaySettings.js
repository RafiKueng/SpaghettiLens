/**
 * creates and handles the popup for agjusting the display settings
 */



function init_Popup_DisplaySettings() {
	ui.popup.displaysettings = new Widget(
		"PopupDisplaySettings",
		"DisplaySettings.svg",
		0, 0,
		Widget.h_pos.mid | Widget.v_pos.mid,
		Widget.Animation(Widget.aniType.none)
	);

  ui.popup.displaysettings.addHandler("DisplayContourLines",  Widget.event.click, ui.popup._displaysettings.onclick.dispContLine);
  ui.popup.displaysettings.addHandler("DisplayContourPoints",  Widget.event.click, ui.popup._displaysettings.onclick.dispContPnt);
  ui.popup.displaysettings.addHandler("DisplayConnectingLines",  Widget.event.click, ui.popup._displaysettings.onclick.dispCncLine);

  ui.popup.displaysettings.addHandler("_all", Widget.event.mouseout, ui.popup._displaysettings.onmouseout);
  ui.popup.displaysettings.addHandler("_init", Widget.event.init, ui.popup._displaysettings.oninit);
  
  ui.popup.displaysettings.init();
  ui.popup.displaysettings.hide();
  
}


/**
 * just a random object to store the functions
 * those are only used direcly above 
 */
ui.popup._displaysettings = {
	
	oninit: function() {
	},
	
	onmouseout: function() {
		//ui.popup.displaysettings.hide();
	},
	
	onclick: {
	
		dispContLine: function(evt) {
			settings.paintContour = !settings.paintContour;
			model.repaint();
			var classname = settings.paintContour ? "btn active" : "btn" 
			ui.popup.displaysettings.buttons.DisplayContourLines._bg.setAttribute('class', classname);
		},
		
		dispContPnt: function(evt) {
			settings.paintContourPoints = !settings.paintContourPoints;
			model.repaint();
			var classname = settings.paintContourPoints ? "btn active" : "btn" 
			ui.popup.displaysettings.buttons.DisplayContourPoints._bg.setAttribute('class', classname);
		},
		
		
		dispCncLine: function(evt) {
			settings.paintConnectingLines = !settings.paintConnectingLines;
			model.repaint();
			var classname = settings.paintConnectingLines ? "btn active" : "btn" 
			ui.popup.displaysettings.buttons.DisplayConnectingLines._bg.setAttribute('class', classname);
		},
	}
	
	
} 