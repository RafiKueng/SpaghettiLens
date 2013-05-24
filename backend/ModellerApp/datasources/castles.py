
def getName():
  return "Castles Image Catalog"
  

  
def getDialogHTML():
  return """
<script>
(function(){
/* assign event handlers for dialog */
  $(document).on('datasrcSelect', function(evt){
    alert("hi")
  })
})()
</script>

<!-- enter dialog html code here -->
<p>Select Castles images</p>


"""


