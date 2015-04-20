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



var events = {};

// special event on startup
events.startUp = function () {

    initGetVars();

    // first init some objects in the namespace
    LMT.model = new LMT.objects.Model();
    LMT.model.init();

    LMT.actionstack = new LMT.objects.ActionStack();    

    // then assign handlers
    LMT.events.assignHandlers();

    // then initalise the rest
    LMT.ui.out.init();    
    LMT.ui.html.SelectModelDialog.init();
    LMT.ui.html.Toolbar.init();
    LMT.ui.html.DisplaySettingsDialog.init();
    LMT.ui.html.GlassSettingsDialog.init();
    LMT.ui.html.ColorSettingsOutputDialog.init();
    LMT.ui.html.SaveModelDialog.init();
    LMT.ui.html.WaitForResultDialog.init();
    LMT.ui.html.SetUsernameDialog.init();

    LMT.ui.html.HelpBar.init();

    LMT.ui.html.Tooltip.init();
    LMT.ui.html.Tooltip2.init();
    //LMT.ui.html.KeyboardListener.init(); //only load when app is ready, no more dialogs

    LMT.ui.svg.initCanvas();


    //v2    LMT.ui.html.SelectDatasourceDialog.init();
    LMT.ui.html.LoadProgressDialog.init();

    /*
    $.event.trigger("ShowSelectDatasourceDialog");
    */


    if (LMT.GET.hasOwnProperty("mid")){
        var mid = parseInt(LMT.GET["mid"]);
        $.event.trigger("GetModelData", [[mid],'','init']);
        $.event.trigger("SetUsername");

    } else if (LMT.GET.hasOwnProperty("rid")) {
        rid = parseInt(LMT.GET["rid"]);
        var loadResult = function(res_data) {
            var mid = res_data.model_id;
            jsonStr = res_data.json_str;

            $.event.trigger("GetModelData", [[mid],'','init']);
            LMT.model = Model.getModelFormJSONString(jsonStr);
            $.event.trigger("UpdateRepaintModel");
            LMT.modelData.parentId = rid;
        };

        $.event.trigger("GetAndLoadResult", [rid, loadResult]);
        $.event.trigger("SetUsername");
    } else {
        //v2      $.event.trigger("ShowSelectDatasourceDialog");
        $.event.trigger("GetSelectDatasourceDialog");
    };
};
  
events.assignHandlers = function() {
    
    // dummy function
    var fnc = function(){return false;}
    
    


// ---------- the new event handlers ----------------------
    // This are the new and tested assignments

    $(document).on('GetSelectDatasourceDialog', LMT.com.getSelectDatasourceDialog);
    $(document).on('GotSelectDatasourceDialog', LMT.ui.html.SelectDatasourceDialog.show);

    $(document).on('LensSelected', LMT.com.getLensData);

    //$(document).on('ReceivedModelData', LMT.ui.html.ColorSettingsDialog.init); //for now, this is not used
    $(document).on('ReceivedModelData', LMT.ui.html.Toolbar.updateTop);
    $(document).on('ReceivedModelData', LMT.ui.svg.bg.init);
    $(document).on('ReceivedModelData', LMT.events.AppReadyHandler); // only fires AppReady atm

    //everything is loaded and init
    $(document).on('AppReady', LMT.events.ready);
      
      
      
    $(document).on('HideAllTooltips', html.Tooltip2.closeAll); // should be called whenever a button gets deactivated due to a bug in jquery ui tooltip

    $(document).on('RefreshBackgroundImage', LMT.ui.svg.bg.refreshBackgroundImage);
      
      //$(document).on('ShowDialogColorSettings', LMT.ui.html.ColorSettingsDialog.show); // not in use atm


    // old pipline, completly replaced by the stuff below
//    $(document).on('UploadModel', LMT.com.UploadModel);
//    $(document).on('SimulateModel', LMT.events.SimulateModel);
//    $(document).on('ReceivedSimulation', LMT.ui.out.load);
//    $(document).on('ReceivedSimulation', LMT.ui.html.Toolbar.updateTop);
//    $(document).on('ReceivedSimulation', LMT.ui.html.WaitForResultDialog.stopRefresh);

    $(document).on('SimulateModel', LMT.events.SimulateModel);
    $(document).on('UploadModel', LMT.com.UploadModel);
    $(document).on('UploadModelComplete', LMT.events.onUploadComplete);
    $(document).on('StartRendering', LMT.com.StartRendering);
    $(document).on('StartRendering', LMT.ui.html.WaitForResultDialog.show);
    $(document).on('GetRenderingProgress', LMT.com.GetRenderingProgress);
    $(document).on('UpdateRenderingStatus', LMT.ui.html.WaitForResultDialog.update); // if received a new status, this triggers an update of the status display
    $(document).on('RenderingFailed', LMT.ui.html.WaitForResultDialog.close);
    $(document).on('RenderingComplete', LMT.ui.html.WaitForResultDialog.close);
    
    // those still need overhaul
    $(document).on('RenderingComplete', LMT.ui.out.load);
    $(document).on('RenderingComplete', LMT.ui.html.Toolbar.updateTop);
    
    $(document).on('DisplayOutputSlide', LMT.ui.out.show); //needs a id
    
    $(document).on('ShowDialogSaveResult', LMT.ui.html.SaveModelDialog.show);
    $(document).on('ConvertInputImageToPNG', LMT.ui.svg.ConvertToPNG);

    $(document).on('InputImageGenerated', LMT.ui.html.SaveModelDialog.generatedImage);
    $(document).on('SaveModel', LMT.com.SaveModel);  // upload model with is final tag
    $(document).on('SavedModel', LMT.ui.html.SaveModelDialog.savedModel);  // if successful saved
    
    
    
// ---------- the old ones ----------------------

    $(document).on('ToggleLog', logger.toggle);

//    $(document).on('ShowSelectDatasourceDialog', LMT.ui.html.SelectDatasourceDialog.show);
//    $(document).on('GetDatasourcesList', LMT.com.getDatasourcesList);
//    $(document).on('RcvDatasourcesList', LMT.ui.html.SelectDatasourceDialog.onRcvDatasourcesList);
    //$(document).on('ShowSelectDatasourceDialog', LMT.ui.html.SelectDatasourceDialog.call);

      
      
//    $(document).on('GetDatasourceDialog', LMT.com.getDatasourceDialog);
//    $(document).on('RcvDatasourceDialog', LMT.ui.html.GenericDatasourceDialog.init);
      

    $(document).on('GetAndLoadResult', LMT.com.getAndLoadResult);
    $(document).on('SetUsername', LMT.ui.html.SetUsernameDialog.show);
    
    $(document).on('ToggleDisplay', LMT.ui.html.ToggleDisplay);
    $(document).on('ToggleHelpBar', LMT.ui.html.HelpBar.toggle);
    $(document).on('MouseEnter', LMT.ui.html.HelpBar.MouseEnter);
    $(document).on('MouseLeave', LMT.ui.html.HelpBar.MouseLeave);
    $(document).on('MouseEnter', LMT.ui.svg.events.hoverIn);
        
    // get the inital data, available lenses and catalogues, if no identifier provided in get string
    $(document).on('GetInitData', LMT.com.getInitData);
    $(document).on('GotInitData', LMT.ui.html.SelectModelDialog.onInitData);

    // ask the server for a particular modelid
    $(document).on('GetModelData', LMT.com.getModelData);    
    $(document).on('ShowSelectModelDataDialog', LMT.ui.html.SelectModelDialog.show);    
    // the server sent the starting data for the model, like urls to the background image(s) and default color binding
//    $(document).on('ReceivedModelData', LMT.ui.html.ColorSettingsDialog.init);
//    $(document).on('ReceivedModelData', LMT.ui.html.Toolbar.updateTop);
//    $(document).on('ReceivedModelData', LMT.ui.svg.bg.init);
//    $(document).on('ReceivedModelData', LMT.events.AppReadyHandler);

//    $(document).on('RefreshBackgroundImage', LMT.ui.svg.bg.refreshBackgroundImage);

    
    //everything is loaded and init
//    $(document).on('AppReady', LMT.events.ready);
    
    // the background images / channels color settings were changed
    $(document).on('ChangedModelData', LMT.ui.svg.bg.updateColor);
    
    //display settings were changed
    $(document).on('ChangedDisplaySettings', LMT.ui.svg.updateDisp);
    $(document).on('ToggleModelDisplay', LMT.ui.svg.toggleModelDisplay);

    $(document).on('Undo', LMT.objects.ActionStack.Undo);
    $(document).on('Redo', LMT.objects.ActionStack.Redo);
    $(document).on('SaveModelState', LMT.objects.ActionStack.SaveModelState); //something happend that one can undo
    $(document).on('ActionStackUpdated', LMT.ui.html.Toolbar.update); //lets the buttons know that they need to update themselves
    $(document).on('ActionStackUpdated', LMT.ui.html.Toolbar.updateTop); //lets the buttons know that they need to update themselves

    $(document).on('Zoom', LMT.ui.svg.bg.zoom); // expects 1 arg: +1: zoom in, -1 zoom out;
    $(document).on('Pan', LMT.ui.svg.bg.updateZoomPan);
    $(document).on('ZoomPanReset', LMT.ui.svg.bg.zoomPanReset);


//    $(document).on('ShowDialogColorSettings', LMT.ui.html.ColorSettingsDialog.show);
    $(document).on('ShowDialogDisplaySettings', LMT.ui.html.DisplaySettingsDialog.show);
    $(document).on('ShowDialogGlassSettings', LMT.ui.html.GlassSettingsDialog.show); 
    $(document).on('ShowDialogOutputGraphics', LMT.ui.html.ColorSettingsOutputDialog.show);
    $(document).on('RedrawCurrentOutput', LMT.ui.out.updateImg);


    $(document).on('SwitchMode', LMT.ui.svg.SwitchMode);
    $(document).on('ModeSwitched', LMT.ui.html.Toolbar.update);

//    $(document).on('ShowDialogSaveResult', LMT.ui.html.SaveResultDialog.show);
//    $(document).on('InputImageGenerated', LMT.ui.html.SaveResultDialog.generatedImage);
//    $(document).on('SaveModel', LMT.com.SaveModel);  // upload model with is final tag
//    $(document).on('SavedModel', LMT.ui.html.SaveResultDialog.savedModel);  // if successful saved
    
    $(document).on('WaitForSimulation', LMT.ui.html.WaitForResultDialog.show);
    $(document).on('WaitForSimulation', LMT.ui.html.WaitForResultDialog.startRefresh);
    
    $(document).one('UpdateRepaintModel', LMT.events.UpdateRepaintModel); //can only be called once, once finished with the update, it reassigns itself
    $(document).on('RepaintModel', LMT.objects.Model.Repaint);

    $(document).on('GetSimulation', LMT.com.GetSimulation);

    $(document).on('GetSimulationFail', LMT.ui.html.WaitForResultDialog.stopRefresh);

//    $(document).on('DisplayOutputSlideNext', LMT.ui.out.next);
//    $(document).on('DisplayOutputSlidePrev', LMT.ui.out.prev);
//    $(document).on('DisplayOutputSlideOverview', LMT.ui.out.showOverview); //not yet implemented

    
    $(document).on('CreateRootMinima', LMT.objects.Model.CreateRootMinima);
    // expans or collapses an extremalpoint
    $(document).on('ToggleExtremalPoint', LMT.objects.ExtremalPoint.ToggleExtremalPoint);
    $(document).on('CreateContourPoint', LMT.objects.ContourPoint.Doublicate);
    $(document).on('DeleteContourPoint', fnc);
    $(document).on('MoveObject', LMT.events.MoveObject);
    $(document).on('MoveCrosshair', LMT.ui.svg.moveCrosshair);
    $(document).on('CreateExternalMass', LMT.objects.Model.CreateExternalMass);
    $(document).on('CreateRuler', LMT.objects.Model.CreateRuler);
    $(document).on('DeleteObject', LMT.objects.Model.RemoveObject); // expects supplied jsObj to be removed

    /*
    $(document).on('ShowTooltip', html.Tooltip.show);
    $(document).on('HideTooltip', html.Tooltip.hide);
    */
//    $(document).on('HideAllTooltips', html.Tooltip2.closeAll); // should be called whenever a button gets deactivated due to a bug in jquery ui tooltip
    
//    $(document).on('ConvertInputImageToPNG', LMT.ui.svg.ConvertToPNG);
    //$(document).on('UploadInputImage', LMT.ui.com.UploadInputImage);
};




/** V2 NEW
 * This should be called by each independant sub component involved in loading something
 * Here is checked, if all sub components are already ready
 * It they are, the final AppReady is called
 *
 * It's only a stub at the moment..
 */
events.AppReadyHandler = function () {
    //TODO maybe some check if everything is really ready
    $.event.trigger("AppReady");
};



/** V2 NEW
 * This files, as soon as the the app is ready to be used by the user
 */
events.ready = function () {
    log("events.ready == (Appready as been fired)");
    
    //push initial state to actionstack
    $.event.trigger("SaveModelState");
    
    // only activate keyboard shotcut input, when the app is really ready
    // otherwise messes shortcuts on dialogs up
    LMT.ui.html.KeyboardListener.init();
};






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
};




/**
 * moves any jsObj on the svg canvas.
 * DON'T trigger a action stack push here
 * this will be called many^100 times 
 */
events.MoveObject = function(evt, jsTarget, svgTarget, coord){
  jsTarget.move(coord, svgTarget);
  $(document).one('UpdateRepaintModel', LMT.events.UpdateRepaintModel);
};


/** V2 NEW
 * What happens when simulatemodel is clicked
 */
events.SimulateModel = function(){
    $.event.trigger("UploadModel");
    
//  $(document).one('UploadModelComplete', function(){$.event.trigger("GetSimulation");}); 
    //some old relict
};

/** V2 NEW
 * Immideatly start polling for result once a model is uploaded
 */
events.onUploadComplete = function(){
  $.event.trigger("StartRendering");
};


LMT.events = events;
