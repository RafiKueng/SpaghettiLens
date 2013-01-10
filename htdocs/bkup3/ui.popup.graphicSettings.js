/**
 * creates and handles the popup for agjusting the graphics settings
 */



function init_Popup_GraphicsSettings() {
	ui.popup.graphicssettings = new Widget(
		"PopupGraphicsSettings",
		"GraphicsSettings.svg",
		0, 0,
		Widget.h_pos.mid | Widget.v_pos.mid,
		Widget.Animation(Widget.aniType.none)
	);
	
	var gs = ui.popup.graphicssettings;
	var _gs = ui.popup._graphicssettings;
	var evnts =  Widget.event;

  //ui.popup.graphicssettings.addHandler("DisplayContourLines",  Widget.event.click, ui.popup._displaysettings.onclick.dispContLine);
  
  gs.addHandler("AdjBrightness",  evnts.mousedown, _gs.onmousedown);
  gs.addHandler("AdjContrast",  evnts.mousedown, _gs.onmousedown);
  gs.addHandler("AdjBrightness",  evnts.mouseup, _gs.onmouseup);
  gs.addHandler("AdjContrast",  evnts.mouseup, _gs.onmouseup);


  gs.addHandler("_all", Widget.event.mousemove, _gs.onmousemove);
  gs.addHandler("_all", Widget.event.mouseout, _gs.onmouseout);
  gs.addHandler("_all", Widget.event.mouseup, _gs.onmouseup);

  gs.addHandler("_init", Widget.event.init, _gs.oninit);
  
  gs.init();
  gs.hide();
  
}


/**
 * just a random object to store the functions
 * those are only used direcly above 
 */
ui.popup._graphicssettings = {
	
	oninit: function() {
		var _this = ui.popup.graphicssettings;
		var _that = ui.popup._graphicssettings;
		
		_that.movetarget = null;

		// top position of slider .slideMax has smaller y coordines on screen!
		var range = null;
		for (var i = 0; i < _this.bg.childNodes.length; ++i) {
			if (_this.bg.childNodes[i].id=='range0') {
				range = _this.bg.childNodes[i];
				break;
			}			
		}
		if (!range) {alert('ERROR: no range slider found');return;}
		
		_that.slideHeight = parseInt(range.getAttribute('height'));
		_that.slideMax = parseInt(range.getAttribute('y'));
		_that.slideMin = parseInt(range.getAttribute('y')) + parseInt(range.getAttribute('height'));
		
		_that.slideDy = _that.slideMin - _that.slideMax;
		_that.btnDy = _this.buttons["AdjBrightness"].height.baseVal.value;

		_this.buttons["AdjBrightness"].setAttribute('y', _that.slideMax-_that.btnDy/2+_that.slideDy*model.brightness);
		_this.buttons["AdjContrast"].setAttribute('y', _that.slideMax-_that.btnDy/2+_that.slideDy*model.contrast);

		//init the colorpicker / channel
		var colorspace = _this.special.colorspace.firstChild;
		var n = model.channels.length;
		
		var x = parseInt(colorspace.getAttribute('x'));
		var y = parseInt(colorspace.getAttribute('y')) - 100;	
		var dx = parseInt(colorspace.getAttribute('width')) / n;
		var dy = 50;

		_that.bcs = [];
		for (var i=0; i<n; ++i){
			var bcs = new BandColorSelector(model.channels[i], x+i*dx, y, dx, dy, colorspace, _this.grp);
			bcs.init();
			_that.bcs.push(bcs)
			bcs.circ.onmousedown = _that.onmousedown;
			bcs.circ.onmouseup = _that.onmouseup;
		}
		
		_this.catchMouseMove(false);
		
	},
	
	onmouseout: function(evt) {
		var _this = ui.popup.graphicssettings;
		var _that = ui.popup._graphicssettings;
		
		var tmp1 = evt.target == _this.bg;
		var tmp2 = evt.rangeParent == $sel.svg;
		
		if (evt.rangeParent == $sel.svg) {
			_that.movetarget = null;
			_this.catchMouseMove(false);
			_this.hide();
		}
	},
	
	onmousedown: function (evt) {
		var _this = ui.popup.graphicssettings;
		var _that = ui.popup._graphicssettings;
		
		//var tmp = evt;
		_that.movetarget = evt.target;
		_this.catchMouseMove(true);
		
		
	  evt.stopPropagation();
		evt.preventDefault();
	},
	
	onmousemove: function(evt) {
		var _this = ui.popup.graphicssettings;
		var _that = ui.popup._graphicssettings;
		
		if (_that.movetarget) {

			var svgpnt = coordTrans(evt);

			switch (_that.movetarget.id.substring(0,3)) {
				case 'Adj':
					var slide_pos_y = svgpnt.y;
					
					//remember Max pos has the lowest y value
					var snapdist = 5;
					if (slide_pos_y < _that.slideMax+snapdist) {
						slide_pos_y = _that.slideMax;
					}
					else if (slide_pos_y > _that.slideMin-snapdist) {
						slide_pos_y = _that.slideMin;
					}
					else if (Math.abs(slide_pos_y - (_that.slideMax+_that.slideMin)/2 )< snapdist ) {
						slide_pos_y = (_that.slideMax + _that.slideMin)/2;
					}
					
					slide_pos_y -= _that.btnDy/2;
					
					var slideval = (slide_pos_y + _that.btnDy/2 - _that.slideMax) / _that.slideDy;
					
					var str = _that.movetarget.id.substring(3).toLowerCase();
					model[str] = slideval;
					
					_that.movetarget.setAttribute('y', slide_pos_y);
					
					break;
				case 'bcs':
					_that.movetarget.jsClass.update(svgpnt.x, svgpnt.y);
					break;

				default:
					alert('unknown string in ui.popup.graphics.onmousemove: ' + _that.movetarget.id.substring(4));
					break;
			}

			dbg.write(slideval);
		  evt.stopPropagation();
		  evt.preventDefault();
		}
	},
	
	onmouseup: function (evt) {
		var _this = ui.popup.graphicssettings;
		var _that = ui.popup._graphicssettings;
		
		switch (_that.movetarget.id.substring(0,3)) {
			case 'bcs':
			case 'Adj':
				canvas.repaint();
		}
		
		_that.movetarget = null;
		_this.catchMouseMove(false);
	},
	
	onclick: {
	
	}
}



