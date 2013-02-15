<!-- START body.php -->

<body>

  <div id="doc">

    <div id="top">
      <div style="display:table-cell; height: 100%">
        <h1>Lens Modelling Tool</h1>
      </div>
      <div id="toolbarTop" style="display:table-cell; width: auto; text-align: right;vertical-align: bottom; padding: 10px; ">
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
              data-event="UploadModel"
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
            data-tooltip="loggs in"
            data-furtherinfo="http://www.google.com"
            data-hotkey="Ctrl+Z; Q"
            data-icon="icon-signin">
            Log In
          </button>

          <input id="btnMainHelp" type="checkbox"
            data-event="ToggleHelp"
            data-tooltip="Displays the mouseover help"
            data-furtherinfo="http://www.google.com"
            data-hotkey="H, F1"
            data-icon="icon-question-sign" />
          <label for="btnMainHelp">Toggle Mouseover Help</label>
                    
        </span>
      </div>
    </div>

    <div id="cont">
      <div id="main">
        <div id="toolbar1" class="toolbarContainer">
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
                data-tooltip="change the color mapping"
                data-furtherinfo="http://www.google.com"
                data-hotkey="C"
                data-icon="icon-adjust">
                Show Color Settings
              </button>
              <button id="btnInSettingsLines"
                data-event="ShowDialogDisplaySettings"
                data-tooltip="enables / disables some heling lines"
                data-furtherinfo="http://www.google.com"
                data-hotkey="C"
                data-icon="icon-eye-open">
                Show Display Settings
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
                data-tooltip="places additional images"
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


        <div id="toolbar2" class="toolbarContainer">
          <span id="toolbarGrp2" class="toolbar ui-widget-header ui-corner-all">
            <!--
            <span id="btnsetOutNav">
              <button id="btnOutPrev">
                Previous
              </button>
              <button id="btnOutNext">
                Next
              </button>
            </span>
            <button id="btnOutOverview">
              Overview
            </button>
            -->
            <span id="btnsetOutNrNav"></span>
            <span id="btnsetOutConfig">
              <button id="btnOutGlassConfig">
                Configure Glass (backend simulation program)
              </button>
            </span>
          </span>
        </div>



        <div id="inp"></div>



        <div id="out"></div>


        <div id="slider" onclick="sliderclick();">
          &lt;&lt;&gt;&gt;
        </div>

      </div>
    </div>

    <footer id="footer">
      footer
    </footer>

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
    
    
  </div>

  <div id="popup" class="initHidden">
    <span id="text"></span>
    <br/>
    <span id="link"></span>
    <br/>
    <span id="hotkey"></span>
  </div>

  <div id="color_dialog" class="dialog initHidden" title="ColorPicker">
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

</body>

<!-- END body.php -->