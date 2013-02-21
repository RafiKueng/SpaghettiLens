/*************************************
 * lmt.ui.out.js
 * takes care of the output of the images (slideshow like)
 * 
 */

/*(function(){*/

out = {
	//config
	$out: $("#out"),
	$btns: $("#btnsetOutNrNav"),
	$caption: null, 
	
	slides: [],
	shownImage: -1,
	
	tmp: 0,

	init: function() {
	  var that = LMT.ui.out; 
		that.$caption = $('<div class="slide_caption">blabla</div>');
		that.$caption.hide();
		that.$caption.appendTo(that.$out);
		that.tmp=1;
		
		
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
		
		
    $("#btnOutGlassConfig").button({
      text: false,
      disabled: false,
      icons: {primary: "icon-tasks" },
    });
    $("#btnOutGlassConfig").on('click', function(){$.event.trigger('ShowDialogGlassSettings');});


    $("#btnsetOutConfig").buttonset();
    
    

		
		var tmp = 1;
	};
	
	
	this.load = function() {

    var that = LMT.ui.out; //since this is a callback, this is document, not this object
		that.slides = [];
		var urls = LMT.simulationData.img;

		that.$out.empty(); //remove previous results
		that.$btns.empty(); //remove the number navigation buttons from previous results
		
		$.each(urls, function(i, val) {
			var $div = $('<div class="slide"><img class="slide_img" src="'+ val.url +'" /></div>');
			$div.hide();
			
			$div.appendTo(that.$out);
			
			that.slides.push($div);
			
			/*
			var $nr = $('<span class="slide_btn">_' + i +'_</span>');
			$nr.on('click', {that: that, id:i}, function(evt){
				var that = evt.data.that;
				that.show(evt.data.id);
			});
			$nr.appendTo(that.$btns);
			*/
			var $nr = $('<input type="radio" id="radio'+i+'" name="slideNr" /><label for="radio'+i+'">'+i+'</label>');
			$nr.appendTo(that.$btns);
			$nr.on('click', {id:i}, function(evt){
				$.event.trigger('DisplayOutputSlide', [evt.data.id]);
				/*
				var that = evt.data.that;
				that.show(evt.data.id);
				*/
			});
			
		});
		
		that.$btns.buttonset();
		
		$("#btnsetOutNav > button").button({ disabled: false });
		
	};
	
	/**
	 * callback, displays next slide 
	 */
	this.next = function(evt){
	  var that = LMT.ui.out;
	  var i = that.shownImage+1;
	  if (i > that.slides.length-1) {
	    i = 0;
	  }
		LMT.ui.out.showSlide(i);
		$('input[name="slideNr"]')[i].checked = true;
		$('input[name="slideNr"]').change();
	};
	
	
	/**
	 * callback, displays prev slide 
	 */
	this.prev = function(){
    var that = LMT.ui.out;
    var i = that.shownImage-1;
    if (i < 0) {
      i = that.slides.length-1;
    }
    LMT.ui.out.showSlide(i);
    $('input[name="slideNr"]')[i].checked = true;
    $('input[name="slideNr"]').change();
	};


	
	this.show = function(evt, i){
		LMT.ui.out.showSlide(i);
	};
	
	/**
	 *internal, does really show the image
	 * zindex layers:
	 * 80 default
	 * 81 the old image, thats being showed, but replaced with a new one
	 * 82 the new image that will be faded to
	 */
	this.showSlide = function(i){
		//cancle current timeout of caption
		if (this.captionRemoveTimer){
			window.clearTimeout(this.captionRemoveTimer);
		}

		if (this.shownImage > -1 && i != this.shownImage) {
			var $curr = this.slides[this.shownImage];
			$curr.css({zIndex: 81});
			$curr.addClass('bg');
			$curr.stop(true, true); //it this obj is still animated, cancle all animations and go immideatly to end state
		}
		
		var $new = this.slides[i];
		$new.hide();            //hide the new element in foreground
		$new.css({zIndex: 82}); //make it top
		this.shownImage = i; 
		
		$new.fadeIn(400, function(){ //and fade it in
			var $elem = $('.slide.bg');
			$elem.toggleClass('bg');
			$elem.css({zIndex: 80});
			//$elem.hide();
		});
		
		//show the caption 3 secs
		$('.slide_caption').slideDown();
		this.captionRemoveTimer = window.setTimeout(function(){
			$('.slide_caption').slideUp();
		}, 3000);
	};
	
	
	this.showOverview = function(){
	  return false;
	};
	
} 


LMT.ui.output = Output;


/*})();*/
