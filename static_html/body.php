<!-- START body.php -->

<body>
  
<div id="outer_table" class="layout table strech rounded_top rounded_bottom">

  <div class="layout row">
    <div id="head" class="layout table rounded_top">
      <div id="headtitle" class="layout cell">
        <h1>SpaghettiLens</h1>
      </div>
      <div id="toolbarTop" class="layout cell centered">
        <span id="toolbarGrpTop" class="toolbar ui-widget-header ui-corner-all">
          <span id="btngrpMainNav" class="btnset">
            <button id="btnMainActionPrev"
              data-event="PrevModel"
              data-ttip-title="Previous"
              data-ttip-text="goto previous model"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-chevron-left">
              Goto Previous Model
            </button>
            <button id="btnMainFinish"
              data-event="ShowDialogSaveResult"
              data-ttip-title="Save Model"
              data-ttip-text="Save this model and your input on the server"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-ok">
              Save the final model on the server
            </button>
            <button id="btnMainActionNext"
              data-event="NextModel"
              data-ttip-title="Next"
              data-ttip-text="load the next model in the list"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-chevron-right">
              Goto Next Model
            </button>
          </span>
          
          <button id="btnMainLogin"
            data-event="LoginClicked"
            data-ttip-title="Log In"
            data-ttip-text="log in / create user account"
            data-ttip-link=""
            data-hotkey=""
            data-icon="icon-signin">
            Log in / Create user account
          </button>

          <input id="btnMainHelp" type="checkbox"
            data-event="ToggleHelpBar"
            data-ttip-title="Context Help"
            data-ttip-text="Displays the mouseover help"
            data-ttip-link=""
            data-hotkey="H, F1"
            data-icon="icon-question-sign" />
          <label for="btnMainHelp">Toggle Mouseover Help</label>
                    
        </span>
      </div>
    </div>
  </div>  



  <div class="layout row">
    <div id="toolbars" class="layout fillbox">
      
      
      
      <div id="toolbarInp" class="layout block centered">
        <span id="toolbarGrp1" class="toolbar ui-widget-header ui-corner-all">
          <span id="btnsetXxdo" class="btnset">
            <button id="btnInUndo"
              data-event="Undo"
              data-ttip-title="Undo"
              data-ttip-text="reverts the last action"
              data-ttip-link=""
              data-hotkey="Ctrl+Z; Q"
              data-icon="icon-undo">
              Undo
            </button>
            <button id="btnInRedo"
              data-event="Redo"
              data-ttip-title="Redo"
              data-ttip-text="reapplies the last undone action"
              data-ttip-link="http://www.google.com"
              data-hotkey="Ctrl+Y; W"
              data-icon="icon-repeat">
              Redo
            </button>
          </span>
          
          <span id="btngrpSettings" class="btnset">
            <button id="btnInSettingsColor"
              data-event="ShowDialogColorSettings"
              data-ttip.title="Color Settings"
              data-ttip-text="Change the brightness / contrast and colormapping of the background image"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-adjust">
              background image settings
            </button>
            <button id="btnInSettingsLines"
              data-event="ShowDialogDisplaySettings"
              data-ttip-title="Model Display Settings"
              data-ttip-text="Change the appeareance of the model, hide contour lines, contour points, ..."
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-eye-open">
              input panel display settings
            </button>
          </span>
          
          <span id="btngrpMode" class="btnset">
            <input type="radio" id="btnInModeMass" name="mode"
              data-event="SwitchMode" data-value="mass"
              data-ttip-title="Add Point Mass"
              data-ttip-text="Place additional point masses"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-star" />
            <label for="btnInModeMass">add external point masses</label>

            <input type="radio" id="btnInModeImage" name="mode"
              data-event="SwitchMode" data-value="image"
              data-ttip-title="Image Tool"
              data-ttip-text="Mark / identify lensed images"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-screenshot"
              checked="checked"/>
            <label for="btnInModeImage">identify images</label>

            <input type="radio" id="btnInModeRuler" name="mode"
              data-event="SwitchMode" data-value="ruler"
              data-ttip-title="Ruler Tool"
              data-ttip-text="Click and drag to use a ruler to estimate distances"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-resize-horizontal" />
            <label for="btnInModeRuler">use to estimate distances</label>
          </span>
          
          <span id="btngrpActions" class="btnset">
            <!--
            <button id="btnInActionSave"
              data-event="SaveModel"
              data-ttip-text="Save the Model"
              data-ttip-link="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-save">
              Save the model locally
            </button>
            -->
            <!--
            <button id="btnInActionUpload"
              data-event="UploadModel"
              data-ttip-text="Save the final model on the server"
              data-ttip-link="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-cloud-upload">
              Save the final model on the server
            </button>
            -->
            <button id="btnInActionSimulateModel"
              data-event="SimulateModel"
              data-ttip-title="Model"
              data-ttip-text="Send your input to be modelled"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-cogs">
              Simulate the Model and Refresh the Output Images
            </button>
          </span>
        </span>
      </div>
      
      
      
      <div id="toolbarOut" class="layout block centered">
        <span id="toolbarGrp2" class="toolbar ui-widget-header ui-corner-all">
          <span id="btnsetOutNrNav"></span>
          <span id="btnsetOutConfig">
            <button id="btnOutGraphics"
              data-event="ShowDialogOutputGraphics"
              data-ttip-title="Adjust Output"
              data-ttip-text="Adjust brightness and contrast of the rendered output images"
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-adjust">
              Change brightness and contrast of output images
            </button>
            <button id="btnOutGlassConfig"
              data-event=""
              data-ttip-title="Simulation Properties"
              data-ttip-text="Set up modelling properties such as resolution, redshifts, ..."
              data-ttip-link=""
              data-hotkey=""
              data-icon="icon-tasks">
              Configure simulation properties
            </button>
          </span>
        </span>
      </div>




    </div>
  </div>






  <div class="layout row strech">
    <div id="main" class="layout fillbox">
      
      <div id="inp" class="layout block">
      </div>

      <div id="bigslider" class="layout block right" onclick="$.event.trigger('ToggleDisplay');">
        <div style="position:absolute; top: 50%; left: 50%; margin-top: -0.75em; margin-left: -0.125em;">
          <i class="icon-double-angle-left"></i>
        </div>
      </div>
        
      <div id="out" class="layout block">
      </div>

    </div>
  </div>



  <div id="help" class="layout row">
    <div id='helpcont' class='help container'></div>
  </div>

  <div id="footer" class="layout row">
    <p class="foottext">
      by Rafael Kueng; uses glass (Jonathan Coles), jquery ui, chosen, datatables, colorpicker, django, celery, gunicorn, mysql. Visit https://github.com/RafiKueng/SpaghettiLens
    </p>
  </div>
</div>


<div id="log" style="display: none;">
  <p id="logtitle">
    DEBUG INFORMATION / LOG:
  </p>
  <p id="logcont">
    blabla
    <br />
    blabla
    <br />
    blabla
    <br />
    blabla
    <br />
    blabla
  </p>
</div>




<div id="popup" class="initHidden">
  <span id="text"></span>
  <br/>
  <span id="link"></span>
  <br/>
  <span id="hotkey"></span>
</div>

<div id="color_dialog" class="dialog initHidden" title="Brightness / Contrast / Color Settings">
  
  <div id="cd_table">
    <div class="cd_row">
      <div class='cd_cell cd_cell_name '>
        <p>Ch1</p>
      </div>
      
      <div class="cd_cell cd_cell_sliders">
        <div class="cd_i_table">
        
          <div style="display: table-row;">
            <div class="cd_cell cd_cell_icon">
              <i class="icon-adjust"></i>
            </div>
            <div class="cd_cell cd_cell_slider">
              <div id="csettings_ch0_contrast" data-id="0" data-type="contrast" class="slider contrast"></div>
            </div>
            <div class="cd_cell cd_cell_value">
              <p>0.00</p>
            </div>
          </div>
          
          <div style="display: table-row;">
            <div class="cd_cell cd_cell_icon">
              <i class="icon-lightbulb"></i>
            </div>
            <div class="cd_cell cd_cell_slider">
              <div id="csettings_ch0_brightness" data-id="0" data-type="brightness" class="slider brightness"></div>
            </div>
            <div class="cd_cell cd_cell_value">
              <p>0.00</p>
            </div>
          </div>
        </div>
      </div>
      
      <div class="cd_cell cd_cell_cp">
        <input id="csettings_ch0_color" data-id="0" value="ff0000" class="mycp"></input>
      </div>
      
    </div>
  </div>
  
  
<div id="color_out_dialog" class="dialog initHidden" title="Brightness / Contrast / Color Settings of Output">
  
  <div id="cod_table">
    <div class="cd_row">
      
      <div class="cd_cell cd_cell_sliders">
        <div class="cd_i_table">
        
          <div style="display: table-row;">
            <div class="cd_cell cd_cell_icon">
              <i class="icon-adjust"></i>
            </div>
            <div class="cd_cell cd_cell_slider">
              <div id="cod_co" data-id="0" data-type="contrast" class="slider contrast"></div>
            </div>
            <div class="cd_cell cd_cell_value">
              <p>0.00</p>
            </div>
          </div>
          
          <div style="display: table-row;">
            <div class="cd_cell cd_cell_icon">
              <i class="icon-lightbulb"></i>
            </div>
            <div class="cd_cell cd_cell_slider">
              <div id="cod_br" data-id="0" data-type="brightness" class="slider brightness"></div>
            </div>
            <div class="cd_cell cd_cell_value">
              <p>0.00</p>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>    
  
  
  
  <!--
  <div id="csettings_ch0" class="settings_channelcontainer">
    <div style="
    float: left;
    width: 300px;
    height: 100%;">
      <div id="csettings_ch0_contrast" data-id="0" data-type="contrast" class="slider contrast"></div>
      <div id="csettings_ch0_brightness" data-id="0" data-type="brightness" class="slider brightness"></div>
    </div>
    <div style="
    width: 100px;
    height: 100%;
    overflow: hidden;">
      <input id="csettings_ch0_color" data-id="0" class="mycp" value="ff0000">
      </input>
    </div>
  </div>
  -->
</div>

<div id="display_dialog" class="dialog initHidden" title="Display Settings">
  <div id="dsettings">
    <input type="checkbox" id="ds_all" />
    <label for="ds_all">Toggle Model (all)</label>
    <input type="checkbox" id="conn_l" />
    <label for="conn_l">Toggle Connecting Lines</label>
    <input type="checkbox" id="cont_p" />
    <label for="cont_p">Toggle Contour Points</label>
    <input type="checkbox" id="cont_l" />
    <label for="cont_l">Toggle Contour Lines</label>
  </div>
</div>


<div id="glass_dialog" class="dialog" title="Glass Configuration">
  <div>
    <p style="display: inline">Redshifts: </p><p id='gset_redshift_out' style="display: inline"></p>
    <div style="display: block; width: 300px" id="gset_redshift_slide" class="slider"></div>
  </div>
  <div>
    <p style="display: inline">PixelRadius: </p><p id='gset_pixrad_out' style="display: inline"></p>
    <div style="display: block; width: 300px" id="gset_pixrad_slide" class="slider"></div>
  </div>
  <div>
    <p style="display: inline">nModels: </p><p id='gset_nmodels_out' style="display: inline"></p>
    <div style="display: block; width: 300px" id="gset_nmodels_slide" class="slider"></div>
  </div>
  <div>
    <p style="display: inline">is the model symmetrical? </p>
    <input type="checkbox" id="gset_issymm" /><label for="gset_issymm">true</label>
  </div>
</div>

<div id="select_model_dialog" class="dialog" title="Select Lenses to Work on..">
  <p>Select a catalog to filter lenses list:</p>
  <select id="selmod_cat" data-placeholder="Choose a Catalogue" style="width:500px;" class="chzn-select-deselect" tabindex="7">
    <option value=""></option>
  </select>
  <p>Select particular Lenses:<br>(none selected: all; type to search)</p>
  <!--
  <select id="selmod_lensid" data-placeholder="ID" multiple style="width:70px;" class="chzn-select-deselect" tabindex="7">
    <option value=""></option>
  </select>
  -->
  <select id="selmod_lens" data-placeholder="Name (Catalogue)" multiple style="width:500px;" class="chzn-select-deselect" tabindex="7">
    <option value=""></option>
  </select>
</div>





<div id="select_datasource_dialog" class="dialog" title="Select Datasource">
  <p>Please enter your name:<br/>
    <label for="username">Name:</label>
    <input type="text" name="username" id="username" class="text ui-widget-content ui-corner-all" />
  </p>
  <p>Select Datasource:<br/>
    <select id="sel_datasource" data-placeholder="Choose a datasource" style="width:500px;" class="chzn-select-deselect" tabindex="7">
      <!--<option value=""></option>-->
    </select>
  </p>
</div>


<div id="generic_datasource_dialog" class="dialog" title="INSERT TITLE">
</div>


<div id="save_results_dialog" class="dialog" title="Save your Model">
</div>

<div id="wait_for_results_dialog" class="dialog" title="Currently Crunching Numbers">
  <p>Running since: <span id="wfrd_running">0</span>s</p>
  <p>Estimated duration: (very roughly) <span id="wfrd_est">0</span>s</p>
</div>

<div id="load_progress_dialog" class="dialog" title="Loading images">
  <p>    
  </p>
</div>

<div id="new_version" class="dialog" title="new version available">
  <p>There is a new version available<br/>
    Please press Ctrl + F5 to force a reload
  </p>
</div>


<div id="get_username" class="dialog" title="Username">
  <p>Please enter your name:<br/>
    <label for="username2"></label>
    <input type="text" name="username2" id="username2" class="text ui-widget-content ui-corner-all" />
  </p>
</div>



<script type="text/javascript">
  if (typeof(LMT) === 'undefined') {
    $('#new_version').dialog({
      autoOpen: true,
      minWidth: 600,
      minHeight: 400,
      modal: false
    })
  }
  else {
    $('.foottext').prepend(LMT.version + '; ');
  }
</script>

</body>

<!-- END body.php -->