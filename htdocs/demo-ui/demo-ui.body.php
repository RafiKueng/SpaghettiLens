
<!-- /// demo-ui.body.php start -->
<body>
<h1>Demo User interface</h1>
<h2>the user interface</h2>

<div id="ui.area">

<!-- / include svg, cut first line-->
<?php
echo file_get_contents('demo-ui.svg', NULL, NULL, 55); //skip the first line with xml def
?>
<!-- \ end in svg, cut first line-->

<!-- / include canvas -->
<canvas id="ui.canvas_layer" width="750" height="400">
  your browser doesn't support canvases
</canvas>
<!-- \ end include canvas -->

</div>
</body>

<!-- \\\ demo-ui.body.php end -->
