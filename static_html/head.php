<?php
header( "Expires: Mon, 20 Dec 1998 01:00:00 GMT" );
header( "Last-Modified: " . gmdate("D, d M Y H:i:s") . " GMT" );
header( "Cache-Control: no-cache, must-revalidate" );
header( "Pragma: no-cache" );
?>

<!-- START head.php -->

<head>
  <meta charset="UTF-8">

  <link href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/themes/ui-darkness/jquery-ui.css" rel="stylesheet">

  <link href="css/jquery.colorpicker.css" rel="stylesheet" type="text/css"/>
  <link href="css/jquery.chosen.css" rel="stylesheet" />
  <link href="css/font-awesome.css" rel="stylesheet" type="text/css"/>

  <link rel="stylesheet" href="css/main.css" type="text/css" />
  <link rel="stylesheet" href="css/svg_elements.css" type="text/css" />
  <link rel="stylesheet" href="css/big_screen.css" type="text/css" />
  <link rel="stylesheet" href="css/small_screen.css" type="text/css" />



  <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.js"></script>
  <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.9.2/jquery-ui.js"></script>
  
  
  <script type="text/javascript" src="http://canvg.googlecode.com/svn/trunk/rgbcolor.js"></script> 
  <script type="text/javascript" src="http://canvg.googlecode.com/svn/trunk/StackBlur.js"></script>
  <script type="text/javascript" src="http://canvg.googlecode.com/svn/trunk/canvg.js"></script>   

  
  <script type="text/javascript" src="js/lmt.js"></script>
<?php
  // include all script files in the folder /js
  $handle=opendir("js/");

  while (($file = readdir($handle))!==false) {
    if ($file[0] != '.' && $file != 'lmt.js') {
      echo '  <script type="text/javascript" src="js/' . $file . '"></script>' . "\n";
    }
  }

  closedir($handle);
?>
  <script type="text/javascript" src="js/lmt.settings.js"></script>


  <link rel="icon" href="/favicon.ico" type="image/x-icon">
  
<!--
  <link rel="stylesheet" href="demo-ui.css" type="text/css" />

  <script type="text/javascript" src="Color.js"></script>
  <script type="text/javascript" src="object.ui.BandColorSelector.js"></script>

  
  <script type="text/javascript" src="demo-ui.gen.js"></script>
  <script type="text/javascript" src="demo-ui.objects.js"></script>
  <script type="text/javascript" src="demo-ui.obj.contour.js"></script>
  <script type="text/javascript" src="demo-ui.obj.contourPoint.js"></script>
  <script type="text/javascript" src="demo-ui.obj.model.js"></script>
  <script type="text/javascript" src="demo-ui.obj.actionstack.js"></script>
  <script type="text/javascript" src="object.ruler.js"></script>
  <script type="text/javascript" src="object.external_mass.js"></script>

  <script type="text/javascript" src="demo-ui.intel.js"></script>
  <script type="text/javascript" src="demo-ui.com.js"></script>
  <script type="text/javascript" src="demo-ui.ui-svg.js"></script>
  <script type="text/javascript" src="demo-ui.widget.js"></script>
  <script type="text/javascript" src="demo-ui.ui-canv.js"></script>
 
  <script type="text/javascript" src="demo-ui.ui-actionmenu.js"></script>
  <script type="text/javascript" src="demo-ui.ui-modemenu.js"></script>
  <script type="text/javascript" src="demo-ui.ui-settingstab.js"></script>
  <script type="text/javascript" src="demo-ui.ui-xxdo.js"></script>
  <script type="text/javascript" src="ui.popup.displaySettings.js"></script>
  <script type="text/javascript" src="ui.popup.graphicSettings.js"></script>
-->

  <title>LensModellingTool</title>
</head>

<!-- END head.php -->
