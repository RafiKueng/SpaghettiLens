<!-- START body.php -->

<body>
  
<div id="outer_table" class="layout table strech rounded_top rounded_bottom">

  <div class="layout row">
    <div id="head" class="layout table rounded_top">
      <div id="headtitle" class="layout cell">
        <h1>Lens Modelling Tool</h1>
      </div>
      <div id="toolbarTop" class="layout cell centered">
        <span id="toolbarGrpTop" class="toolbar ui-widget-header ui-corner-all">
          <span id="btngrpMainNav" class="btnset">
            <button id="btnMainActionPrev"
              data-event="PrevModel"
              data-tooltip="goto previous model"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-chevron-left">
              Goto Previous Model
            </button>
            <button id="btnMainFinish"
              data-event="SaveModel"
              data-tooltip="Save the final model on the server"
              data-furtherinfo="http://www.google.com"
              data-hotkey="s"
              data-icon="icon-ok">
              Save the final model on the server
            </button>
            <button id="btnMainActionNext"
              data-event="NextModel"
              data-tooltip="goto next model"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-chevron-right">
              Goto Next Model
            </button>
          </span>
          
          <button id="btnMainLogin"
            data-event="LoginClicked"
            data-tooltip="log in / create user account"
            data-furtherinfo="http://www.google.com"
            data-hotkey="Ctrl+Z; Q"
            data-icon="icon-signin">
            Log in / Create user account
          </button>

          <input id="btnMainHelp" type="checkbox"
            data-event="ToggleHelpBar"
            data-tooltip="Displays the mouseover help"
            data-furtherinfo="http://www.google.com"
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
              data-tooltip="reverts the last action"
              data-furtherinfo="http://www.google.com"
              data-hotkey="Ctrl+Z; Q"
              data-icon="icon-undo">
              Undo
            </button>
            <button id="btnInRedo"
              data-event="Redo"
              data-tooltip="reapplies the last undone action"
              data-furtherinfo="http://www.google.com"
              data-hotkey="Ctrl+Y; W"
              data-icon="icon-repeat">
              Redo
            </button>
          </span>
          
          <span id="btngrpSettings" class="btnset">
            <button id="btnInSettingsColor"
              data-event="ShowDialogColorSettings"
              data-tooltip="Change the brightness / contrast and colormapping of the background image"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-adjust">
              background image settings
            </button>
            <button id="btnInSettingsLines"
              data-event="ShowDialogDisplaySettings"
              data-tooltip="Change the appeareance of the model"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-eye-open">
              display settings
            </button>
          </span>
          
          <span id="btngrpMode" class="btnset">
            <input type="radio" id="btnInModeMass" name="mode"
              data-event="SwitchMode" data-value="mass"
              data-tooltip="places additional point masses"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-star" />
            <label for="btnInModeMass">Place Point Masses</label>

            <input type="radio" id="btnInModeImage" name="mode"
              data-event="SwitchMode" data-value="image"
              data-tooltip="mark images as min / max / sad"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-screenshot"
              checked="checked"/>
            <label for="btnInModeImage">Mark Images</label>

            <input type="radio" id="btnInModeRuler" name="mode"
              data-event="SwitchMode" data-value="ruler"
              data-tooltip="places a helping ruler to estimate distances"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-resize-horizontal" />
            <label for="btnInModeRuler">Add Ruler to esimate Distances</label>
          </span>
          
          <span id="btngrpActions" class="btnset">
            <!--
            <button id="btnInActionSave"
              data-event="SaveModel"
              data-tooltip="Save the Model"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-save">
              Save the model locally
            </button>
            -->
            <!--
            <button id="btnInActionUpload"
              data-event="UploadModel"
              data-tooltip="Save the final model on the server"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
              data-icon="icon-cloud-upload">
              Save the final model on the server
            </button>
            -->
            <button id="btnInActionSimulateModel"
              data-event="SimulateModel"
              data-tooltip="update the simulated results"
              data-furtherinfo="http://www.google.com"
              data-hotkey="C"
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
              data-tooltip="display the graphicssettings for the output"
              data-furtherinfo="http://www.google.com"
              data-hotkey="t"
              data-icon="icon-adjust">
              Change brightness and contrast of output images
            </button>
            <button id="btnOutGlassConfig"
              data-event=""
              data-tooltip="Configure simulation properties"
              data-furtherinfo="http://www.google.com"
              data-hotkey="g"
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
    foot
  </div>
</div>


<div id="log" onclick="togglelog();">
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
    <input type="checkbox" id="conn_l" />
    <label for="conn_l">ConnectingLines</label>
    <input type="checkbox" id="cont_p" />
    <label for="cont_p">ContourPoints</label>
    <input type="checkbox" id="cont_l" />
    <label for="cont_l">ContourLine</label>
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
  <p>Plese enter your name:<br/>
    <label for="username">Name:</label>
    <input type="text" name="username" id="username" class="text ui-widget-content ui-corner-all" />
  </p>
  <p>Select Datasource:<br/>
    <select id="sel_datasource" data-placeholder="Choose a datasource" style="width:500px;" class="chzn-select-deselect" tabindex="7">
      <option value=""></option>
    </select>
  </p>
</div>


<div id="generic_datasource_dialog" class="dialog" title="INSERT TITLE">
</div>


</body>

<!-- END body.php -->