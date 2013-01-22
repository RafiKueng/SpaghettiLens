<!-- START body.php -->

<body  onload="onBodyInit();"> 

<div id="doc">
  
  <header
    id="top">
  </header>

  <div id="cont">
    <div id="main">
      <div id="toolbar1" class="toolbar">
		<!--
		onmouseover="document.getElementById('popup').style.display = 'block';"
        onmouseout="document.getElementById('popup').style.display = 'none';"
       -->
        
        <div id="btngrpXXDO" class="toolbar_element" data-type="fix" data-order="0">
	        <img id="undo" class="svg button" src="svg/undo.svg"
				data-event="Undo"
	        	data-tooltip="reverts the last action"
	        	data-furtherinfo="http://www.google.com"
	        	data-hotkey="Ctrl+Z; Q"
	        	/>
	        <img id="redo" class="svg button" src="svg/redo.svg"
	        	data-event="Redo"
	        	data-tooltip="reapplies the last undone action"
	        	data-furtherinfo="http://www.google.com"
	        	/>
        </div>
        
        <div id="btngrpSettings" class="toolbar_element" data-type="expand" data-order="2">
	        <!--
	        <img id="settings_master" class="svg button" src="svg/settings.svg"
	        	data-tooltip="open the settings panel"
	        	data-furtherinfo="http://www.google.com"
	        	/>
        	-->
	        <img id="settings_color" class="svg button" src="svg/settings.color.svg"
	        	data-event="ShowColorSettings"
	        	data-tooltip="change the color mapping"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="settings_lines" class="svg button" src="svg/settings.lines.svg"
	        	data-event="ShowDisplaySettings"
	        	data-tooltip="enables / disables some heling lines"
	        	data-furtherinfo="http://www.google.com"
	        	/>
        </div>
        
        <div id="btngrpMode" class="toolbar_element" data-type="toggle" data-event="SwitchMode" data-order="1">
	        <img id="mode_mass" class="svg button" src="svg/mode.mass.svg"
	        	data-event="SwitchMode" data-value="mass"
	        	data-tooltip="places additional point masses"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="mode_image" class="svg button" src="svg/mode.image.svg"
	        	data-event="SwitchMode" data-value="image"
	        	data-tooltip="places additional images"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="mode_ruler" class="svg button" src="svg/mode.ruler.svg"
	        	data-event="SwitchMode" data-value="ruler"
	        	data-tooltip="places a helping ruler to estimate distances"
	        	data-furtherinfo="http://www.google.com"
	        	/>
        </div>

        <div id="btngrpAction" class="toolbar_element" data-type="fix" data-order="0">
	        <img id="action_prev" class="svg button" src="svg/prev.svg"
				data-event="GotoPrevModel"
	        	data-tooltip="goto the next model"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="action_save" class="svg button" src="svg/save.svg"
	        	data-event="SaveModel"
	        	data-tooltip="save the current model locally and on server"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="action_model" class="svg button" src="svg/calculate.svg"
	        	data-event="CalculateModel"
	        	data-tooltip="Simulates the model"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="action_next" class="svg button" src="svg/next.svg"
	        	data-event="GotoNextModel"
	        	data-tooltip="goto the previous model"
	        	data-furtherinfo="http://www.google.com"
	        	/>
        </div>

	  </div>

      <div id="toolbar2" class="toolbar">
      	<button id="btnOutPrev">Previous</button>
      	<span class="slide_btn" onclick="LMT.out.prev();">prev</span>
      	<span id="nrbtn"></span>
      	<span class="slide_btn" onclick="LMT.out.next();">next</span>
      </div>

      <div id="inp"></div>
      
      <div id="out"></div>
      
      <div
        id="slider"
        onclick="sliderclick();">
        &lt;&lt;&gt;&gt;
      </div>
    </div>
  </div>


  <footer
    id="footer">
    footer
  </footer>
  
  <div
    id="log"
    onclick="togglelog();">
    <p id="logtitle">DEBUG INFORMATION / LOG:</p>
    <p id="logcont">blabla<br />blabla<br />blabla<br />blabla<br />blabla</p>
  </div>
</div>

<div id="popup">
	<span id="text"></span> <br/>
	<span id="link"></span> <br/>
	<span id="hotkey"></span>
</div>


<div id="color_dialog" class="dialog" title="ColorPicker">
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
			<input id="csettings_ch0_color" data-id="0" class="mycp" value="ff0000"></input>
		</div>
	</div>
</div>

<div id="display_dialog" class="dialog" title="Display Settings">
	<div id="dsettings">
		<input type="checkbox" id="conn_l" /><label for="conn_l">ConnectingLines</label>
		<input type="checkbox" id="cont_p" /><label for="cont_p">ContourPoints</label>
		<input type="checkbox" id="cont_l" /><label for="cont_l">ContourLine</label>
	</div>
</div>



<!-- before renaming // old version
<div id="container1">
  <div id="container2">
    <div id="output">
    	
    	<img id="glassimg" src="" alt="glassimg" height="300" width="300"> 
    	
    </div>
    <div id="inp1">
    	
		    	
		<canvas id="ui_bg_canvas" width="600" height="600">
		  your browser doesn't support canvases
		</canvas>
		    	
    </div>
    <div id="log"><div id="console">

		<p>:: debug.log ::</p>
		<p id="debug.log">test</p>

	</div></div>
    <div id="inp2">

	  <?php
        echo file_get_contents('demo-ui.svg', NULL, NULL, 55); //skip the first line with xml def
      ?>
    	


	</div>
  </div>
</div>


-->


</body>

<!-- END body.php -->