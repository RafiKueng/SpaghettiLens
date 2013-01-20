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


html.init = function() {
	
	//add generic event handler to each button
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

		/*	
	var btngrps = jQuery('.button_group');
	btngrps.each(function(key, value){


		var $btngrp = $(this);
		if ($btngrp.data("type") == 'expand'){
			$('.master', this).addClassSVG("hidden");
		}

	});
		*/
	$('.toolbar').each(function(){
		var tb = new Toolbar(this);
	});


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
		
	}
	
	
	
	
	
}



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