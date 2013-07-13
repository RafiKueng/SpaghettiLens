LMT.datasources.spacewarps = {}
LMT.datasources.spacewarps.init = function(){
/*
  assign event handlers for dialog
  it's possible to override the init and show fundions of the dialog here..
  catch the event LensesSelected for the event on the click on ok
*/
  
  
  $(document).on('LensesSelected', function(evt){
    //alert("inet select");

    //get the lens ids
    var ids = new Array();
    $('.dtab_row_selected').each(function(i){
      ids.push(parseInt($(this).children()[1].innerHTML));
    });
    
    //start the creation of the database objects
    $.ajax('/api', {
      type: "POST",
      success: LMT.datasource.createSuccess,
      error: LMT.datasource.createFail,
      data: {
        'action': "datasourceApi",
        'src_id': 3,
        'do': "createObj",
        'data': LMT.datasource.lenses,
      },
      datatype: "json",
    });
    
  });

  LMT.datasource.createSuccess = function(modelIDs) {
    $.event.trigger("GetModelData", [models = modelIDs, catalog='', action='init']);
    $('#generic_datasource_dialog').dialog("close");
  }

  LMT.datasource.createFail = function(evt) {
    alert("createFail");
  }
  
  
  LMT.ui.html.GenericDatasourceDialog.show = function(evt){
    $('#generic_datasource_dialog')
      .dialog("open")
      .keypress(function(e) {
        if (e.keyCode == $.ui.keyCode.ENTER) {
          $('#sw_fetch').button().click();
        }
      });
    $('#btn_gdd_ok').button('disable');
  }
  
  
  $('#sw_fetch').button().click(function(){
    var swid = $('#swid').val();
    swid = swid.replace(/\s*/g, '');
    //alert(swid);
    
    //TODO: default value  if nothing was entered, for dev..
    if (swid=='') {
      swid = 'ASW0001mze';
    }
    
    LMT.datasource.swid = swid;
    
    LMT.datasource.fetch(swid);
  });
  
  
  LMT.datasource.fetch = function(swid) {
    $('#sw_loginfield').append('<p>Please wait...</p>');
    $.ajax('/api', {
      type: "POST",
      success: LMT.datasource.fetchSuccess,
      error: LMT.datasource.fetchFail,
      data: {
        'action': "datasourceApi",
        'src_id': 3,
        'do': "fetch",
        'swid': swid,
      },
      datatype: "json",
    })
  };
  
  //if the request to login returned no errorcode (login still can be rejected)
  LMT.datasource.fetchSuccess = function(json, b, c) {
    if (!json.status == 'ok') {
      alert("fetching failed. sure it's a real image id? they start with 'ASW'");
    }
    else {
      var train = json.list[0].metadata.training;
      if (train && train.length == 0) {train = false;}
      $('#sw_loginfield').append(
        '<p>Got data:<br/>'+
        'id: ' + json.list[0].id + '<br/>' +
        'meta id: ' + json.list[0].metaid + '<br/>' +
        'is training img: ' + (train ? 'yes, @ '+train[0].x+'/'+train[0].y : 'no') +
        '</p>');
      
      LMT.datasource.lenses = [json.list[0].id];
      $('#btn_gdd_ok').button('enable');
      $('#btn_gdd_ok').click();
    }
      
    
  };
  
  LMT.datasource.fetchFail = function(a, b, c) {
    alert('fetching failed. did you enter a valid image id?');
  };
  
  
  
};