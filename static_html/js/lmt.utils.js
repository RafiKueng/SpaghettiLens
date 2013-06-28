
LMT.utils.logger = function(toConsole) {
  var _log = document.getElementById("logcont");
  var _history = [];
  var _length = 10;
  $("#log").css({'display':'block'});
  $("#log").hide();
  
  /*
  this.write = function(txt) {
    this.log.innerHTML = txt;
  };
  
  this.append = function(txt) {
    this.log.innerHTML += ('<br/>' + txt); 
  };
  
  this.clear = function() {
    this.log.innerHTML = ""; 
  };
  */
  if (!toConsole){
    this.log = function() {
      var txt = arguments[0] ? arguments[0] : ""; //if no argument write empty
      for (var i = 1;i<arguments.length;++i){
        txt += '<br/>| '+arguments[i];
      }
      txt += arguments.length>1?'<br/>\\------':"";
      
      _history.push(txt);
      if (_history.length>_length) _history.shift();
      
      _log.innerHTML = _history.join('<hr/>');
    };
  }
  else {
    if(!window.console){ window.console = {log: function(){} }; }
    _log.innerHTML = "logging to js console";
    this.log = function() {
      var txt = "";
      for (var i = 0;i<arguments.length;++i){
        txt += arguments[i] + '\n';
      }
      //txt += '------';
      console.log(txt);
      _history.push(txt);
      if (_history.length>_length) _history.shift();
    }
  };
  
  this.toggle = function(){
    $("#log").toggle();
  };
  
}


/**************
 * Math helpers 
 */

LMT.utils.toPolarAng = function(xdiff, ydiff) {
  var direction = (Math.atan2(ydiff, xdiff));
  return (direction);
}

LMT.utils.toPolarR = function(xdiff, ydiff) {
  var distance = Math.sqrt(xdiff * xdiff + ydiff * ydiff);
  return (distance);
}

LMT.utils.toRectX = function(direction, distance) {
  var x = distance * Math.cos(direction);
  return (x);
}

LMT.utils.toRectY = function(direction, distance) {
  var y = distance * Math.sin(direction);
  return (y);
}

/**
 * calculates the distance squarred between to point like objects (have .x and .y attribute) 
 */
LMT.utils.dist2 = function(pnt1, pnt2) {
  var dx = pnt1.x-pnt2.x;
  var dy = pnt1.y-pnt2.y;
  return (dx*dx+dy*dy);
}

LMT.utils.round = function(number, digits) {
  var multiple = Math.pow(10, digits);
  var rndedNum = Math.round(number * multiple) / multiple;
  return rndedNum;
}





/**
 * loads a set of Objects (images), provides a callback on each
 * loaded and one if all are loaded
 * crossOrigin: default True: allow to load from forwign origins
 * get the loaded images as an argument to the onAll callback
 */
LMT.utils.ImageLoader = function(listOfURLs, onEach, onAll, crossOrigin) {
  
  var urls = listOfURLs;
  var imgs = [];
  var nImgs = listOfURLs.length;
  var nLoaded = 0;
  
  var co = typeof crossOrigin !== 'boolean' ? true : crossOrigin;
  
  for (var i=0; i<listOfURLs.length; i++) {
    if (typeof urls[i] === 'string'){
      var img = new Image();
      img.onload = function(){
        nLoaded++;
        onEach({nLoaded:nLoaded, nImgs:nImgs, p:100.0*nLoaded/nImgs});
        
        if (nLoaded==nImgs){
          onAll(imgs);
        }
      };
      if (co) {img.setAttribute('crossOrigin','anonymous');}
      img.src = urls[i];
      imgs[i] = img;
    }
  }
}



/**
 * addons to jquery
 */


/**
 * svg manipulation addon
 * (since addclass doesnt work for svg dom elements, but .attr does)
 * classList does not exist in IE, see here for comatibility lib
 * https://developer.mozilla.org/en-US/docs/DOM/element.classList
 * 
 */
$.fn.addClassSVG = function(classname) {
	return this.each(function() {
		this.classList.add(classname)});
}

$.fn.removeClassSVG = function(classname) {
	return this.each(function() {
		this.classList.remove(classname)});
}

$.fn.toggleClassSVG = function(classname) {
	return this.each(function() {
		this.classList.toggle(classname)});
}




/**
 * gets a simple hashcode from any string
 * used for hashing modelstrings and check for changes 
 */
String.prototype.hashCode = function(){
    var hash = 0, i, char;
    if (this.length == 0) return hash;
    for (i = 0; i < this.length; i++) {
        char = this.charCodeAt(i);
        hash = ((hash<<5)-hash)+char;
        hash = hash & hash; // Convert to 32bit integer
    }
    return hash;
};