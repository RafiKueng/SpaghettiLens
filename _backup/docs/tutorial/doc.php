<?php
  function getDayOfWeek() {
    return date('l');
  }
?>

<!DOCTYPE html>
<html>
  <head>
    <title>Title of the document</title>
  </head>
  <body>
    <?php
      echo '<p>Today is: ' . getDayOfWeek() . "</p>\n";
    ?>
  </body>
</html>