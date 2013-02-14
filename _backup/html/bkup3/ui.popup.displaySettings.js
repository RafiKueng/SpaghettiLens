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
	
	var ds = ui.popup.displaysettings;
	var _ds = ui.popup._displaysettings;
	var evnts =  Widget.event;

  ds.addHandler("DisplayContourLines",  evnts.click, _ds.onclick.dispContLine);
  ds.addHandler("DisplayContourPoints",  evnts.click, _ds.onclick.dispContPnt);
  ds.addHandler("DisplayConnectingLines",  evnts.click, _ds.onclick.dispCncLine);

  ds.addHandler("_all", evnts.mouseout, _ds.onmouseout);
  ds.addHandler("_init", evnts.init, _ds.oninit);
  
  ds.init();
  ds.hide();
  
}


/**
 * just a random object to store the functions
 * those are only used direcly above 
 */
ui.popup._displaysettings = {
	
	oninit: function() {
	},
	
	onmouseout: function(evt) {
		var _this = ui.popup.displaysettings;
		var _that = ui.popup._displaysettings;
		
		if (evt.rangeParent == $sel.svg) {
			_this.hide();
		}
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