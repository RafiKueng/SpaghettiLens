function Color(r, g, b){
	this.r = Math.max(0,Math.min(r,255));
	this.g = Math.max(0,Math.min(g,255));
	this.b = Math.max(0,Math.min(b,255));
	this.rgb = [this.r/255, this.g/255, this.b/255]; // in range 0...1
}

Color.prototype.asHex = function() {
	
	var hex = function(n) {
		return "0123456789ABCDEF".charAt((n-n%16)/16)
      + "0123456789ABCDEF".charAt(n%16);
	}
	return '#' + hex(this.r) + hex(this.g) + hex(this.b);
}



/**
 * 
 * source https://github.com/cloudhead/less.js/blob/master/lib/less/functions.js 
 * @param {Object} h hue from 0...360
 * @param {Object} s saturation from 0...1
 * @param {Object} l lightness from 0...1
 */
Color.fromHSL = function(h,s,l) {
	
  var h = (h % 360) / 360;
  var s = s;
  var l = l;

  var m2 = l <= 0.5 ? l * (s + 1) : l + s - l * s;
  var m1 = l * 2 - m2;

  return new Color(hue(h + 1/3) * 255,
                   hue(h) * 255,
                   hue(h - 1/3) * 255);

  function hue(h) {
      h = h < 0 ? h + 1 : (h > 1 ? h - 1 : h);
      if (h * 6 < 1) return m1 + (m2 - m1) * h * 6;
      else if (h * 2 < 1) return m2;
      else if (h * 3 < 2) return m1 + (m2 - m1) * (2/3 - h) * 6;
      else return m1;
  }
}

