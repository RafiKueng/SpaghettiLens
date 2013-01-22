/*************************************
 * lmt.ui.out.js
 * takes care of the output of the images (slideshow like)
 * 
 */

/*(function(){*/

function Output() {
	//config
	this.$out = $("#out");
	this.$btns = $("#nrbtn");
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
			disabled: true,
			icons: {primary: "ui-icon-carat-1-w" }
		});
		
	};
	
	
	this.load = function(urls) {
		
		this.slides = [];
		var that = this;
		
		$.each(urls, function(i, val) {
			var $div = $('<div class="slide"><img class="slide_img" src="'+ val +'" /></div>');
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
			var $nr = $('<input type="radio" id="radio'+i+'" name="radio" /><label for="radio'+i+'">'+i+'</label>');
			$nr.appendTo(that.$btns);
			$nr.on('click', {that: that, id:i}, function(evt){
				var that = evt.data.that;
				that.show(evt.data.id);
			});
			
		});
		
		this.$btns.buttonset();
		
		
	};
	
	this.next = function(){
		var tmp;
	};
	
	
	this.prev = function(){
		var tmp;
	};
	
	this.show = function(i){
		this.showSlide(i);
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
	}
	
} 


LMT.ui.out = Output;


/*})();*/