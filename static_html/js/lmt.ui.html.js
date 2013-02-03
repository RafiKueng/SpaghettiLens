/**
 * 
 */
/*(function(){*/


var html = {};




html.fire = function(evt){
	
}




html.Toolbar = {
  init: function() {
  
  	$("#toolbarGrp1 button")
  	 .add("#toolbarGrp1 input")
  	 .add("#top button")
  	 .each(function(){
  		
  		var $this = $(this);
  		var icon = $this.data("icon");
  		var eventName = $this.data("event");
  		var value = $this.data("value");
  		
  		$(this).button({
  			text: false,
  			disabled: false,
  			icons: {primary: icon }
  		})
  		.on('click', {name:eventName, value: value} , LMT.ui.html.Toolbar.fire);
  	});
  
  	$("#toolbarGrp1 > .btnset").buttonset();

    //set buttons to correct state 
    
    //mode radio buttons	
    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
    $('input[name="mode"]').change();
    
    //un/re do buttons:
    $('#btnInUndo').add('#btnInRedo').button("disable");
    
  },
  
  /**
   * updates the buttons
   */
  update: function(evt) {
    //radiobuttons for mode selection 
    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
    $('input[name="mode"]').change();
    // un / redo buttons whether there is something to be undone / redone
    $('#btnInUndo').button(LMT.actionstack.undoSize>0 ? "enable" : "disable");
    $('#btnInRedo').button(LMT.actionstack.redoSize>0 ? "enable" : "disable");
  },
  
  /**
   * fires an event when a toolbar button is pressed 
   */
  fire: function(evt){
    $.event.trigger(evt.data.name, evt.data.value);
  }
}



html.ColorSettingsDialog = {
  init: function(){	
	
  		// multiply the color settings tools for n channels
  	var $parent = $('#color_dialog');
  	var $elem = $("#csettings_ch0");
  	var ch = LMT.modelData.ch;
  	
  	for (var i = 1; i<ch.length; i++){
  		$clone = $elem.clone(true, true);
  		$clone.find('*').data('id', i);
  		$clone.appendTo($parent);
  	}
  	
  	
  	// color picker dialog
  	$('#color_dialog').dialog({
  		autoOpen: false,
  		minWidth: 500,
  		open: function(){
  			 $('.mycp').each(function(i, val){
  			   	var str = (1 << 24) | (ch[i].r*255 << 16) | (ch[i].g*255 << 8) | ch[i].b*255;
  			 		$(this).val('#' + str.toString(16).substr(1)).focus();
  			 		
  			 		// hack that should update the field so they get their color from beginning
  			 		var press = jQuery.Event("keyup");
  					press.ctrlKey = false;
  					press.which = 13;
  					$(this).trigger(press);
  			 });
  		}
  	});
  	
  	
  	//sliders
  	$('.slider').slider({
  		max: 1,
  		min: -1,
  		value: 0,
  		step: 0.05,
  		stop: function(evt, ui) {
  			var value = ui.value;
  			var type = $(this).data("type");
  			var id = $(this).data("id");
  			
  			if (type=="contrast"){
  				value = Math.pow(10, value); //change range from [-1...1] to [0.1 ... 10]
  			}
  			
  			LMT.modelData.ch[id][type.substr(0,2)] = value;
  			log.write("stopped sliding");
  			$.event.trigger('ChangedModelData', id);
  		}
  		
  	});
	
  	$('.mycp').colorpicker({
  		parts: ['header',
  			'map',
  			'bar',
  			//'hex',
  			//'hsv',
  			//'rgb',
  			//'alpha',
  			//'lab',
  			//'cmyk',
  			//'preview',
  			'swatches',
  			'footer'],
  		colorFormat: '#HEX',
  		showOn: 'both',
  		buttonColorize: true,
  		altField: '',
  		buttonImage: 'img/cp/ui-colorpicker.png',
  		buttonImageOnly: false,
  		buttonText: 'pick',
  		showOn: 'button',
  		close: function(evt, data){
  			var id= $(this).data("id");
  			$(this).css('background', data.formatted);
  			LMT.modelData.ch[id].r = data.rgb.r;
  			LMT.modelData.ch[id].g = data.rgb.g;
  			LMT.modelData.ch[id].b = data.rgb.b;
  			log.write("picked color for "+id);
  			$.event.trigger('ChangedModelData', id);
  		},
  	});
  	
  	$parent.removeClass("initHidden");
  	
  },
  
  show: function(){
    $('#color_dialog').dialog("open");
  }
  
  
  
}
  	
	
	
html.DisplaySettingsDialog = {

  init: function(){
  
  	/**********************
  	 * the display settings dialog 
  	 */
  	$("#display_dialog").dialog({
  		autoOpen: false,
  		minWidth: 700,
  		open: function(){ //update button status
  			// .change is a bugfix, as described here: http://stackoverflow.com/questions/8796680/jqueryui-button-state-not-changing-on-prop-call
  			$('#conn_l').prop("checked", LMT.settings.display.paintConnectingLines).change();
  			$('#cont_p').prop("checked", LMT.settings.display.paintContourPoints).change();
  			$('#cont_l').prop("checked", LMT.settings.display.paintContours).change();
  		}
  	});
  	
  	$('#dsettings').buttonset();
  	
  	$('#conn_l').click(function(evt){
  		LMT.settings.display.paintConnectingLines = this.checked;
  		log.write('toggle 1' + this.checked);
  		$.event.trigger('RepaintModel');
  	});
  	$('#cont_p').click(function(evt){
  		LMT.settings.display.paintContourPoints = this.checked;
  		log.write('toggle 2');
  		$.event.trigger('RepaintModel');
  	})
  	$('#cont_l').click(function(){
  		LMT.settings.display.paintContours = this.checked;
  		log.write('toggle 3');
  		$.event.trigger('RepaintModel');
  	});
  	
  	$("#display_dialog").removeClass("initHidden");
  	
	},
	
	show: function() {
	  $('#display_dialog').dialog("open");
	}
}
	





html.Tooltip = {
  
  init: function(){
    
    //prepare tooltip div 
    document.getElementById('popup').style.display = 'block';
    //on mouse enter tooltip: cancle fade out animation, display till mouseleave 
    $("#popup").on('mouseenter', function(evt){
      $("#popup").stop(true, true).fadeIn(200);
    });
    $("#popup").on('mouseleave', function(evt){
      $("#popup").stop(true, true).fadeOut(50);
    });
    $("#popup").hide();
  }, 
  
  
  
  show: function(evt, orgEvt, data){
  	var offset = {top: 5, left: 5};
  	var newcss = {};
  	$("#popup > #text").html(data.txt);
  	$("#popup > #link").html(data.link);
  	$("#popup > #hotkey").html(data.hotkey);
  
  	//make change style to get position / width ect...
  	$("#popup").css({visibility: 'hidden'}).show();
  	
  	//calculate position
  	var top = orgEvt.pageY;
  	var left = $(orgEvt.currentTarget).offset().left;
  	var inpY = $('#inp').offset().top;
  
  	left = left + $(orgEvt.currentTarget).outerWidth()/2;
  	
  	//check if out of screes
  	var inpR = $('#inp').offset().left + $('#inp').outerWidth(true);
  	var sizeX = $("#popup").outerWidth(true);
  	
  	/*
  	newcss["border-top-left-radius"] = 0;
  	newcss["border-top-right-radius"] = '5px';
  	*/
  	if (left+sizeX>inpR-20) {
  		left = left - sizeX;
  		//newcss["border-top-left-radius"] = '5px';
  		//newcss["border-top-right-radius"] = 0;
  		$("#popup").addClass('right').removeClass('left');
  	}
  	else {
  		$("#popup").addClass('left').removeClass('right');
  	}
  	
  	newcss.left = left+offset.left,
  	newcss.top= inpY+offset.top;
  	newcss.visibility = 'visible';
  	
  	$("#popup").css(newcss).hide();
  	
  	$("#popup").stop(true, true).fadeIn(200);
  },
  
  
  hide: function(){
  	$("#popup").stop(true, true).fadeOut(600);
  }
}



html.KeyboardListener = {
  init: function(){
    $('body').on('keypress', LMT.ui.html.KeyboardListener.keyEvent);
  },
  
  keyEvent: function(evt){
    var code = event.which || event.keyCode;
    log.write("keycode: "+code);
    
    switch (code) {
      case 13: //enter and numEnter
      case 48:
      case 96: //num0
        $.event.trigger("ZoomPanReset");
        break;
      
      case 43: //num+
        $.event.trigger("Zoom", [+1]);
        break;
      default:
        return;
    }
    if (evt.stopPropagation) {evt.stopPropagation();}
    if (evt.preventDefault) {evt.preventDefault();}
  }
}



LMT.ui.html = html;

/*})();*/