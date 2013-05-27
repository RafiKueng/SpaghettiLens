LMT.datasources.masterlens = {}
LMT.datasources.masterlens.init = function(){
/*
  assign event handlers for dialog
  it's possible to override the init and show fundions of the dialog here..
  catch the event LensesSelected for the event on the click on ok
*/
  
  
  $(document).on('LensesSelected', function(evt){
    alert("inet select");

    //get the lens ids
    var ids = new Array();
    $('.dtab_row_selected').each(function(i){
      ids.push(int($(this).children()[1].innerHTML));
    });
    
    //start the creation of the database objects
    $.ajax('/api', {
      type: "POST",
      success: LMT.datasource.createSuccess,
      error: LMT.datasource.createFail,
      data: {
        action: "datasourceApi",
        do: "createObj",
        user: LMT.datasource.username,
        psw: LMT.datasource.password,
        data: ids,
      },
      datatype: "json",
    });
    
  });

  LMT.datasource.createSuccess = function(evt) {
    alert("createSuccess");
  }

  LMT.datasource.createFail = function(evt) {
    alert("createFail");
  }
  
  
  LMT.ui.html.GenericDatasourceDialog.show = function(evt){
    $('#generic_datasource_dialog').dialog("open");
    $('#btn_gdd_ok').button('disable');
    $('#ml_loginfield').show();
    $('#ml_selection_field').hide();
  }
  
  
  $('#ml_login').button().click(function(){
    var user = $('#username').val();
    var psw = $('#psw').val();
    //alert(user + ' // ' + psw);
    
    LMT.datasource.username = user;
    LMT.datasource.password = psw;
    
    LMT.datasource.login(user, psw);
    
    //$('#ml_loginfield').hide();
    //$('#ml_selection_field').show();
    //$('#btn_gdd_ok').button('enable');
  });
  
  
  LMT.datasource = {};
  
  LMT.datasource.login = function(user, psw) {
    $('#ml_loginfield').append('<p>Please wait...</p>');
    $.ajax('/api', {
      type: "POST",
      success: LMT.datasource.loginSuccess,
      error: LMT.datasource.loginFail,
      data: {
        action: "datasourceApi",
        do: "login",
        user: user,
        psw: psw,
      },
      datatype: "json",
    })
  };
  
  //if the request to login returned no errorcode (login still can be rejected)
  LMT.datasource.loginSuccess = function(json, b, c) {
    if (!json.status == 'ok') {
      alert("login failed. bad username / password?");
    }
    else {

      $('#ml_selection_field').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="ds_table"></table>' );
      $('#ds_table').append('<thead><tr><th>x</th><th>id</th><th>name</th><th>image</th></tr></thead>');
      var tbody = $('<tbody></tbody>');

      
      for (var i=0; i<json.list.length; i++){
        var elem = json.list[i];
        tbody.append('<tr>'+ 
          '<td> </td>' +
          '<td>' + elem.id + '</td>' +
          '<td>' + elem.name + '</td>' +
          '<td>' + '<img class="dtab_img" src="'+elem.pvurl+'"/>' + '</td>' +
          '</tr>');
      }
      
      $('#ds_table').append(tbody);
      
      $('#ds_table > tbody > tr').click( function() {
        $(this).toggleClass('dtab_row_selected');
        
        
        var r = $(this).children()[0];
        //r.innerHTML = (r.innerHTML == 'X' ? ' ' : 'X');
        if (r.innerHTML == 'X'){
          $('#ds_table').dataTable().fnUpdate(' ', this,0);
        }
        else {
          $('#ds_table').dataTable().fnUpdate('X', this,0);
        }
        
        
        if ($('.dtab_row_selected').length > 0) {
          $('#btn_gdd_ok').button('enable');
        }
        else {
          $('#btn_gdd_ok').button('disable');
        }
      });
      
      $('#ds_table').dataTable( {
        "bJQueryUI": true,
        "bPaginate": false,
        "bLengthChange": false,
        "bAutoWidth": true,
        "sScrollY": "500px",
        "bScrollCollapse": true,
      });
      
      $('#ml_loginfield').hide();
      $('#ml_selection_field').show();
    }
      
    
  };
  
  LMT.datasource.loginFail = function(a, b, c) {
    alert('login request failed');
  };
  
  
  
};