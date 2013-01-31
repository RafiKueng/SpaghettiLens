




function BandColorSelector(channel, x, y, width, height, svgColorspaceElem, svgParent) {
	this.channel = channel;
	this.x = x;
	this.y = y;
	this.w = width;
	this.h = height;
	this.cSpace = svgColorspaceElem;
	this.parent = svgParent;
}


BandColorSelector.prototype.init = function () {
	
	//the starting position of the color selector circle
	var startpos = {
		x: Math.floor(this.x + this.w / 2),
		y: parseInt(this.cSpace.getAttribute('y')) + parseInt(this.cSpace.getAttribute('height'))/2
	};
	
	this.grp = document.createElementNS("http://www.w3.org/2000/svg", "g");

	this.rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
	this.rect.setAttribute('x', this.x);
	this.rect.setAttribute('y', this.y);
	this.rect.setAttribute('width', this.w);
	this.rect.setAttribute('height', this.h);
	this.rect.setAttribute('fill', '#fff');
	
	this.text = document.createElementNS("http://www.w3.org/2000/svg", "text");
	this.text.setAttribute('x', this.x + this.w/2 - 5);
	this.text.setAttribute('y', this.y + this.h/2 + 5);
	this.text.textContent = this.channel.short;
	
	this.line = document.createElementNS("http://www.w3.org/2000/svg", "line");
	this.line.setAttribute('x1', this.x + this.w/2);
	this.line.setAttribute('y1', this.y + this.h);
	this.line.setAttribute('x2', startpos.x);
	this.line.setAttribute('y2', startpos.y);
	this.line.setAttribute('style', 'stroke:#000000;stroke-width:1');

	this.circ = document.createElementNS("http://www.w3.org/2000/svg", "circle");
	this.circ.setAttribute('id', 'bcselect'+BandColorSelector.n++);
	this.circ.setAttribute('cx', startpos.x);
	this.circ.setAttribute('cy', startpos.y);
	this.circ.setAttribute('r', 5);
	this.circ.setAttribute('style', 'stroke:#000000;stroke-width:1');
	this.circ.jsClass = this;

	this.grp.appendChild(this.line);
	this.grp.appendChild(this.rect);
	this.grp.appendChild(this.text);
	this.grp.appendChild(this.circ);

	this.parent.appendChild(this.grp);
	
	this.update(startpos.x, startpos.y);
	
}


BandColorSelector.prototype.update = function (x, y) {
	
	//snap at middle, top and bottom line:
	var cs_x = parseInt(this.cSpace.getAttribute('x'));
	var cs_y = parseInt(this.cSpace.getAttribute('y'));
	var cs_w = parseInt(this.cSpace.getAttribute('width'));
	var cs_h = parseInt(this.cSpace.getAttribute('height'));

	var snapdist = 10; //the distance to snap  in in pixels

	if (y-cs_y < snapdist) {
		y = cs_y;
	}
	else if (Math.abs( y - (cs_y + cs_h/2) ) < snapdist){
		y = cs_y + cs_h / 2;
	}
	else if (cs_h-y+cs_y < snapdist) {
		y = cs_y + cs_h;
	}

	if (x<cs_x) {x=cs_x;}
	else if (x>cs_x+cs_w) {x=cs_x+cs_w;}
	
	this.line.setAttribute('x2', x);
	this.line.setAttribute('y2', y);

	this.circ.setAttribute('cx', x);
	this.circ.setAttribute('cy', y);

	this.color = this.getColor();
	this.channel.color = this.color;
	
	this.rect.setAttribute('fill', this.color.asHex());
	this.circ.setAttribute('fill', this.color.asHex());
}



BandColorSelector.prototype.getColor = function () {

	var x = this.circ.getAttribute('cx');
	var y = this.circ.getAttribute('cy');
	
	var cs_x = this.cSpace.getAttribute('x');
	var cs_y = this.cSpace.getAttribute('y');
	var cs_w = this.cSpace.getAttribute('width');
	var cs_h = this.cSpace.getAttribute('height');
	
	//xaxis of selection field 0...360 
	var h = (x-cs_x) / cs_w * 360; 
	var s = 1;
	//y axis of selection field
	var l = 1 - ((y-cs_y) / cs_h);
	 
	

	return Color.fromHSL(h,s,l);
}

//counter
BandColorSelector.n=0;