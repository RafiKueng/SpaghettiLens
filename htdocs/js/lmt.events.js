/**
 * custom event management / Creation
 * 
 * event handling is taken care of in the according section (mostly in the intelligence script)
 * here, new events will be created in dependence of previous events
 */


var events = {
};


/**
 * Fires AppReady when the app has completly loaded and is ready to be used
 * 
 * (this is one instance of an anonymous class)
 */
events.AppReady = {
	loadedButtons: false,
	loadedModelData: false,
	loadedModelImages: false,

	init: function() {
		// add handler to listen to
		// inside the handler, make events.Appready available as 'that'
		// 'this' is the document (the jquery selector noted)
		$(document).on('loadedButtons', {that: this}, function(evt){
			var that = evt.data.that;
			that.loadedButtons = true;
			that.check();
		});
		
		$(document).on('loadedModelData', {that: this}, function(evt){
			var that = evt.data.that;
			this.loadedModelData  = true;
			this.check();
		});
		
		$(document).on('loadedModelImages', {that: this}, function(evt){
			var that = evt.data.that;
			this.loadedModelImages = true ;
			this.check();
		});
		return this;
	},
	
	check: function() {
		if (this.loadedButtons && this.loadedModelData && this.loadedModelImages) {
			$.event.trigger('AppReady');
		}
	}
}.init();





LMT.events = events;