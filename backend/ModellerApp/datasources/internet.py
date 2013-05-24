
def getName():
  return "Some internetfile"
  
def getDialog():
  html = """
<!-- enter dialog html code here -->
<p>Select any image URL</p>
"""

  js = """
(function(){
/*
  assign event handlers for dialog
  it's possible to override the init and show fundions of the dialog here..
  catch the event LensesSelected for the event on the click on ok
*/

  $(document).on('LensesSelected', function(evt){
    alert("inet select");
  })
  
  
  
})()
"""

  title = "Internet Image Access"

  return {'js':js, 'html':html, 'title': title}
