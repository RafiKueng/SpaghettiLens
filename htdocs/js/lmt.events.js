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

    LMT.ui.html.Toolbar.init();
    LMT.ui.html.DisplaySettingsDialog.init();
    LMT.ui.html.Tooltip.init();
    LMT.ui.html.KeyboardListener.init();

    LMT.ui.svg.initCanvas();
    LMT.ui.out = new LMT.ui.output(); //TODO change this not to be an object
    LMT.ui.out.init();
    
    LMT.model = new LMT.objects.Model();
    LMT.model.init();
    
  },
  
  
  assignHandlers: function() {
    
    // dummy function
    var fnc = function(){return false;}
    
    // the server sent the starting data for the model, like urls to the background image(s) and default color binding
    $(document).on('ReceivedModelData', LMT.ui.html.ColorSettingsDialog.init);
    $(document).on('ReceivedModelData', LMT.ui.svg.bg.init);
    
    // the background images / channels color settings were changed
    $(document).on('ChangedModelData', LMT.ui.svg.bg.updateColor);
    

    $(document).on('Undo', fnc);
    $(document).on('Redo', fnc);
    $(document).on('ActionStackUpdated', fnc);


    $(document).on('Zoom', LMT.ui.svg.bg.zoom); // expects 1 arg: +1: zoom in, -1 zoom out;
    $(document).on('Pan', LMT.ui.svg.bg.updateZoomPan);
    $(document).on('ZoomPanReset', LMT.ui.svg.bg.zoomPanReset);


    $(document).on('ShowDialogColorSettings', LMT.ui.html.ColorSettingsDialog.show);
    $(document).on('ShowDialogDisplaySettings', LMT.ui.html.DisplaySettingsDialog.show);


    $(document).on('SwitchMode', LMT.ui.svg.SwitchMode);
    $(document).on('ModeSwitched', LMT.ui.html.Toolbar.update);

    
    $(document).on('SaveModel', fnc);
    $(document).on('UploadModel', fnc);
    $(document).on('SimulateModel', fnc);
    $(document).one('UpdateRepaintModel', LMT.events.UpdateRepaintModel); //can only be called once, once finished with the update, it reassigns itself
    $(document).on('RepaintModel', LMT.objects.Model.Repaint); //can only be called once, once finished with the update, it reassigns itself

    
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
  $(document).one('UpdateRepaintModel', events.UpdateRepaintModel);
}




/**
 * moves any jsObj on the svg canvas.
 * DON'T trigger a action stack push here
 * this will be called many^100 times 
 */
events.MoveObject = function(evt, jsTarget, svgTarget, coord){
  jsTarget.move(coord, svgTarget);
  $(document).one('UpdateRepaintModel', events.UpdateRepaintModel);
}



LMT.events = events;