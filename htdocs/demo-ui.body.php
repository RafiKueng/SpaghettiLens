
<!-- /// demo-ui.body.php start -->
<body onload="onBodyInit();">
<!--<h1>Demo User interface</h1>-->





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






<div id="ui_area">

<!-- / include svg, cut first line-->
<?php
echo file_get_contents('demo-ui.svg', NULL, NULL, 55); //skip the first line with xml def
?>
<!-- \ end in svg, cut first line-->

<!-- / include canvas -->
<canvas id="ui_bg_canvas2" width="600" height="600">
  your browser doesn't support canvases
</canvas>
<!-- \ end include canvas -->

<canvas id="ui_img_canvas" width="600" height="600">
  your browser doesn't support canvases
</canvas>


</div>
<div id="console">
<p>:: debug.log ::</p>
<p id="debug.log2">test</p>
</div>

<img id="glassimg2" src="" alt="glassimg" height="300" width="300"> 








</body>

<!-- \\\ demo-ui.body.php end -->
