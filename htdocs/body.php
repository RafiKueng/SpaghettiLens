<!-- START body.php -->

<body  onload="onBodyInit();"> 

<div id="doc">
  
  <header
    id="top">
    top
  </header>
  
  <div id="cont">
    <div id="main">
      <div id="btn"
        onmousemove='hoverBtns(event);'
        onmouseover="document.getElementById('popup').style.display = 'block';"
        onmouseout="document.getElementById('popup').style.display = 'none';">
        btn
      </div>

      <div id="btn2"
        onmousemove='log.write("hover btn2");'
        onmouseover="document.getElementById('popup').style.display = 'block';"
        onmouseout="document.getElementById('popup').style.display = 'none';">
        btn2
      </div>

      <div
        id="inp">
        inp<br/>
        line2
      </div>
      
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