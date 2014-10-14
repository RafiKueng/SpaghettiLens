
var fn = {};

fn.toggle = function(target){
  $("#_"+target).slideToggle();
};

fn.showgoto = function(target){
  $("#_"+target).slideDown(200);
  $('html, body').animate({
        scrollTop: $( "#_"+target ).offset().top - $(window).height()/3.
    }, 200);
  $("#_"+target).animateHighlight(200,500,1);
};


$.fn.animateHighlight = function(delay, duration, steps) {
    var delay = delay || 0;
    var duration = duration || 2000;
    var steps = steps || 3;
    var dt = duration / steps / 2;
    this.delay(delay);
    for (var i=0; i<steps;i++) {
      this.fadeTo(dt,0.01).fadeTo(dt,1.0);
    }
};


$( document ).ready(function() {
  
  $("i").each(function(count){
    $target = $('#_'+this.id);
    if ($target.hasClass('ezy')) {type = 'ezy';}
    else if ($target.hasClass('adv')) {type = 'adv';}
    else if ($target.hasClass('exp')) {type = 'exp';}
    else {type = '';}
    
    $(this)
      .click(function(evt){fn.showgoto(this.id)})
      .addClass(type) //this colors the links acccording to target
      ;
  });
  
  $("div.ezy, div.adv, div.exp").hide();
  
  $('h3, h4').click(function(){
    if ($(this).parent().hasClass('ezy') ||
        $(this).parent().hasClass('adv') ||
        $(this).parent().hasClass('exp') ){
      $(this).parent().slideUp();
    } 
  })
  
  
  $('div.video').each(function(){
    $tbox = $('<div class="topicbox">');
    $tbox.append('<h3>Video</h3>');
    $tbox.append('<p>[[watch video]]</p>');
    $tbox.append('<p>'+$(this).data('url')+'</p>');
    $(this).append($tbox);
    $(this).hide(); //hinde until its implemented
  })

});


$( window ).load(function() {
  console.log("load");
  $("body").fadeIn();
});