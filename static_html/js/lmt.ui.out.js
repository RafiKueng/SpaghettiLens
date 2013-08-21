/*************************************
 * lmt.ui.out.js
 * takes care of the output of the images (slideshow like)
 * 
 */

/*(function(){*/

out = {
	tmp: 0,

	init: function() {
	  var that = LMT.ui.out; 

    //config
    that.$out = $("#out"),
    that.$btns = $("#btnsetOutNrNav"),
    that.$caption = null, 
    
    that.slides = [],
    that.shownImage = -1,

		that.$caption = $('<div class="slide_caption">blabla</div>');
		that.$caption.hide();
		that.$caption.appendTo(that.$out);
		that.tmp=1;
		
		
		/*
		$("#btnOutPrev").button({
			text: false,
			disabled: false,
			icons: {primary: "icon-chevron-left" },
		});
		$("#btnOutPrev").on('click', function(){$.event.trigger('DisplayOutputSlidePrev');});


		$("#btnOutNext").button({
			text: false,
			disabled: false,
			icons: {primary: "icon-chevron-right" },
		});
    $("#btnOutNext").on('click', function(){$.event.trigger('DisplayOutputSlideNext');});
    */

		/*
		$("#btnOutOverview").button({
			text: false,
			disabled: true,
			icons: {primary: "icon-th-large" },
		});
    $("#btnOutOverview").on('click', function(){$.event.trigger('DisplayOutputSlideOverview');});
		*/
		
		$("#btnsetOutNav").buttonset();
		$("#btnsetOutNav > button").button({ disabled: true });
		
		var $btn = $("#btnOutGlassConfig");
    $btn.button({
      text: false,
      disabled: false,
      icons: {primary: $btn.data("icon") },
    });
    $("#btnOutGlassConfig").on('click', function(){$.event.trigger('ShowDialogGlassSettings');});


    var $btn = $("#btnOutGraphics");
    $btn.button({
      text: false,
      disabled: true,
      icons: {primary: $btn.data("icon") },
    });
    $("#btnOutGraphics").on('click', function(){$.event.trigger($btn.data("event"));});

    $("#btnsetOutConfig").buttonset();
    
    

		
		var tmp = 1;
	},
	
	
	/**
	 * callback
	 * if a result is received, load images into dom 
	 */
	load: function(evt) {

    var that = LMT.ui.out; //since this is a callback, this is document, not this object
		that.slides = [0,1,2]; //init slides to something
		that.ctx = [0,1,2]; //canvas contexts
		that.imgData = [0,1,2]; //original raw image data
		that.img = [0,1,2]; // image objects
		var simImgs = LMT.simulationResult.imgs;
		that.shownImage = -1; 

		that.$out.empty(); //remove previous results
		that.$btns.empty(); //remove the number navigation buttons from previous results
		
		var nSimImgs = simImgs.length
		
		LMT.settings.display.out = new Array(nSimImgs);
    
    var newSimImgs = new Array(nSimImgs);

    /**
     * reoder, give names, sshortcuts, ect...
     * the key element is the type, this should never change 
     */
		$.each(simImgs, function(i, simImg){
      if (simImg.type=='cont') {
        simImg.btntxt  = 'Cont';
        simImg.title   = 'Contour Map';
        simImg.ttiptxt = 'The reconstructed contour (spaghetti) graph';
        simImg.hkey    = '2';
        simImg.order   = '1';
      }
      else if (simImg.type=='mdis') {
        simImg.btntxt  = 'Mass';
        simImg.title   = 'Mass Distribution Map';
        simImg.ttiptxt = 'Shows the distribution of the mass in the lens';
        simImg.hkey    = '3';
        simImg.order   = '2';
      }
      else if (simImg.type=='synt') {
        simImg.btntxt  = 'OSyn';
        simImg.title   = 'Original Synthetic Image';
        simImg.ttiptxt = 'Synthetic image, approximating the visual appearance of the lens';
        simImg.hkey    = '4';
        simImg.order   = '3';
      }
      else if (simImg.type=='isyn') {
        simImg.btntxt  = 'Synt';
        simImg.title   = 'Synthetic Image';
        simImg.ttiptxt = 'Interpolated synthetic image, approximating the visual appearance of the lens';
        simImg.hkey    = '1';
        simImg.order   = '0';
      }
		  
		  newSimImgs[simImg.order] = simImg;

		});
		
		//delete empy enties
		for (var i=0;i<newSimImgs.length;i++){
		  if (typeof(newSimImgs[i])=='undefined') {newSimImgs.splice(i, 1);}
		}

    LMT.simulationResult.imgs = newSimImgs;
    var simImgs = LMT.simulationResult.imgs;
		
		$.each(simImgs, function(i, simImg) {

      var imageObj = new Image();
      imageObj.onload = function(){
        // this = imageObj
        var that = LMT.ui.out; 
        
        var $div = $('<div id="slide'+ i + '" class="slide"></div>');
        $div.hide();
        var canvas = document.createElement('canvas');
        canvas.width = this.width;
        canvas.height = this.height;
        var ctx =  canvas.getContext("2d");
        
        ctx.drawImage(this,0,0);
        var data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
        
        that.ctx[i] = ctx;
        that.imgData[i] = data;
        
        var $canv = $(canvas);
        $canv.addClass("slide_img");
        $canv.appendTo($div);
        $div.appendTo(that.$out);
        that.slides[i] = $div;
        
        that.draw(i);
      };
      imageObj.src = simImg.url;
      that.img[i] = imageObj;

			var $nr = $('<input ' + 
			  'type="radio" ' +
			  'id="btnSlideRadio'+i+'" ' +
        'data-ttip-title="'+ simImg.title +'" ' +
        'data-ttip-text="'+ simImg.ttiptxt +'" ' +
        'data-hotkey="'+ simImg.hkey +'" ' +
        'data-tooltiplist="'+ simImg.ttiptxt +'" ' +  // this is legay for the helping text below
			  'name="slideNr" />'+
			  '<label for="btnSlideRadio'+i+'" title="">'+ simImg.btntxt +'</label>');
			$nr.appendTo(that.$btns);
			$nr.on('click', {id:i}, function(evt){
				$.event.trigger('DisplayOutputSlide', [evt.data.id]);
				/*
				var that = evt.data.that;
				that.show(evt.data.id);
				*/
			});
			
			LMT.settings.display.out[i] = {br:0, co:1};
			
		});
		
		$("#toolbarGrp2 label").add(".slide");
//		  .hover( function(evt){$.event.trigger('MouseEnter',evt);},
//              function(evt){$.event.trigger('MouseLeave',evt);});
		//that.$btns.children('input').button({label:null});
		that.$btns.buttonset();
		
		//reset the output color/contrast
		//LMT.settings.display.out = [{br:0, co:1},{br:0, co:1},{br:0, co:1}];
		
		
		$.event.trigger('InitTooltips'); //enable tooltips for newly created buttons
		
		$("#btnsetOutNav > button").button({ disabled: false });
		$('#btnOutGraphics').button({disabled: false});
	},
	
	
	/**
	 *actually draws the i-th image on the canvas, considering brightness und constrast settings 
	 */
	draw: function(i){
	  
	  var that = LMT.ui.out; 
    var ctx = that.ctx[i]
    var data = that.imgData[i];
	  var newImgData = ctx.createImageData(that.img[i].width, that.img[i].height); // make deep copy to operate on
	  var newData = newImgData.data; 
	  var br = LMT.settings.display.out[i].br * 255;
	  var co = LMT.settings.display.out[i].co;
	  
	  for (var i = 0; i < data.length; i += 4) {
      newData[i  ] = data[i  ] * co + br; //r
      newData[i+1] = data[i+1] * co + br; //g
      newData[i+2] = data[i+2] * co + br; //b
      newData[i+3] = data[i+3];           //a
	  }
	  
	  ctx.putImageData(newImgData, 0, 0);
	},
	
	
	/**
	 *callback 
	 *
	 *redraws current shown image 
	 */
	updateImg: function(evt){
	  LMT.ui.out.draw(LMT.ui.out.shownImage);
	},
	
	
	/**
	 * callback, displays next slide 
	 */
	next: function(evt){
	  var that = LMT.ui.out;
	  var i = that.shownImage+1;
	  if (i > that.slides.length-1) {
	    i = 0;
	  }
		LMT.ui.out.showSlide(i);
		$('input[name="slideNr"]')[i].checked = true;
		$('input[name="slideNr"]').change();
	},
	
	
	/**
	 * callback, displays prev slide 
	 */
	prev: function(evt){
    var that = LMT.ui.out;
    var i = that.shownImage-1;
    if (i < 0) {
      i = that.slides.length-1;
    }
    LMT.ui.out.showSlide(i);
    $('input[name="slideNr"]')[i].checked = true;
    $('input[name="slideNr"]').change();
	},


	
	show: function(evt, i){
		LMT.ui.out.showSlide(i);
	},
	
	/**
	 *internal, does really show the image
	 * zindex layers:
	 * 80 default
	 * 81 the old image, thats being showed, but replaced with a new one
	 * 82 the new image that will be faded to
	 */
	showSlide: function(i){
	  
	  var that = LMT.ui.out;
		//cancle current timeout of caption
		if (that.captionRemoveTimer){
			window.clearTimeout(that.captionRemoveTimer);
		}
    
    if (i == that.shownImage){
      return;
    }

		if (that.shownImage > -1 && i != that.shownImage) {
      var $all = $(".slide");
			$all.stop(true, true); //it this obj is still animated, cancle all animations and go immideatly to end state
		}
		
		var $new = that.slides[i];
		$new.hide();            //hide the new element in foreground
		$new.css({zIndex: 82}); //make it top
		that.shownImage = i; 
		
		$new.fadeIn(400, function(){ //and fade it in
		  // after finish, reset zlevels to normal
      var $curr = that.slides[that.shownImage];
      var $others = $(".slide").not($curr);
      $others.css({zIndex: 80});
      $curr.css({zIndex: 81});
		});
		
		//show the caption 3 secs
		$('.slide_caption').slideDown();
		that.captionRemoveTimer = window.setTimeout(function(){
			$('.slide_caption').slideUp();
		}, 3000);
		
	  //update the color settings output dialog if shown
    LMT.ui.html.ColorSettingsOutputDialog.refresh();
		
	},
	
	
	/**
	 * show all output images side by side
	 * not implemented 
	 */
	showOverview: function(){
	  return false;
	},
	
} 


LMT.ui.out = out;


/*})();*/
