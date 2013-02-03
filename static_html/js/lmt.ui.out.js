/*************************************
 * lmt.ui.out.js
 * takes care of the output of the images (slideshow like)
 * 
 */

/*(function(){*/

function Output() {
	//config
	this.$out = $("#out");
	this.$btns = $("#btnsetOutNrNav");
	this.$caption = null; 
	
	this.slides = [];
	this.shownImage = -1;
	
	this.tmp=0;

	this.init = function() {
		this.$caption = $('<div class="slide_caption">blabla</div>');
		this.$caption.hide();
		this.$caption.appendTo(this.$out);
		this.tmp=1;
		
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
		
		$("#btnOutOverview").button({
			text: false,
			disabled: true,
			icons: {primary: "icon-th-large" },
		});
    $("#btnOutOverview").on('click', function(){$.event.trigger('DisplayOutputSlideOverview');});
		
		$("#btnsetOutNav").buttonset();
		$("#btnsetOutNav > button").button({ disabled: true });
		
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
	 */
	this.showSlide = function(i){
		//cancle current timeout of caption
		if (this.captionRemoveTimer){
			window.clearTimeout(this.captionRemoveTimer);
		}

		if (this.shownImage > -1 && i != this.shownImage) {
			var $curr = this.slides[this.shownImage];
			$curr.css({zIndex: 80});
			$curr.addClass('bg');
		}
		
		var $new = this.slides[i];
		$new.css({zIndex: 81});
		this.shownImage = i;
		
		$new.fadeIn(400, function(){
			var $elem = $('.slide.bg');
			$elem.toggleClass('bg');
			$elem.hide();
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
