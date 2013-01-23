/**
 * 
 */
/*(function(){*/


var html = {
	
};


html.manageButtonsLeft = function() {
	
}
$(document).on('loadedButtons', html.manageButtonsLeft);


html.loader = function() {
	
}


/**
 * fires an event when a toolbar button is pressed 
 */
html.fire = function(evt){
	$.event.trigger(evt.data.name, evt.data.value);
}

html.init = function() {
	
	//////////////////
	// outdated 
	
	//add generic event handler to each button
	/*
	var btns = jQuery('.button');
	btns.each(function(){
		var $btn = $(this);
		$btn.on('click', LMT.ui.html.events.onclick);
		$btn.on('mouseenter', function(evt){
			$.event.trigger("ShowTooltip", [evt, {
				txt: $btn.data('tooltip'),
				link: $btn.data('furtherinfo'),
				hotkey: $btn.data('hotkey')
			}]);
		});
		$btn.on("mouseleave", function(evt){
			$.event.trigger("HideTooltip");
		});
	});
	*/
	
		/*	
	var btngrps = jQuery('.button_group');
	btngrps.each(function(key, value){


		var $btngrp = $(this);
		if ($btngrp.data("type") == 'expand'){
			$('.master', this).addClassSVG("hidden");
		}

	});
		*/
		/*
	$('.toolbar').each(function(){
		var tb = new Toolbar(this);
	});
	*/
	
	//----------------------------
	/*
	 * init toolbar
	 */

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
		.on('click', {name:eventName, value: value} , LMT.ui.html.fire);
	});


	$("#toolbarGrp1 > .btnset").buttonset();
	
	


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
	
	
	
	// jquery ui stuff
	////////////////////////////////////////////
	
		// multiply the color settings tools for n channels
	var $parent = $('#color_dialog');
	var $elem = $("#csettings_ch0");
	for (var i = 1; i<LMT.channels.length; i++){
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
			 		var str = (1 << 24) | (LMT.channels[i].r*255 << 16) | (LMT.channels[i].g*255 << 8) | LMT.channels[i].b*255;
			 		$(this).val('#' + str.toString(16).substr(1)).focus();
			 		var press = jQuery.Event("keyup");
					press.ctrlKey = false;
					press.which = 13;
					$(this).trigger(press);
			 });
		}
	});
	$(document).on('ShowColorSettings', function(){$('#color_dialog').dialog("open");});
	
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
			
			LMT.channels[id][type] = value;
			log.write("stopped sliding");
			$.event.trigger('UpdateBG', id);
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
			LMT.channels[id].r = data.rgb.r;
			LMT.channels[id].g = data.rgb.g;
			LMT.channels[id].b = data.rgb.b;
			log.write("picked color for "+id);
			$.event.trigger('UpdateBG', id);
		},
	});
	
	
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
	$(document).on('ShowDisplaySettings', function(){$('#display_dialog').dialog("open");});
	
	$('#dsettings').buttonset();
	
	$('#conn_l').click(function(evt){
		LMT.settings.display.paintConnectingLines = this.checked;
		log.write('toggle 1' + this.checked);
		$.event.trigger('UpdateModel');
	});
	$('#cont_p').click(function(evt){
		LMT.settings.display.paintContourPoints = this.checked;
		log.write('toggle 2');
		$.event.trigger('UpdateModel');
	})
	$('#cont_l').click(function(){
		LMT.settings.display.paintContours = this.checked;
		log.write('toggle 3');
		$.event.trigger('UpdateModel');
	});
	



  /***************
   *init main ui stuff
   * the buttons on top
   *  
   */
  

}
$(document).on('loadedButtons', html.init);
	


html.ShowTooltip = function(evt, orgEvt, data){
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
	
}
$(document).on('ShowTooltip', html.ShowTooltip);


html.HideTooltip = function(){
	$("#popup").stop(true, true).fadeOut(600);
}
$(document).on('HideTooltip', html.HideTooltip);




html.events = {

	
	
	onclick: function(evt){
		var event = $(evt.currentTarget).data("event");
		var value = $(evt.currentTarget).data("value");
		
		log.write('click on '+evt.currentTarget.id + ", firing event: " + event + "("+value+")");
		$.event.trigger(event, [value]);
		
	},
	
	
	
	onkeydown: function(evt){
		var code = event.which || event.keyCode;
		log.write("keycode: "+code);
		if (code == 13 || code == 48 || code == 96) { //enter or 0
			LMT.ui.svg.events.onMiddleClick(evt);
			if (evt.stopPropagation) {evt.stopPropagation();}
			if (evt.preventDefault) {evt.preventDefault();}
		}
	}
	
	
	
}

$('body').on('keypress', html.events.onkeydown);



/**
 * Replace all SVG images with inline SVG
 * Source:
 * http://stackoverflow.com/questions/11978995/how-to-change-color-of-svg-image-using-css-jquery-svg-image-replacement/
 * modified to keep all data-* attributes (only in jquery objects, not on dom)
 */
html.loadAllSVG = function(){
	
	var btns = jQuery('img.svg');
	LMT.ui.html.nButtons = btns.length;
	LMT.ui.buttons = [];
  
  btns.each(function(){
    var $img = jQuery(this);
    var imgID = $img.attr('id');
    var imgClass = $img.attr('class');
    var imgURL = $img.attr('src');
    var imgData = $img.data();

    jQuery.get(imgURL, function(data) {
      // Get the SVG tag, ignore the rest
      var $svg = jQuery(data).find('svg');

      // Add replaced image's ID to the new SVG
      if(typeof imgID !== 'undefined') {
          $svg = $svg.attr('id', imgID);
      }
      // Add replaced image's classes to the new SVG
      if(typeof imgClass !== 'undefined') {
          $svg = $svg.attr('class', imgClass+' replaced-svg');
      }
			
			// adds the data-* attributes to svg jquery element (NOT directly to the dom..)
			if (imgData) {
				$svg = $svg.data(imgData);
			}
			
      // Remove any invalid XML tags as per http://validator.w3.org
      $svg = $svg.removeAttr('xmlns:a');

      // Replace image with new SVG
      $img.replaceWith($svg);
      
      LMT.ui.buttons.push($svg);
      
      LMT.ui.html.nButtons--;
      if (LMT.ui.html.nButtons == 0){
      	$.event.trigger('loadedButtons');
      };
    });

  });
  
};



LMT.ui.html = html;

/*})();*/