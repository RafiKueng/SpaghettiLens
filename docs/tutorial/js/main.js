
var fn = {};

fn.toggle = function(target){
  $("#_"+target).slideToggle();
};


$( document ).ready(function() {
  
  $("i").each(function(count){
    $(this).click(function(evt){
      fn.toggle(this.id)
    });
  });
  
  $(".adv").add(".exp").hide();

});


$( window ).load(function() {
  console.log("load");
  $("body").fadeIn();
});