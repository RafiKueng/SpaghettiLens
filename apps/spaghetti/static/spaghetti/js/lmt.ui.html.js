/**
 * 
 */
/*(function(){*/


var html = {};




html.fire = function(evt){
	
};


/**
 * creates a dialog that asks for the username
 * used when loading a result or model
 */
html.SetUsernameDialog = {
  init: function() {
    var $div = $('#get_username').dialog({
      autoOpen: false,
      minWidth: 400,
      minHeight: 200,
      modal: true,
      buttons: [
        {
          text: "Ok",
          click: function(evt){
            $('#get_username').dialog("close");
            var uname = $("#username2").val();
            LMT.settings.username = uname;
          }
        },],
      open: function(){
        var uname = $.cookie('username');
        if (uname){
          $("#username2").val(uname);
          $('.ui-dialog-buttonpane button:last').focus();
        }
        
      }
    });
  },
  
  show: function() {
    var uname = $.cookie('username');
    if (uname){
      LMT.settings.username = uname;
    }
    else {
      $('#get_username').dialog("open");
    }
  }
  

}


html.SaveResultDialog = {
  init: function() {
    $('#save_results_dialog').dialog({
      autoOpen: false,
      minWidth: 600,
      minHeight: 400,
      modal: true,
      open: function(){},
      buttons: [
        {
          text: "Abort",
          click: function(evt){
            $('#save_results_dialog').dialog("close");
          }
        },
        {
          text: "Save",
          click: LMT.ui.html.SaveResultDialog.upload
        },
        {
          text: "Close",
          click: LMT.ui.html.SaveResultDialog.close
        },
        {
          text: "Restart",
          click: function(evt){
            document.location.reload(true);
          }
        }
      ]
    });
  },
  
  show: function(){
    $('#save_results_dialog').html('<p>genrating input image...</p>');
    $('#save_results_dialog').dialog("open");
    $(".ui-dialog-buttonpane button:contains('Restart')").button('disable');
    $(".ui-dialog-buttonpane button:contains('Close')").button('disable');
    $(".ui-dialog-buttonpane button:contains('Save')").button('disable');
    $(".ui-dialog-buttonpane button:contains('Abort')").button('enable');
    $.event.trigger("ConvertInputImageToPNG");
  },
  
  
  upload: function(evt){
    $.event.trigger("SaveModel");
  },
  
  close: function(evt){
    $('#save_results_dialog').dialog("close");
  },
  
  generatedImage: function(evt){
    
    var html = [
      '<p>Input image:</p>',
      '<img style="width:300px; float: left;" src="'+LMT.ui.svg.img+'"/>',
      '<p>To adjust your image before uploading, press Abort, make your changes and reopen the save dialog.<br/>',
      '(Pay attention not to <b>modify</b> the model, otherwise you\'d have to render the model again.)</p>'      
    ].join('\n');
    $('#save_results_dialog').html(html);

    $(".ui-dialog-buttonpane button:contains('Close')").button('disable');
    $(".ui-dialog-buttonpane button:contains('Save')").button('enable');
  },
  
  savedModel: function(evt, rid){
    $(".ui-dialog-buttonpane button:contains('Restart')").button('enable');
    $(".ui-dialog-buttonpane button:contains('Close')").button('enable');
    $(".ui-dialog-buttonpane button:contains('Save')").button('disable');
    $(".ui-dialog-buttonpane button:contains('Abort')").button('disable');

    var url = "http://mite.physik.uzh.ch/data/"+rid;
    var html = [
      '<p>Result Saved</p>',
      '<p>You can retrieve your model at the following url:<br/>',
      '<a href="'+url+'" target="_blank">'+url+'</a></p>'
    ].join('\n');
    
    $('#save_results_dialog').html(html);
  }
  
};



/** NEW V2
 * Shows a progress Dilog while downloading a bunch of images
 */
html.LoadProgressDialog = {
    init: function () {
        $('#load_progress_dialog').dialog({
            autoOpen: false,
            minWidth: 250,
            minHeight: 50,
            modal: true,
            //open: function(){},
            buttons: []
        });
        html.LoadProgressDialog.htmlelem = $("#load_progress_dialog :first-child");
    },

    show: function (nImgs) {
        html.LoadProgressDialog.update( {nImgs: nImgs, nLoaded: 0, p: 0} )
        $('#load_progress_dialog').dialog("open");
    },

    close: function () {
        $('#load_progress_dialog').dialog("close");
    },

    update: function(stat){
        html.LoadProgressDialog.htmlelem.html(
            "loaded: "+stat.p+"% ("+stat.nLoaded+" of "+stat.nImgs+")"
        );
    },
};






html.WaitForResultDialog = {
    init: function() {
        $('#wait_for_results_dialog').dialog({
            autoOpen: false,
            minWidth: 350,
            minHeight: 100,
            modal: false,
            //open: html.WaitForResultDialog.onOpen,
            buttons: []
        });
    },

    show: function(){
        $('#wait_for_results_dialog')
            .dialog('open')
            .dialog('widget').position({
            my: "center center",
            at: "center center",
            of: $('#out')
        });
    },


    close: function(){
        $('#wait_for_results_dialog').dialog('close');
    },

    update: function(){
        var prog = LMT.simulationResult.progress;
        if (prog) {
            if (prog.of == 0) {
                ss = '';
            }
            else {
                ss = " (" + prog.i + " of " + prog.of + ")";
            }
            $('#wait_for_results_dialog p').html(
                prog.text + ss

/*
                'solutions: ' + LMT.simulationResult.progress.solutions + '<br>' +
                'models: ' + LMT.simulationResult.progress.models + '<br>' +
                'images: ' + LMT.simulationResult.progress.images + '<br>'
*/
            );
        }
    },
};




// OLD, new above, new pipeline
//
//html.WaitForResultDialog = {
//  init: function() {
//    $('#wait_for_results_dialog').dialog({
//      autoOpen: false,
//      minWidth: 350,
//      minHeight: 100,
//      modal: false,
//      //open: html.WaitForResultDialog.onOpen,
//      buttons: []
//    });
//  },
//  
//  show: function(){
//    $('#wait_for_results_dialog')
//      .dialog('open')
//      .dialog('widget').position({
//        my: "center center",
//        at: "center center",
//        of: $('#out')
//      });
//  },
//  
//  estimate: function tottime(p,n) {
//    //parameters from variious fits
//    //machine: how much slower is the worker than anker (@2.8Ghz): 2.21 for mite
//    var aa1= 34.1040000000;
//    var bb1=-28.0330000000;
//    var aa2=  0.9857000000;
//    var bb2=  2.3436000000;
//    var cc1=  0.0000000000;
//    var a11=  0.0000001989;
//    var a12=  0.8493931800;
//    var a21=  0.0000005989;
//    var a22=  0.0055298878;
//    var a23= -3.0273621847;
//    var machine=  2.2100000000;
//    return machine*(aa1*(a11*Math.pow(p,7) + a12)+bb1 + aa2*(a21*Math.pow(p,7) + a22*n*3 + a23)+bb2 + cc1);
//  },
//  
//  close: function(){
//    $('#wait_for_results_dialog').dialog('close');
//  },
//  
//  startRefresh: function(){
//    if (!html.WaitForResultDialog.doRefresh){
//      html.WaitForResultDialog.doRefresh = true;
//      var now = new Date();
//      html.WaitForResultDialog.startTime = now.getTime() / 1000;
//      var pr = LMT.model.Parameters.pixrad;
//      var nm = LMT.model.Parameters.n_models;
//      LMT.settings.estimate = html.WaitForResultDialog.estimate(pr, nm);
//      setTimeout(html.WaitForResultDialog.update,1);
//    }
//  },
//  
//  stopRefresh: function(){
//    html.WaitForResultDialog.doRefresh = false;
//    $('#wait_for_results_dialog').dialog('close');
//  },
//  
//  update: function(){
//    if (html.WaitForResultDialog.doRefresh == true) {
//      var now = new Date();
//      var dt = now.getTime()/1000 - html.WaitForResultDialog.startTime;
//      $('#wfrd_running').html(dt.toFixed(1));
//      $('#wfrd_est').html(LMT.settings.estimate.toFixed(1));
//      setTimeout(function(){html.WaitForResultDialog.update()},100);
//    }
//    else {
//      $('#wfrd_running').html(0);
//      $('#wfrd_est').html(0);
//    }
//  },
//  
//};

//v2 this is outdated
/*
html.SelectDatasourceDialog = {
  init: function(){
    $('#select_datasource_dialog').dialog({
      autoOpen: false,
      minWidth: 550,
      minHeight: 550,
      modal: true,
      open: function(){
        var uname = $.cookie('username');
        if (uname){
          $("#username").val(uname);
          $('.ui-dialog-buttonpane button:last').focus();
        }
        var ds = $.cookie('ds');
        if (ds){$("#sel_datasource").val(ds).trigger("liszt:updated");}
      },
      buttons: [
      {
        text: "Delete defaults",
        click: function(){
          $("#username").val('');
          $.removeCookie('username');
          $.removeCookie('ds');
        }
      },
      {
        text: "Save defaults",
        click: function(){
          $.cookie('username', $("#username").val(), { expires: 365 });
          $.cookie('ds', $("#sel_datasource").val(), { expires: 365 });
        }
      },
      {
        text: "Ok",
        click: function(evt){
          var val = $("#sel_datasource").val();
          if (!val){
            alert("Please choose one datasource to continue");
            return;
          }
          else {
            var uname = $("#username").val();
            LMT.settings.username = uname;
            $.event.trigger("GetDatasourceDialog", [id = val, uname=uname]);
            $('#select_datasource_dialog').dialog("close");
          }
        }
        
      },
      ]
        
    });

    $("#sel_datasource").chosen({allow_single_deselect:true});
    
  },
  
  //event handler
  show: function(evt){
    $.event.trigger("GetDatasourcesList");
    $('#select_datasource_dialog').dialog("open");
  },
  
  // gets triggered if we received the list of all available datasources
  onRcvDatasourcesList: function(evt, jsonDatasourcesList){

    var $selectObj = $("#sel_datasource");

    for (var i=0; i<jsonDatasourcesList.length; i++){
      var x = jsonDatasourcesList[i];
      var elem = $('<option value="' + i + '">'
        + x.id + ' (' + x.desc + ')</option>');
      $selectObj.append(elem);
    }
    var ds = $.cookie('ds');
    ds = ds ? ds : jsonDatasourcesList.length-1;
    $selectObj.val(ds);
    $selectObj.trigger("liszt:updated");
  }
}
*/


//
//html.SelectDatasourceDialog = {
////    call: function(evt){
////        $.event.trigger("GetSelectDatasourceDialog");
////    },
//    
//    show: function(evt, html) {
//        var self = $(html).dialog({
//            autoOpen: false,
//            minWidth: 550,
//            minHeight: 550,
//            modal: true,
//            open: function(){
//                var uname = $.cookie('username');
//                if (uname){
//                    $("#username").val(uname);
//                    $('.ui-dialog-buttonpane button:last').focus();
//                }
//                var ds = $.cookie('ds');
//                if (ds){$("#sel_datasource").val(ds).trigger("liszt:updated");}
//            },
//            buttons: [
//                {
//                    text: "Delete defaults",
//                    click: function(){
//                        $("#username").val('');
//                        $.removeCookie('username');
//                        $.removeCookie('ds');
//                    }
//                },
//                {
//                    text: "Save defaults",
//                    click: function(){
//                        $.cookie('username', $("#username").val(), { expires: 365 });
//                        $.cookie('ds', $("#sel_datasource").val(), { expires: 365 });
//                    }
//                },
//                {
//                    text: "Ok",
//                    click: function(evt){
//                        var val = $("#sel_datasource").val();
//                        if (!val){
//                            alert("Please choose one datasource to continue");
//                            return;
//                        }
//                        else {
//                            var uname = $("#username").val();
//                            LMT.settings.username = uname;
//                            self.dialog("close");
//                            $.event.trigger("GetDatasourceDialog", [id = val, uname = uname]);
//                        }
//                    }
//
//                },
//            ]
//        }).dialog("open")
//    }
//}

html.SelectDatasourceDialog = {
//    call: function(evt){
//        $.event.trigger("GetSelectDatasourceDialog");
//    },
    
    show: function(evt, html, jsobj) {
        var self = $(html).dialog(jsobj).dialog("open")
    }
}



// generic lens selecetion dialog, this will be modified by an ajax request
html.GenericDatasourceDialog = {
  init: function(evt, jsonDialogData){
    
    var dd = jsonDialogData;

    //add the html, construct the dialog    
    $('#generic_datasource_dialog').append(dd.html);
    
    //execute the javascript
    LMT.datasources[dd.id].init();
    
    $('#generic_datasource_dialog').dialog({
      title: dd.title,
      autoOpen: false,
      minWidth: 550,
      minHeight: 550,
      modal: true,
      open: function(){},
      buttons: [
      { id: "btn_gdd_ok",
        text: "Ok",
        click: function(evt){
          $.event.trigger("LensesSelected");
        }
      }
      ]
        
    });
    LMT.ui.html.GenericDatasourceDialog.show()
  },
  
  //event handler
  show: function(evt){
    $('#generic_datasource_dialog').dialog("open");
  },
  
}














html.SelectModelDialog = {
  
  init: function() {
    
    $('#select_model_dialog').dialog({
      autoOpen: false,
      minWidth: 550,
      minHeight: 550,
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
          tmp1 = $("#selmod_cat").val();
          //tmp2 = $("#selmod_lens").val();
          tmp3 = $("#selmod_lens").val();
          if (!tmp1 && !tmp3){ // if both null
            alert("please choose at least one lens or a catalog");
            return;
          }
          else {
            if (tmp3) {
              for(var i=0; i<tmp3.length;i++) {tmp3[i] = +tmp3[i];} //parse to int
            }
            else {tmp3='';}
            $.event.trigger("GetModelData", [models = tmp3, catalog=+$("#selmod_cat").val(), action='init']);
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








/** V2 WIP
 * initalises the toolpars on the top and the one on the input / left side
 */
html.Toolbar = {
  init: function() {
  
  	$("#toolbarGrp1 button")
  	 .add("#toolbarGrp1 input")
  	 .add("#toolbarTop button")
  	 .add("#toolbarTop input")
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
  	
  	
  	//init top buttons correctly
    $('#btnMainActionPrev').on('click', function() {$.event.trigger('GetModelData', [null,null,'prev']);})
    $('#btnMainActionNext').on('click', function() {$.event.trigger('GetModelData', [null,null,'next']);})
    $("#toolbarGrpTop button").button("disable");
    $('#btnMainHelp').button("enable");
    $('#btnMainHelp').prop('checked', true);
    $('#btnMainHelp').change(); 	
  	
    // make buttongroups
    $("#toolbarGrp1 > .btnset").buttonset();
    $("#toolbarGrpTop > .btnset").buttonset();
  	

    //set buttons to correct state 
    
    //mode radio buttons	
    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
    $('input[name="mode"]').change();
    
    //un/re do buttons:
    $('#btnInUndo').add('#btnInRedo').button("disable");
    $('#btnInSettingsColor').button("disable");
    
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
    
    $.event.trigger("HideAllTooltips"); //workaround for stuck tooltips of deact. buttons
  },
  
    /** V2
     * updates the top toolbar buttons 
     */
    updateTop: function(evt) {
    
        if (evt.type=="ReceivedSimulation") {
            // that means we sent our model to th server and checked it,
            // we can save this as final result
            LMT.settings.renderedEqualsModel = true;

        } else if (evt.type=="ActionStackUpdated") {
            // means that something changed on the model.. user need to check the
            // output before saving 
            LMT.settings.renderedEqualsModel = false;

        } else {
            // this shouldn't happend
            LMT.settings.renderedEqualsModel = false;
        };

        // prev and next buttons are not in use
        $('#btnMainActionPrev').button("disable");
        $('#btnMainActionNext').button("disable");

        // set the final model save button accordingly
        $('#btnMainFinish').button(
            LMT.settings.renderedEqualsModel ? "enable" : "disable"
        );

        //workaround for stuck tooltips of deact. buttons
        $.event.trigger("HideAllTooltips"); 
    },

    

  /**
   * fires an event when a toolbar button is pressed 
   */
  fire: function(evt){
    $.event.trigger(evt.data.name, evt.data.value);
  }
}



// OLD Toolbar, new V2 above

///**
// * initalises the toolpars on the top and the one on the input / left side
// */
//html.Toolbar = {
//  init: function() {
//  
//  	$("#toolbarGrp1 button")
//  	 .add("#toolbarGrp1 input")
//  	 .add("#toolbarTop button")
//  	 .add("#toolbarTop input")
//  	 .each(function(){
//  		
//  		var $this = $(this);
//  		var icon = $this.data("icon");
//  		var eventName = $this.data("event");
//  		var value = $this.data("value");
//  		
//  		$(this).button({
//  			text: false,
//  			disabled: false,
//  			icons: {primary: icon }
//  		})
//  		.on('click', {name:eventName, value: value} , LMT.ui.html.Toolbar.fire);
//  	});
//  	
//  	
//  	//init top buttons correctly
//    $('#btnMainActionPrev').on('click', function() {$.event.trigger('GetModelData', [null,null,'prev']);})
//    $('#btnMainActionNext').on('click', function() {$.event.trigger('GetModelData', [null,null,'next']);})
//    $("#toolbarGrpTop button").button("disable");
//    $('#btnMainHelp').button("enable");
//    $('#btnMainHelp').prop('checked', true);
//    $('#btnMainHelp').change(); 	
//  	
//    // make buttongroups
//    $("#toolbarGrp1 > .btnset").buttonset();
//    $("#toolbarGrpTop > .btnset").buttonset();
//  	
//
//    //set buttons to correct state 
//    
//    //mode radio buttons	
//    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
//    $('input[name="mode"]').change();
//    
//    //un/re do buttons:
//    $('#btnInUndo').add('#btnInRedo').button("disable");
//    $('#btnInSettingsColor').button("disable");
//    
//  },
//  
//  /**
//   * updates the buttons
//   */
//  update: function(evt) {
//    //radiobuttons for mode selection 
//    $('input[data-value="'+LMT.settings.mode+'"]')[0].checked = true;
//    $('input[name="mode"]').change();
//    // un / redo buttons whether there is something to be undone / redone
//    $('#btnInUndo').button(LMT.actionstack.undoSize>0 ? "enable" : "disable");
//    $('#btnInRedo').button(LMT.actionstack.redoSize>0 ? "enable" : "disable");
//    
//    $.event.trigger("HideAllTooltips"); //workaround for stuck tooltips of deact. buttons
//  },
//  
//  /**
//   * updates the top toolbar buttons 
//   */
//  updateTop: function(evt) {
//    
//    if (evt.type=="ReceivedSimulation") {
//      //that means we sent our model to th server and checked it, we can save this as final result
//      LMT.settings.renderedEqualsModel = true;
//    }
//    else if (evt.type=="ActionStackUpdated") {
//      // means that something changed on the model.. user need to check the output before saving 
//      LMT.settings.renderedEqualsModel = false;
//    }
//    else {LMT.settings.renderedEqualsModel = false;} //this shouldn't happend
//    
//    $('#btnMainActionPrev').button(LMT.modelData.prevAvail ? "enable" : "disable");
//    $('#btnMainActionNext').button(LMT.modelData.nextAvail ? "enable" : "disable");
//    $('#btnMainFinish').button(LMT.settings.renderedEqualsModel ? "enable" : "disable");
//    
//    $.event.trigger("HideAllTooltips"); //workaround for stuck tooltips of deact. buttons
//  },
//  
//  /**
//   * fires an event when a toolbar button is pressed 
//   */
//  fire: function(evt){
//    $.event.trigger(evt.data.name, evt.data.value);
//  }
//}



// OLD dialog, V2 not implemented yet (events -> on ReceivedModelData)
//html.ColorSettingsDialog = {
//  init: function(){	
//	
//  		// multiply the color settings tools for n channels
//  	var $parent = $('#cd_table');
//  	var $elem = $("#cd_table > .cd_row");
//  	var ch = LMT.modelData.ch;
//  	
//  	for (var i = 1; i<ch.length; i++){
//  		$clone = $elem.clone(true, true);
//  		var e = $clone.find('*');
//  		e.data('id', i);
//  		e.first().children().text("Ch"+(i+1));
//  		$clone.appendTo($parent);
//  	}
//  	
//  	
//  	// color picker dialog
//    $('#color_dialog').dialog({
//  	 	autoOpen: false,
//  		minWidth: 500,
//  		open: function(){
//  			 $('.mycp').each(function(i, val){
//  			   //get color in hex notation   
//           var str = (1 << 24) | (ch[i].r*255 << 16) | (ch[i].g*255 << 8) | ch[i].b*255;
//           $(this).val('#' + str.toString(16).substr(1)).focus();
//           
//           // hack that should update the field so they get their color from beginning
//           /*
//           var press = jQuery.Event("keyup");
//           press.ctrlKey = false;
//           press.which = 13;
//           $(this).trigger(press);*/
//  			 });
//  			 
//  		}
//  	});
//  	
//  	
//  	//sliders
//  	$('#color_dialog .slider').slider({
//  		max: 1,
//  		min: -1,
//  		value: 0,
//  		step: 0.05,
//  		slide: function(evt, ui) {
//  		  //only update labels
//        var value = ui.value;
//        var type = $(this).data("type");
//        if (type=="contrast"){
//          value = Math.pow(10, value); //change range from [-1...1] to [0.1 ... 10]
//        }
//        $(this).parent().siblings('.cd_cell_value').children().text(value.toFixed(2));
//  		},
//  		stop: function(evt, ui) {
//  			var value = ui.value;
//  			var type = $(this).data("type");
//  			var id = $(this).data("id");
//  			
//  			if (type=="contrast"){
//  				value = Math.pow(10, value); //change range from [-1...1] to [0.1 ... 10]
//  			}
//  			
//  			LMT.modelData.ch[id][type.substr(0,2)] = value;
//  			//log("stopped sliding");
//  			$.event.trigger('ChangedModelData', id);
//  		}
//  		
//  	});
//  	
//  	var e = $('.cd_cell_value > p');
//  	e.filter(':even').text("1.00");
//    e.filter(':odd').text("0.00");
//  	
//	  // if color image, hide color settings
//	  if (LMT.modelData.img_type == "CO"){
//	    $(".cd_cell_cp").add(".cd_cell_name").hide();
//	  }
//	
//	
//  	$('.mycp').colorpicker({
//  		parts: ['header',
//  			'map',
//  			'bar',
//  			//'hex',
//  			//'hsv',
//  			//'rgb',
//  			//'alpha',
//  			//'lab',
//  			//'cmyk',
//  			//'preview',
//  			'swatches',
//  			'footer'],
//  		colorFormat: '#HEX',
//  		showOn: 'both',
//  		buttonColorize: true,
//  		altField: '',
//  		buttonImage: 'img/cp/ui-colorpicker.png',
//  		buttonImageOnly: false,
//  		buttonText: 'pick',
//  		showOn: 'button',
//  		close: function(evt, data){
//  			var id= $(this).data("id");
//  			$(this).css('background', data.formatted);
//  			LMT.modelData.ch[id].r = data.rgb.r;
//  			LMT.modelData.ch[id].g = data.rgb.g;
//  			LMT.modelData.ch[id].b = data.rgb.b;
//  			//log("picked color for "+id);
//  			$.event.trigger('ChangedModelData', id);
//  		},
//  	});
//  	
//  	$parent.parent().removeClass("initHidden");
//  	
//  },
//  
//  show: function(){
//    $('#color_dialog')
//      .dialog("open");
//  }
//  
//  
//  
//}
//


html.ColorSettingsOutputDialog = {
  init: function(){ 
  
   
    
    // color picker dialog
    $('#color_out_dialog').dialog({
      autoOpen: false,
      minWidth: 500,
      open: function(){
        LMT.ui.html.ColorSettingsOutputDialog.refresh();
      }
    });
    
    
    //sliders
    $('#color_out_dialog .slider').slider({
      max: 1,
      min: -1,
      value: 0,
      step: 0.01,
      slide: function(evt, ui) {
        var value = ui.value;
        var type = $(this).data("type");
        var i = LMT.ui.out.shownImage;
        
        if (type=="contrast"){
          value = Math.pow(10, value); //change range from [-1...1] to [0.1 ... 10]
          LMT.settings.display.out[i].co = value;
        }
        else {
          LMT.settings.display.out[i].br = value;
        }
        
        //log("stopped sliding");
        $(this).parent().siblings('.cd_cell_value').children().text(value.toFixed(2));
        $.event.trigger('RedrawCurrentOutput');
      },
      stop: function(evt, ui) {
        var value = ui.value;
        var type = $(this).data("type");
        var i = LMT.ui.out.shownImage;
        
        if (type=="contrast"){
          value = Math.pow(10, value); //change range from [-1...1] to [0.1 ... 10]
          LMT.settings.display.out[i].co = value;
        }
        else {
          LMT.settings.display.out[i].br = value;
        }
        
        //log("stopped sliding");
        $.event.trigger('RedrawCurrentOutput');
      }
      
    });
    
    var e = $('.cd_cell_value > p');
    e.filter(':even').text("1.00");
    e.filter(':odd').text("0.00");
    

    $('#color_out_dialog').removeClass("initHidden");
    
  },
  
  show: function(){
    $('#color_out_dialog')
      .dialog("open")
      .dialog('widget').position({
          my: "left center",
          at: "left center",
          of: $('#inp')
      });
  },
  
  
  /**
   * sets the sliders to the current values 
   */
  refresh: function() {
    var co = LMT.settings.display.out[LMT.ui.out.shownImage].co;
    var co10 = Math.log(co) / Math.LN10;
    var br = LMT.settings.display.out[LMT.ui.out.shownImage].br
    $("#cod_br").slider( "option", "value", br )
      .parent().siblings('.cd_cell_value').children().text(br.toFixed(2));
    $("#cod_co").slider( "option", "value", co10 )
      .parent().siblings('.cd_cell_value').children().text(co.toFixed(2));
    
  }
  
}


  	
	
	
html.DisplaySettingsDialog = {

  init: function(){
  
  	/**********************
  	 * the display settings dialog 
  	 */
  	$("#display_dialog").dialog({
  		autoOpen: false,
  		minWidth: 200,
  		open: function(){ //update button status
  			// .change is a bugfix, as described here: http://stackoverflow.com/questions/8796680/jqueryui-button-state-not-changing-on-prop-call
        $('#ds_all').prop("checked", LMT.settings.display.paintConnectingLines).change();
  			$('#conn_l').prop("checked", LMT.settings.display.paintConnectingLines).change();
  			$('#cont_p').prop("checked", LMT.settings.display.paintContourPoints).change();
  			$('#cont_l').prop("checked", LMT.settings.display.paintContours).change();
  		}
  	});
  	
  	//$('#dsettings').buttonset();
  	
  	$('#conn_l').button().click(function(evt){
  		LMT.settings.display.paintConnectingLines = this.checked;
  		$.event.trigger('ChangedDisplaySettings');
  	});
  	$('#cont_p').button().click(function(evt){
  		LMT.settings.display.paintContourPoints = this.checked;
      $.event.trigger('ChangedDisplaySettings');
  	})
  	$('#cont_l').button().click(function(){
  		LMT.settings.display.paintContours = this.checked;
      $.event.trigger('ChangedDisplaySettings');
  	});
  	
  	$('#ds_all').button().click(function(evt){
      LMT.settings.display.paintModel = this.checked;
      $.event.trigger('ToggleModelDisplay');
  	});
  	
  	
  	$("#display_dialog").removeClass("initHidden");
  	
	},
	
	show: function() {
	  $('#display_dialog')
	    .dialog("open")
  	  .dialog('widget').position({
          my: "center bottom",
          at: "center bottom",
          of: $('body')
      });
	}
}
	


html.GlassSettingsDialog = {
  init: function(){
    $("#glass_dialog").dialog({
      autoOpen: false,
      minWidth: 400,
      open: function(){
        
        // assign correct values to sliders
        $("#gset_redshift_slide").slider("values",
          [LMT.model.Parameters.z_lens|| 0.5 ,
          LMT.model.Parameters.z_src || 1]);
        $("#gset_pixrad_slide").slider("value", LMT.model.Parameters.pixrad || 8);
        $("#gset_nmodels_slide").slider("value", LMT.model.Parameters.n_models || 200);
        $("#gset_issymm").prop("checked", LMT.model.Parameters.isSym || false).change();
      }
    });
    
    
    $("#gset_redshift_slide").slider({
      range: true,
      min: 0,
      max: 2,
      step: 0.01,
      values: [0.5, 1], //default value will be set on open of diaalog..
      change: function(evt, ui){
        $("#gset_redshift_out").html("(Lens: " + ui.values[0] + " / Source: " + ui.values[1] + ")");
      },
      slide: function(evt, ui){
        $("#gset_redshift_out").html("(Lens: " + ui.values[0] + " / Source: " + ui.values[1] + ")");
      },
      stop: function(evt, ui){
        LMT.model.Parameters.z_lens = ui.values[0];
        LMT.model.Parameters.z_src = ui.values[1];
        
      }
    });
    

    $("#gset_pixrad_slide").slider({
      range: false,
      min: 5,
      max: 12,
      step: 1,
      value: 8, //default value will be set on open of dialog..
      slide: function(evt, ui){
        $("#gset_pixrad_out").html("("+ui.value+")");
      },
      change: function(evt, ui){
        $("#gset_pixrad_out").html("("+ui.value+")");
      },
      stop: function(evt, ui){
        LMT.model.Parameters.pixrad = ui.value;
      }
    });


    $("#gset_nmodels_slide").slider({
      range: false,
      min: 50,
      max: 2000,
      step: 50,
      value: 200, //default value will be set on open of diaalog..
      slide: function(evt, ui){
        $("#gset_nmodels_out").html("("+ui.value+")");
      },
      change: function(evt, ui){
        $("#gset_nmodels_out").html("("+ui.value+")");
      },
      stop: function(evt, ui){
        LMT.model.Parameters.n_models = ui.value;
      }
    });
    
    $("#gset_issymm")
      .button()
      .click(function( evt ) {
        var $btn = $(this);
        var state = !($btn.attr("checked")? true : false); //get old state, invert it to have new state
        $btn.attr("checked", state);
        LMT.model.Parameters.isSym = state;
        $btn.button( "option", "label", state ? "Yes" : "No" );
      });

    
    //set defaults
    $("#gset_redshift_out").html("(Lens: " + $("#gset_redshift_slide").slider( "values", 0 ) + " / Source: " + $("#gset_redshift_slide").slider( "values", 1 ) + ")");
    
    LMT.model.Parameters.pixrad = $("#gset_pixrad_slide").slider( "value");
    $("#gset_pixrad_out").html("(" + $("#gset_pixrad_slide").slider( "value") + ")");

    LMT.model.Parameters.n_models = $("#gset_nmodels_slide").slider("value");
    $("#gset_nmodels_out").html("(" + $("#gset_nmodels_slide").slider( "value") + ")");
   
    //LMT.model.Parameters.isSym = $("#gset_issymm").attr('checked') ? true : false;
    LMT.model.Parameters.isSym = true;
    $("#gset_issymm").attr('checked', true);
    $("#gset_issymm").button("option", "label", "Yes");
    
   
    $("#glass_dialog").removeClass("initHidden");
  },
  
  show: function() {
    $('#glass_dialog')
      .dialog("open")
      .dialog('widget').position({
          my: "center center",
          at: "center center",
          of: $('body')
      });
  }
}




/** V2 WIP
 * second try to do tooltips, this time use jqyerys tooltips 
 */
html.Tooltip2 = {
  init: function(item){
    var item = item || '*';
    $(item).tooltip({
      content: LMT.ui.html.Tooltip2.content,
      close:   LMT.ui.html.Tooltip2.close,
      tooltipClass: 'ttip'
    });
  },

  content: function(response) {
    
    var tag = this.tagName;
    var $this = null
    
    if (tag=='LABEL') {
      $this = $(this).prev(); //.attr('data-tooltip'); //data('tooltip') doen't work!
    }
    else if (tag=='BUTTON') {
      $this = $(this);
    }
    else {
      return '';
    }
    
    var tit = $this.data("ttipTitle");
    var txt = $this.data("ttipText");
    var lnk = $this.data("ttipLink");
    var key = $this.data("hotkey");

    var html =
      '<span class="titlebox">' + 
      '<span class="title">'+tit+'</span>' + 
      '<span class="close" onclick="LMT.ui.html.Tooltip2.forceClose(event)">[X]</span>' +
      '</span>' + 
      '<span class="txt">'+txt+'</span>';
      
    if (lnk!='' || key!='') {
      html += '<span class="small">';
      if (lnk!='') {html += '<span class="info"><a href="'+lnk+'">...more info</a></span>';}
      if (key!='') {html += '<span class="key">hotkey: '+key+'</span>';}
      html += '</span>';
    }
    
    return html
    // those are equal:
    //return 'haaa'
    //response('haaa')
  },
  
  /**
   * prevent tooltip from closing on mouseover 
   */
  close: function(evt, ui){
    ui.tooltip.hover(
      function(evt){
        $(this).stop(true).fadeTo(400,1);
      },
      function(evt){
        $(this).fadeOut("400", function(){ $(this).remove(); })
      }
    )
  },
  
  /**
   * manually close a tooltip in case it gets stuck
   * there are still many bugs in jqueryui tooltip... 
   */
  forceClose: function(evt){
    $(evt.currentTarget).parent().parent().parent().stop(true).fadeOut(200, function(){
      $(this).remove();
    });
  },
  
    /** V2
     * event to close all stuck tooltips 
     */
    closeAll: function(){
        $('.ttip').stop(true).fadeOut(200, function(){$(this).remove();});
    }
};



// OLD Version bevor V2, new above
///**
// * second try to do tooltips, this time use jqyerys tooltips 
// */
//html.Tooltip2 = {
//  init: function(item){
//    var item = item || '*';
//    $(item).tooltip({
//      content: LMT.ui.html.Tooltip2.content,
//      close:   LMT.ui.html.Tooltip2.close,
//      tooltipClass: 'ttip'
//    });
//  },
//
//  content: function(response) {
//    
//    var tag = this.tagName;
//    var $this = null
//    
//    if (tag=='LABEL') {
//      $this = $(this).prev(); //.attr('data-tooltip'); //data('tooltip') doen't work!
//    }
//    else if (tag=='BUTTON') {
//      $this = $(this);
//    }
//    else {
//      return '';
//    }
//    
//    var tit = $this.data("ttipTitle");
//    var txt = $this.data("ttipText");
//    var lnk = $this.data("ttipLink");
//    var key = $this.data("hotkey");
//
//    var html =
//      '<span class="titlebox">' + 
//      '<span class="title">'+tit+'</span>' + 
//      '<span class="close" onclick="LMT.ui.html.Tooltip2.forceClose(event)">[X]</span>' +
//      '</span>' + 
//      '<span class="txt">'+txt+'</span>';
//      
//    if (lnk!='' || key!='') {
//      html += '<span class="small">';
//      if (lnk!='') {html += '<span class="info"><a href="'+lnk+'">...more info</a></span>';}
//      if (key!='') {html += '<span class="key">hotkey: '+key+'</span>';}
//      html += '</span>';
//    }
//    
//    return html
//    // those are equal:
//    //return 'haaa'
//    //response('haaa')
//  },
//  
//  /**
//   * prevent tooltip from closing on mouseover 
//   */
//  close: function(evt, ui){
//    ui.tooltip.hover(
//      function(evt){
//        $(this).stop(true).fadeTo(400,1);
//      },
//      function(evt){
//        $(this).fadeOut("400", function(){ $(this).remove(); })
//      }
//    )
//  },
//  
//  /**
//   * manually close a tooltip in case it gets stuck
//   * there are still many bugs in jqueryui tooltip... 
//   */
//  forceClose: function(evt){
//    $(evt.currentTarget).parent().parent().parent().stop(true).fadeOut(200, function(){
//      $(this).remove();
//    });
//  },
//  
//  /**
//   * event to close all stuck tooltips 
//   */
//  closeAll: function(){
//    $('.ttip').stop(true).fadeOut(200, function(){$(this).remove();});
//  }
//  
//}



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
    $('body').on('keydown', LMT.ui.html.KeyboardListener.keyEvent);
    //$('body').on('keypress', LMT.ui.html.KeyboardListener.keyEvent);
    //$('body').on('keyup', LMT.ui.html.KeyboardListener.keyEvent);
  },
  
  keyEvent: function(evt){
    evt = evt || window.event;
    
    if (evt.target.tagName=="INPUT") {return;}
    if (evt.target.tagName=="BUTTON") {return;}
    
    var code = evt.keyCode;
    //var code = evt.which || evt.keyCode;
    log('KeyBoardListener | keyEvent: '+evt.type +', '+ evt.keyCode);
    var keyCatched = false;
    
    switch (code) {
      case 96: //num0
      case 48: //0
      case 8: //[backspace]
        $.event.trigger("ZoomPanReset");
        keyCatched = true;
        break;
      
      case 107: //num+
      case 187: // =+
        $.event.trigger("Zoom", [+1]);
        keyCatched = true;
        break;
      case 109: //num-
      case 189: //-_
        $.event.trigger("Zoom", [-1]);
        keyCatched = true;
        break;

      case 49: //1
      case 50: //2
      case 51: //3
      case 52: //4
      //case 53: //5
      //case 54: //6
        $.event.trigger('DisplayOutputSlide', [code-49]);
        keyCatched = true;
        break;
        
      case 81: //Q
        $.event.trigger('Undo');
        keyCatched = true;
        break;
      case 87: //W
        $.event.trigger('Redo');
        keyCatched = true;
        break;

      case 65: //ASD
      case 83: //ASD
      case 68: //ASD
        mode = code==65 ? 'mass' : (code==83?'image':'ruler') ;
        $.event.trigger('SwitchMode', mode);
        keyCatched = true;
        break;

      case 88: //x
        $.event.trigger('SimulateModel');
        keyCatched = true;
        break;

      case 90: //z
        $.event.trigger('ShowDialogGlassSettings');
        keyCatched = true;
        break;


      case 72: //h
        $.event.trigger('ToggleHelpBar');
        keyCatched = true;
        break;

      case 67://c
      case 32://[space]
        $.event.trigger('ShowDialogSaveResult');
        keyCatched = true;
        break;
              
      /*default:
        return;
      */
    }

    if (debug) { //debug keys
      switch (code){
        
        // show log on ` (` + space in some international cases)
        case 96: // `
          $.event.trigger("ToggleLog");
      }
    }

    if (keyCatched){
      if (evt.stopPropagation) {evt.stopPropagation();}
      if (evt.preventDefault) {evt.preventDefault();}
    }
  }
}



/**
 * when in small screen mode, toggles the shown display 
 */
html.ToggleDisplay = function(evt){
  //alert("sliderklick");
  LMT.ui.html.dispState = $("#bigslider").hasClass('left') ? 'left' : 'right';

  if (LMT.ui.html.dispState == 'left') {
    hide = [$("#out"), $("#toolbarOut")];
    show = [$("#inp"), $("#toolbarInp")];
  }
  else {
    show = [$("#out"), $("#toolbarOut")];
    hide = [$("#inp"), $("#toolbarInp")];
  }
  $hide = hide[0].add(hide[1]);
  $show = show[0].add(show[1]);
  
  $show.hide().css("zIndex", 21);
  $hide.css("zIndex", 20);
  
  
  var dur = 200;
  
  $show.fadeIn({duration: dur});
  
  $("#bigslider").fadeOut({
    duration: dur/2,
    done: function() {
      $("#bigslider").toggleClass('left right');  
      $("#bigslider i").toggleClass('icon-double-angle-right icon-double-angle-left');
    }
  });
  $("#bigslider").fadeIn({
    duration: dur/2,
    done: function(){
      $("#bigslider").css('display', '');
    }
  });
  
  /*
  hide[0]
  .css("opacity", 1)
  .animate({opacity: 0}, {
    duration: 100,
    done: function(){
      $(this).css("display", "none");
      $("#bigslider").toggleClass('left right');  
      $("#bigslider i").toggleClass('icon-double-angle-right icon-double-angle-left');
      show[0]
      .css("opacity", 0)
      .animate({opacity: 1}, {duration: 300})
      .css("display", "table-cell");
    }
  });

  hide[1]
  .css("opacity", 1)
  .animate({opacity: 0}, {
    duration: 100,
    done: function(){
      $(this).css("display", "none");
      show[1]
      .css("opacity", 0)
      .animate({opacity: 1}, {duration: 300})
      .css("display", "table-cell");
    }
  });
  **/
  
  /* very nice sliding animation, but it doesn't work with content in divs...
  show[0].animate({width: "100%"},{
    duration: 400,
  }).css("display", "table-cell");

  hide[0].animate({width: "0%"},{
    duration: 400,
    done: function(){$(this).css("display", "none")}
  }).css("display", "table-cell");
  */
  
}


html.HelpBar = {
  
  isShown: function(){
    //get state of button
    var isIt = $("#btnMainHelp")[0].checked;
    return isIt;
  },
  
  init: function() {
    var $t = $("#toolbarGrp1 button")
    .add("#toolbarGrp1 label")
    .add("#toolbarTop button")
    .add("#toolbarTop label")
    .add("#toolbarGrp2 button")
    .add("#toolbarGrp2 label");
    $t.hover( function(evt){$.event.trigger('MouseEnter',evt);},
              function(evt){$.event.trigger('MouseLeave',evt);});
  },
  
  toggle: function(){
    var that = LMT.ui.html.HelpBar;
    if (that.isShown()){
      $("#help").show();
    }
    else {
      $("#help").hide();
    }
  },
  
  show: function(title, body, hotkey, link) {
    var txt = title
      + (hotkey ? " (Hotkey: <i>"+hotkey+"</i>)" : "");
      //+ (link ? " <a href='" + link + "'>further info</a>" : "");
    var t = $("<div class='help title'></div>").html(txt);
    
    //parse string to array
    if (body && typeof(body)=="string") {
      body = body.split("|");
    }

    if (body && typeof(body)=="object") {
      if (body.length==1){
        var b = $("<div class='help body'></div>").html(body[0]);
      }
      else {
        var b = $("<ul class='help list'></ul>");
        for (var i=0;i<body.length;++i){
          b.append($("<li></li>").html(body[i]));
        }
      }
    }
    else {
      var b = null;
    }
    $("#helpcont").empty().append(t).append(b);
  },
  
  MouseLeave: function(){
    $("#helpcont").empty();
  },
  
  MouseEnter: function(a, evt) {
    
    //prevent flickering if fast moving stuff
    if (svg.events.state != 'none') {return;}
    
    var tmp = evt;
    var ctid = evt.currentTarget.id;
    var jsTarget = evt.target.jsObj || null;
    var control = evt.currentTarget.control || null; //for input / labels, get the real element
    var cid = control ? control.id : null;
    
    /*
    var activeLayers = ['masses', 'connectorlines', 'contourlines',
      'contourpoints', 'extremalpoints', 'rulers', 'bg'];
    */

    if (ctid=="extremalpoints"){
      
      var t = "";
      if      (jsTarget.type=="sad") {t += "Saddlepoint";}
      else if (jsTarget.type=="min") {t += "Minima";}
      else if (jsTarget.type=="max") {t += "Maxima";}
      t += jsTarget.isExpanded ? " (expanded)" : " (unexpanded)";
      t += " of the arrival time surface.";
      var b=[];
      b.push("Drag to move");
      b.push("Click to " + (
        jsTarget.isExpanded ?
          "collapse (remove children)": "expand (convert to saddlepoint)"));
      b.push("to remove, " + (
        jsTarget.isRoot ? "use the Undo function" : "collapse the parent saddlepoint"));
      
      html.HelpBar.show(t, b);
    }
    
    else if (ctid == "bg") {
      var t = "Modelling Area";
      var b = [];
      if (LMT.settings.mode=="image"){b.push("Click to mark an Image");}
      else if (LMT.settings.mode=="ruler"){b.push("Click to place a ruler");}
      else if (LMT.settings.mode=="mass"){b.push("Click to place an exernal mass");}
      b.push("(change what to do in the toolbar)");
      b.push("Drag to move the canvas");
      b.push("Mousewheel to zoom in/out, mousewheel press to reset");
      html.HelpBar.show(t, b);
    }
    
    else if (ctid == "contourpoints") {
      var t = "Contor Point (only visual aid, doesn't influence the model)";
      var b = [];
      b.push("Drag to move");
      b.push("Click to doublicate");
      b.push("Move close to next / previous to delete");
      html.HelpBar.show(t,b);
    }

    else if (ctid == "contourlines") {
      var t = "Contor / Isoline for arrival time";
      var b = [];
      b.push("Use points to move");
      b.push("Disable display in toolbar, display settings");
      html.HelpBar.show(t,b);
    }

    else if (ctid == "connectorlines") {
      var t = "Connection";
      var b = [];
      b.push("Visual aid to show parent / child");
      html.HelpBar.show(t,b);
    }
    
    else if (ctid == "masses"){
      var t = "External Point Mass";
      var b = [];
      b.push("Drag the middle point to move");
      b.push("Drag the point on the line to change the amount of mass");
      b.push("Click on middle point to remove");
      html.HelpBar.show(t,b);
    }
    
    else if (ctid == "rulers"){
      var t = "Ruler / Distance Estimation";
      var b = [];
      b.push("Drag the middle point to move");
      b.push("Drag the point on the line expand the circle");
      b.push("Click on middle point to remove");
      html.HelpBar.show(t,b);
    }

    
    
    else if ((ctid && ctid.substr(0,3)=="btn") || (cid && cid.substr(0,3) == "btn")) {
      var $t = control ? $(control) : $(evt.currentTarget);
      html.HelpBar.show($t.data("ttip-title"), $t.data("ttip-text"), $t.data("hotkey"), $t.data("ttip-link"));
    }

    else {
      html.HelpBar.show("unknown element",[]);
    } 
    
  }
}



LMT.ui.html = html;

/*})();*/