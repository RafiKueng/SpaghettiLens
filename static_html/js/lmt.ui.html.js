/**
 * 
 */
/*(function(){*/


var html = {};




html.fire = function(evt){
	
}




html.SelectModelDialog = {
  
  init: function() {
    
    $('#select_model_dialog').dialog({
      autoOpen: false,
      minWidth: 550,
      minHeight: 700,
      modal: true,
      open: function(){},
      buttons: [
      {
        text: "Login and continue previous session",
        click: function(){
          alert("not yet implemented, please use the selection again");
        }
      },
      {
        text: "Ok",
        click: function(evt){
          //tmp1 = $("#selmod_cat").val();
          //tmp2 = $("#selmod_lens").val();
          tmp3 = $("#selmod_lens").val();
          if (tmp3==""){
            //todo in this case, load all ids
            alert("please choose at least one lens");
            return;
          }
          else {
            //modelid = parseInt(tmp2);
            for(var i=0; i<tmp3.length;i++) {tmp3[i] = +tmp3[i];} //parse to int
            $.event.trigger("GetModelData", [models = tmp3, catalog=+$("#selmod_cat").val()]);
            $('#select_model_dialog').dialog("close");
          }
        }}
      ]
        
   });
    
    
    $("#selmod_cat").chosen({allow_single_deselect:true});
    $("#selmod_cat").chosen().change(function(){
      if ($("#selmod_cat").val() != "0" ){
        $("#selmod_lens").val('0').trigger("liszt:updated");
        //$("#selmod_lensid").val('0').trigger("liszt:updated");
        LMT.ui.html.SelectModelDialog.updateLensList();
      }
    });
    
    $("#selmod_lens").chosen({allow_single_deselect:true});
    $("#selmod_lens").chosen().change(function(){
      if ($("#selmod_lens").val() != "0" ){
        //$("#selmod_cat").val('0').trigger("liszt:updated");
        //$("#selmod_lensid").val($("#selmod_lens").val()).trigger("liszt:updated");
      }
    });
    
    /*
    $("#selmod_lensid").chosen({allow_single_deselect:true});
    $("#selmod_lensid").chosen().change(function(){
      if ($("#selmod_lensid").val() != "0" ){
        $("#selmod_cat").val('0').trigger("liszt:updated");
        $("#selmod_lens").val($("#selmod_lensid").val()).trigger("liszt:updated");
      }
      
    });
    */
        
    //LMT.com.getInitData(); //this will trigger an update
  },
  
  //event handler
  show: function(evt){
    $.event.trigger("GetInitData");
    $('#select_model_dialog').dialog("open");
  },
  
  onInitData: function(evt, jsonObj) {
    LMT.ui.html.SelectModelDialog.availObj = jsonObj; 
    
    $parent = $("#selmod_cat");

    $parent.append($('<option value="-1">NONE (all lenses NOT in a catalog)</option>'));
    var cat = {};
    for (var i=0; i<jsonObj.catalogues.length; i++){
      var id = jsonObj.catalogues[i].id;
      cat[id] = jsonObj.catalogues[i];
      var elem = $('<option value="' + id + '">'
        + cat[id].name + ' (' + cat[id].description + ')</option>');
      $parent.append(elem);
    }
    $parent.trigger("liszt:updated");
    
    LMT.ui.html.SelectModelDialog.catalogs = cat; 
    
    LMT.ui.html.SelectModelDialog.updateLensList();

    /*
    $parent1 = $("#selmod_lens")
    //$parent2 = $("#selmod_lensid")
    for (var i=0; i<jsonObj.lenses.length; i++){
      var lens = jsonObj.lenses[i];
      var lenscat = cat[lens.catalog] ? ' (catalog: '+ cat[lens.catalog].name + ")": ""
      var elem1 = $('<option value="' + lens.id + '">' + lens.name +  lenscat + '</option>');
      $parent1.append(elem1);
      //var elem2 = $('<option value="' + lens.id + '">' + lens.id + '</option>');
      //$parent2.append(elem2);
    }
    $parent1.trigger("liszt:updated");
    //$parent2.trigger("liszt:updated");
    */
  },
  
  updateLensList: function() {
    availObj = LMT.ui.html.SelectModelDialog.availObj;
    cat = LMT.ui.html.SelectModelDialog.catalogs;
    $parent = $("#selmod_lens")
    
    $parent.empty();
    $parent.append($('<option value=""></option>'));

    catId = +$("#selmod_cat").val(); //+ casts string to int

    for (var i=0; i<availObj.lenses.length; i++){
      var lens = availObj.lenses[i];
      if (lens.catalog == catId || catId == 0 || //only add if the lenses catalog is selected or no calatog selected
        (catId==-1 && lens.catalog==null) ){ // or the NONE option is selected and this lens doesnt have a cat 
        var lenscat = cat[lens.catalog] ? ' (cat: '+ cat[lens.catalog].name + ")": ""
        var elem1 = $('<option value="' + lens.id + '">id:' + lens.id + ' ' + lens.name +  lenscat + '</option>');
        $parent.append(elem1);
      }
    }

    $parent.trigger("liszt:updated");
  }
  
}





html.Toolbar = {
  init: function() {
  
  	$("#toolbarGrp1 button")
  	 .add("#toolbarGrp1 input")
  	 .add("#top button")
  	 .each(function(){
  		
  		var $this = $(this);
  		var icon = $this.data("icon");
  		var eventName = $this.data("event");
  		var value = $this.data("value");
  		
  		$(this).button({
  			text: false,
  			disabled: false,
  			icons: {primary: icon }
  		})
  		.on('click', {name:eventName, value: value} , LMT.ui.html.Toolbar.fire);
  	});
  
  	$("#toolbarGrp1 > .btnset").buttonset();

    //set buttons to correct state 
    
    //mode radio buttons	
    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
    $('input[name="mode"]').change();
    
    //un/re do buttons:
    $('#btnInUndo').add('#btnInRedo').button("disable");
    
  },
  
  /**
   * updates the buttons
   */
  update: function(evt) {
    //radiobuttons for mode selection 
    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
    $('input[name="mode"]').change();
    // un / redo buttons whether there is something to be undone / redone
    $('#btnInUndo').button(LMT.actionstack.undoSize>0 ? "enable" : "disable");
    $('#btnInRedo').button(LMT.actionstack.redoSize>0 ? "enable" : "disable");
  },
  
  /**
   * fires an event when a toolbar button is pressed 
   */
  fire: function(evt){
    $.event.trigger(evt.data.name, evt.data.value);
  }
}



html.ColorSettingsDialog = {
  init: function(){	
	
  		// multiply the color settings tools for n channels
  	var $parent = $('#color_dialog');
  	var $elem = $("#csettings_ch0");
  	var ch = LMT.modelData.ch;
  	
  	for (var i = 1; i<ch.length; i++){
  		$clone = $elem.clone(true, true);
  		$clone.find('*').data('id', i);
  		$clone.appendTo($parent);
  	}
  	
  	
  	// color picker dialog
  	$('#color_dialog').dialog({
  		autoOpen: false,
  		minWidth: 500,
  		open: function(){
  			 $('.mycp').each(function(i, val){
  			   	var str = (1 << 24) | (ch[i].r*255 << 16) | (ch[i].g*255 << 8) | ch[i].b*255;
  			 		$(this).val('#' + str.toString(16).substr(1)).focus();
  			 		
  			 		// hack that should update the field so they get their color from beginning
  			 		var press = jQuery.Event("keyup");
  					press.ctrlKey = false;
  					press.which = 13;
  					$(this).trigger(press);
  			 });
  		}
  	});
  	
  	
  	//sliders
  	$('#color_dialog .slider').slider({
  		max: 1,
  		min: -1,
  		value: 0,
  		step: 0.05,
  		stop: function(evt, ui) {
  			var value = ui.value;
  			var type = $(this).data("type");
  			var id = $(this).data("id");
  			
  			if (type=="contrast"){
  				value = Math.pow(10, value); //change range from [-1...1] to [0.1 ... 10]
  			}
  			
  			LMT.modelData.ch[id][type.substr(0,2)] = value;
  			log.write("stopped sliding");
  			$.event.trigger('ChangedModelData', id);
  		}
  		
  	});
	
  	$('.mycp').colorpicker({
  		parts: ['header',
  			'map',
  			'bar',
  			//'hex',
  			//'hsv',
  			//'rgb',
  			//'alpha',
  			//'lab',
  			//'cmyk',
  			//'preview',
  			'swatches',
  			'footer'],
  		colorFormat: '#HEX',
  		showOn: 'both',
  		buttonColorize: true,
  		altField: '',
  		buttonImage: 'img/cp/ui-colorpicker.png',
  		buttonImageOnly: false,
  		buttonText: 'pick',
  		showOn: 'button',
  		close: function(evt, data){
  			var id= $(this).data("id");
  			$(this).css('background', data.formatted);
  			LMT.modelData.ch[id].r = data.rgb.r;
  			LMT.modelData.ch[id].g = data.rgb.g;
  			LMT.modelData.ch[id].b = data.rgb.b;
  			log.write("picked color for "+id);
  			$.event.trigger('ChangedModelData', id);
  		},
  	});
  	
  	$parent.removeClass("initHidden");
  	
  },
  
  show: function(){
    $('#color_dialog').dialog("open");
  }
  
  
  
}
  	
	
	
html.DisplaySettingsDialog = {

  init: function(){
  
  	/**********************
  	 * the display settings dialog 
  	 */
  	$("#display_dialog").dialog({
  		autoOpen: false,
  		minWidth: 700,
  		open: function(){ //update button status
  			// .change is a bugfix, as described here: http://stackoverflow.com/questions/8796680/jqueryui-button-state-not-changing-on-prop-call
  			$('#conn_l').prop("checked", LMT.settings.display.paintConnectingLines).change();
  			$('#cont_p').prop("checked", LMT.settings.display.paintContourPoints).change();
  			$('#cont_l').prop("checked", LMT.settings.display.paintContours).change();
  		}
  	});
  	
  	$('#dsettings').buttonset();
  	
  	$('#conn_l').click(function(evt){
  		LMT.settings.display.paintConnectingLines = this.checked;
  		log.write('toggle 1' + this.checked);
  		$.event.trigger('RepaintModel');
  	});
  	$('#cont_p').click(function(evt){
  		LMT.settings.display.paintContourPoints = this.checked;
  		log.write('toggle 2');
  		$.event.trigger('RepaintModel');
  	})
  	$('#cont_l').click(function(){
  		LMT.settings.display.paintContours = this.checked;
  		log.write('toggle 3');
  		$.event.trigger('RepaintModel');
  	});
  	
  	$("#display_dialog").removeClass("initHidden");
  	
	},
	
	show: function() {
	  $('#display_dialog').dialog("open");
	}
}
	


html.GlassSettingsDialog = {
  init: function(){
    $("#glass_dialog").dialog({
      autoOpen: false,
      minWidth: 400,
      open: function(){}
    });
    
    
    $("#gset_redshift_slide").slider({
      range: true,
      min: 0,
      max: 2,
      step: 0.01,
      values: [0.5, 1],
      slide: function(evt, ui){
        $("#gset_redshift_out").html("(Lens: " + ui.values[0] + " / Source: " + ui.values[1] + ")");
      },
      stop: function(evt, ui){
        LMT.model.GlassSettings.z_lens = ui.values[0];
        LMT.model.GlassSettings.z_src = ui.values[1];
        
      }
    });
    

    $("#gset_pixrad_slide").slider({
      range: false,
      min: 3,
      max: 8,
      step: 1,
      value: 5,
      slide: function(evt, ui){
        $("#gset_pixrad_out").html("("+ui.value+")");
      },
      stop: function(evt, ui){
        LMT.model.GlassSettings.pixrad = ui.value;
      }
    });


    $("#gset_nmodels_slide").slider({
      range: false,
      min: 50,
      max: 2000,
      step: 50,
      value: 200,
      slide: function(evt, ui){
        $("#gset_nmodels_out").html("("+ui.value+")");
      },
      stop: function(evt, ui){
        LMT.model.GlassSettings.n_models = ui.value;
      }
    });
    
    $("#gset_issymm")
      .button()
      .click(function( evt ) {
        var $btn = $(this);
        var state = !($btn.attr("checked")? true : false); //get old state, invert it to have new state
        $btn.attr("checked", state);
        LMT.model.GlassSettings.isSym = state;
        log.write(state);
        $btn.button( "option", "label", state ? "Yes" : "No" );
      });

    
    //set defaults
    $("#gset_redshift_out").html("(Lens: " + $("#gset_redshift_slide").slider( "values", 0 ) + " / Source: " + $("#gset_redshift_slide").slider( "values", 1 ) + ")");
    $("#gset_pixrad_out").html("(" + $("#gset_pixrad_slide").slider( "value") + ")");
    $("#gset_nmodels_out").html("(" + $("#gset_nmodels_slide").slider( "value") + ")");
   
    $("#gset_issymm").button("option", "label", "No");
    
   
    $("#glass_dialog").removeClass("initHidden");
  },
  
  show: function() {
    $('#glass_dialog').dialog("open");
  }
}





html.Tooltip = {
  
  init: function(){
    
    //prepare tooltip div 
    document.getElementById('popup').style.display = 'block';
    //on mouse enter tooltip: cancle fade out animation, display till mouseleave 
    $("#popup").on('mouseenter', function(evt){
      $("#popup").stop(true, true).fadeIn(200);
    });
    $("#popup").on('mouseleave', function(evt){
      $("#popup").stop(true, true).fadeOut(50);
    });
    $("#popup").hide();
  }, 
  
  
  
  show: function(evt, orgEvt, data){
  	var offset = {top: 5, left: 5};
  	var newcss = {};
  	$("#popup > #text").html(data.txt);
  	$("#popup > #link").html(data.link);
  	$("#popup > #hotkey").html(data.hotkey);
  
  	//make change style to get position / width ect...
  	$("#popup").css({visibility: 'hidden'}).show();
  	
  	//calculate position
  	var top = orgEvt.pageY;
  	var left = $(orgEvt.currentTarget).offset().left;
  	var inpY = $('#inp').offset().top;
  
  	left = left + $(orgEvt.currentTarget).outerWidth()/2;
  	
  	//check if out of screes
  	var inpR = $('#inp').offset().left + $('#inp').outerWidth(true);
  	var sizeX = $("#popup").outerWidth(true);
  	
  	/*
  	newcss["border-top-left-radius"] = 0;
  	newcss["border-top-right-radius"] = '5px';
  	*/
  	if (left+sizeX>inpR-20) {
  		left = left - sizeX;
  		//newcss["border-top-left-radius"] = '5px';
  		//newcss["border-top-right-radius"] = 0;
  		$("#popup").addClass('right').removeClass('left');
  	}
  	else {
  		$("#popup").addClass('left').removeClass('right');
  	}
  	
  	newcss.left = left+offset.left,
  	newcss.top= inpY+offset.top;
  	newcss.visibility = 'visible';
  	
  	$("#popup").css(newcss).hide();
  	
  	$("#popup").stop(true, true).fadeIn(200);
  },
  
  
  hide: function(){
  	$("#popup").stop(true, true).fadeOut(600);
  }
}



html.KeyboardListener = {
  init: function(){
    $('body').on('keypress', LMT.ui.html.KeyboardListener.keyEvent);
  },
  
  keyEvent: function(evt){
    var code = event.which || event.keyCode;
    log.write("keycode: "+code);
    
    switch (code) {
      case 13: //enter and numEnter
      case 48:
      case 96: //num0
        $.event.trigger("ZoomPanReset");
        break;
      
      case 43: //num+
        $.event.trigger("Zoom", [+1]);
        break;
      default:
        return;
    }
    if (evt.stopPropagation) {evt.stopPropagation();}
    if (evt.preventDefault) {evt.preventDefault();}
  }
}



LMT.ui.html = html;

/*})();*/