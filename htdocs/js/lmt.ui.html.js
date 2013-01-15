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
 * Replace all SVG images with inline SVG
 * Source:
 * http://stackoverflow.com/questions/11978995/how-to-change-color-of-svg-image-using-css-jquery-svg-image-replacement/
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