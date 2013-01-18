/**
 * 
 */


/**
 * elements: div element containing div elements with buttons
 */
function Toolbar(domElement){
	this.toolbarElements = [];
	this.parent = domElement;
	this.$parent = $(domElement);
	this.$elems = $(".toolbar_element", domElement);
	var self = this;
	this.$elems.each(function(i, val){
		var tbe = new LMT.objects.SimpleTBE(val);
		self.toolbarElements.push(tbe);
	});
	
	//sort, such that first collapsing is first
	this.toolbarElements.sort(function(a, b){
    if(a.order < b.order) return -1;
    if(a.order > b.order) return 1;
    return 0;
	});
	
	this.collapseNext = 0; //pointer (id) to toolBarElement to collapse next
	
}


Toolbar.prototype.adjust = function(){
	var thres = 30;
	
	var currLength = 0;
	var parentLength = this.$parent.outerWidth();
	
	for (var i = 0; i<this.toolbarElements.length; i++){
		currLength += this.toolbarElements[i].outerWidth();
	}
	
	if (parentLength-currLength < thres){
		this.toolbarElements[this.collapseNext].collapse();
		this.collapseNext++;
	}
	if (this.collapseNext != 0
		&& parentLength-currLength > this.toolbarElements[this.collapseNext-1].maxWidth + thres) {
		this.toolbarElements[this.collapseNext-1].expand();
		this.collapseNext--;
	}
}




var tbe = {}; //toolbar elements
/**
 * element: div element conaining the svg buttons
 */
tbe.SimpleTBE = function(elem){
	this.$elem = $(elem);
	this.type = this.$elem.data("type");
	this.order = this.$elem.data("order");
	this.maxWidth
}


tbe.ToggleGroupTBE = function (element){

}


tbe.outerWitdh = function () {
	return this.$elem.outerWidth();
}
tbe.ToggleGroupTBE.prototype.outerWidth = tbe.outerWitdh;
tbe.SimpleTBE.prototype.outerWidth = tbe.outerWitdh;






function ToggleButton(){
	
}


function ClickButton(){
	
}



LMT.objects.Toolbar = Toolbar;
LMT.objects.SimpleTBE = tbe.SimpleTBE;