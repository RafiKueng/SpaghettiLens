/*************************
 * LMT.events.js
 * 
 * Event Management
 * 
 * here, all possible occuring UI events will be mapped to the according event handlers
 * 
 * events will be triggered at UI elements
 * the according objects listen to those events
 * 
 * below are some shortcut functions for events
 */



var events = {
  
  // special event on startup
  startUp: function(){

    initGetVars()

    // first init some objects in the namespace
    
    LMT.ui.out = new LMT.ui.output(); //TODO change this not to be an object
    LMT.ui.out.init();    
    
    LMT.model = new LMT.objects.Model();
    LMT.model.init();
    
    LMT.actionstack = new LMT.objects.ActionStack();    
    
    
    // then assign handlers
    
    LMT.events.assignHandlers();
    
    
    // then initalise the rest
    
    LMT.ui.html.SelectModelDialog.init();
    LMT.ui.html.Toolbar.init();
    LMT.ui.html.DisplaySettingsDialog.init();
    LMT.ui.html.GlassSettingsDialog.init();
    LMT.ui.html.Tooltip.init();
    LMT.ui.html.KeyboardListener.init();
    
    LMT.ui.svg.initCanvas();

    if (LMT.GET.hasOwnProperty("id")){
      id = parseInt(LMT.GET["id"]);
      $.event.trigger("GetModelData", model_id=id);
    }
    else {
      $.event.trigger("ShowSelectModelDataDialog"); //this will trigger the getmodedata on close
      //LMT.ui.html.SelectModelDialog.show();
    }
    
    //LMT.com.getModelData(id);
    
  },
  
  
  assignHandlers: function() {
    
    // dummy function
    var fnc = function(){return false;}
    
    // get the inital data, available lenses and catalogues, if no identifier provided in get string
    $(document).on('GetInitData', LMT.com.getInitData);
    $(document).on('GotInitData', LMT.ui.html.SelectModelDialog.onInitData);

    // ask the server for a particular modelid
    $(document).on('GetModelData', LMT.com.getModelData);    
    $(document).on('ShowSelectModelDataDialog', LMT.ui.html.SelectModelDialog.show);    
    // the server sent the starting data for the model, like urls to the background image(s) and default color binding
    $(document).on('ReceivedModelData', LMT.ui.html.ColorSettingsDialog.init);
    $(document).on('ReceivedModelData', LMT.ui.html.Toolbar.updateTop);
    $(document).on('ReceivedModelData', LMT.ui.svg.bg.init);
    $(document).on('ReceivedModelData', LMT.events.AppReadyHandler);
    
    //everything is loaded and init
    $(document).on('AppReady', LMT.events.ready);
    
    // the background images / channels color settings were changed
    $(document).on('ChangedModelData', LMT.ui.svg.bg.updateColor);
    

    $(document).on('Undo', LMT.objects.ActionStack.Undo);
    $(document).on('Redo', LMT.objects.ActionStack.Redo);
    $(document).on('SaveModelState', LMT.objects.ActionStack.SaveModelState); //something happend that one can undo
    $(document).on('ActionStackUpdated', LMT.ui.html.Toolbar.update); //lets the buttons know that they need to update themselves


    $(document).on('Zoom', LMT.ui.svg.bg.zoom); // expects 1 arg: +1: zoom in, -1 zoom out;
    $(document).on('Pan', LMT.ui.svg.bg.updateZoomPan);
    $(document).on('ZoomPanReset', LMT.ui.svg.bg.zoomPanReset);


    $(document).on('ShowDialogColorSettings', LMT.ui.html.ColorSettingsDialog.show);
    $(document).on('ShowDialogDisplaySettings', LMT.ui.html.DisplaySettingsDialog.show);
    $(document).on('ShowDialogGlassSettings', LMT.ui.html.GlassSettingsDialog.show); //not yet implemented


    $(document).on('SwitchMode', LMT.ui.svg.SwitchMode);
    $(document).on('ModeSwitched', LMT.ui.html.Toolbar.update);

    
    $(document).on('SaveModel', fnc);
    $(document).on('UploadModel', LMT.com.UploadModel);
    $(document).on('SimulateModel', LMT.events.SimulateModel);
    $(document).one('UpdateRepaintModel', LMT.events.UpdateRepaintModel); //can only be called once, once finished with the update, it reassigns itself
    $(document).on('RepaintModel', LMT.objects.Model.Repaint);

    $(document).on('GetSimulation', LMT.com.GetSimulation);
    $(document).on('ReceivedSimulation', LMT.ui.out.load);
    
    $(document).on('DisplayOutputSlide', LMT.ui.out.show); //needs a id
    $(document).on('DisplayOutputSlideNext', LMT.ui.out.next);
    $(document).on('DisplayOutputSlidePrev', LMT.ui.out.prev);
    $(document).on('DisplayOutputSlideOverview', LMT.ui.out.showOverview); //not yet implemented

    
    $(document).on('CreateRootMinima', LMT.objects.Model.CreateRootMinima);
    // expans or collapses an extremalpoint
    $(document).on('ToggleExtremalPoint', LMT.objects.ExtremalPoint.ToggleExtremalPoint);
    $(document).on('CreateContourPoint', LMT.objects.ContourPoint.Doublicate);
    $(document).on('DeleteContourPoint', fnc);
    $(document).on('MoveObject', LMT.events.MoveObject);
    $(document).on('CreateExternalMass', LMT.objects.Model.CreateExternalMass);
    $(document).on('CreateRuler', LMT.objects.Model.CreateRuler);
    $(document).on('DeleteObject', LMT.objects.Model.RemoveObject); // expects supplied jsObj to be removed

    
    $(document).on('ShowTooltip', html.Tooltip.show);
    $(document).on('HideTooltip', html.Tooltip.hide);
  },
  
  ready: function(){
    //push initial state to actionstack
    $.event.trigger("SaveModelState");
  }
  
}  



/**
 * 
 */
events.AppReadyHandler = function(){
  //TODO maybe some check if everything is really ready
  $.event.trigger("AppReady");
}


/**
 * updates all the coordinates of the model and then repaints it
 * 
 * only make one update per time
 * bind this function to the event, but remove it on the first occurance (.one + one time execution)
 * and only reattach it, onces the update is finished.. 
 */
events.UpdateRepaintModel = function(){
  LMT.model.update();
  LMT.model.paint();
  $(document).one('UpdateRepaintModel', LMT.events.UpdateRepaintModel);
}




/**
 * moves any jsObj on the svg canvas.
 * DON'T trigger a action stack push here
 * this will be called many^100 times 
 */
events.MoveObject = function(evt, jsTarget, svgTarget, coord){
  jsTarget.move(coord, svgTarget);
  $(document).one('UpdateRepaintModel', LMT.events.UpdateRepaintModel);
}



events.SimulateModel = function(){
  $.event.trigger("UploadModel");
  $(document).one('UploadModelComplete', function(){$.event.trigger("GetSimulation");});
}


LMT.events = events;
