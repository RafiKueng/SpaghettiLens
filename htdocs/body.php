<!-- START body.php -->

<body  onload="onBodyInit();"> 

<div id="doc">
  
  <header
    id="top">
    top
  </header>
  
  <div id="cont">
    <div id="main">
      <div id="toolbar1" class="toolbar"
        onmousemove='hoverBtns(event);'
        onmouseover="document.getElementById('popup').style.display = 'block';"
        onmouseout="document.getElementById('popup').style.display = 'none';">
        
        <div id="btngrpSettings" class="toolbar_element" data-type="expand" data-order="2">
	        <img id="settings_master" class="svg button" src="svg/settings._grp.svg"
	        	data-tooltip="open the settings panel"
	        	data-furtherinfo="http://www.google.com"
	        	/>
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
	        	data-value="mass"
	        	data-tooltip="places additional point masses"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="mode_image" class="svg button" src="svg/mode.image.svg"
	        	data-value="image"
	        	data-tooltip="places additional images"
	        	data-furtherinfo="http://www.google.com"
	        	/>
	        <img id="mode_ruler" class="svg button" src="svg/mode.ruler.svg"
	        	data-value="ruler"
	        	data-tooltip="places a helping ruler to estimate distances"
	        	data-furtherinfo="http://www.google.com"
	        	/>
        </div>
	  </div>

      <div id="toolbar2" class="toolbar"
        onmousemove='log.write("hover btn2");'
        onmouseover="document.getElementById('popup').style.display = 'block';"
        onmouseout="document.getElementById('popup').style.display = 'none';">
        btn2
      </div>

      <div id="inp"></div>
      
      <div
        id="out">
        out
      </div>
      
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

  <div
    id="popup">
    popup
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