/**
 * takes care of all the communication to the server 
 */





var com = {
  getCataloguesUrl: "/get_initdata",
  getModelDataUrl: "/get_modeldata",
  saveDataUrl: "/save_model/",
  saveDataFinalUrl: "/save_model_final/",
  resultUrl: "/result/",
  refreshCounter: 0,
};




com.getInitData = function(evt) {
  
  var success = function(jsonObj, b, c){
    log("getInitData | success");
    $.event.trigger("GotInitData", jsonObj);
  }
  
  var fail = function(a, b, c){
    log("getInitData | fail");
  }  
  
  $.ajax(LMT.com.serverUrl + LMT.com.getCataloguesUrl + "/", {
      type:"GET",
      success: success,
      error: fail,
      dataType:"json", //data type expected from server
  });
  
}



/**
 * gets the model data such as
 * - model name
 * - channels [1-3] with 
 *   * colorsettings {r, g, b, br, co}
 *   * url to image file  
 * 
 * can call for a specific model_id or a random model
 * if auth user: you'll get a model you havent already done
 */
com.getModelData = function(evt, model_ids, catalog, action) {
  
  var success = function(obj, status_text, resp) {
    // obj[0].fields['name']
    // obj[0].fields['channel1_data']
    // obj[0].fields['channel1_url']
    
    log("com.getModelData | success", "pk: " + obj[0].pk);
    
    LMT.modelData = obj[0].fields;
    LMT.modelData.id = obj[0].pk;
    LMT.modelData.nTodo = obj[1].todo;
    LMT.modelData.nDone = obj[1].done;
    LMT.modelData.nLenses = obj[1].nr;
    LMT.modelData.nextAvail = obj[1].next_avail;
    LMT.modelData.prevAvail = obj[1].prev_avail;
    
    LMT.model.Parameters.z_src = LMT.modelData.z_source || 1;
    LMT.model.Parameters.z_lens = LMT.modelData.z_lens || 0.5;
    
    LMT.modelData.ch = [];
    
    LMT.modelData.imgurl = JSON.parse(obj[0].fields.img_data).url
    
    /*
    if (LMT.modelData['img_type'] == "CO") {
      var data = LMT.modelData['channel1_data']=="" ? {co:1, br:0} : JSON.parse(LMT.modelData['channel1_data']);
      LMT.modelData.ch.push({
        r: 0,
        g: 0,
        b: 0,
        co: data.co,
        br: data.br,
        url: LMT.modelData['channel1_imgurl'],
        type: LMT.modelData['channel1_type']
      });
    }    
    else {
      for (var i = 1; i<=5; i++){
        if (LMT.modelData['channel'+i+'_imgurl']==""){
          continue;
        }
        
        if (LMT.modelData['channel'+i+'_data'] && LMT.modelData['channel'+i+'_data'].length>0){
          var data = JSON.parse(LMT.modelData['channel'+i+'_data']);
        }
        else {
          var data = {r:Math.random(), g:Math.random(), b:Math.random(), co:1, br:0};
        }
        LMT.modelData.ch.push({
          r: data.r,
          g: data.g,
          b: data.b,
          co: data.co,
          br: data.br,
          url: LMT.modelData['channel'+i+'_imgurl'],
          type: LMT.modelData['channel'+i+'_type']
        });
      }
    }
    */    
    $.event.trigger('ReceivedModelData');
  };
  
  var fail = function(resp, status_text, code) {
    if (resp.responseText == "this model is not available") {
      alert("you asked for a model that's not on the server");
      $.event.trigger("ShowSelectModelDataDialog");
    }
    else if (resp.status == 404) {
      alert("server configuration error: can't get model data from url: "+LMT.com.getModelDataUrl);
    }
    else if (status_text == "error") {
      alert("server is down, please try later");
    }
    
    log("com.getModelData | fail", resp, status_text, code);
  };

  /*
  $.ajax(LMT.com.serverUrl + LMT.com.getModelDataUrl+'/'+model_id, {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: {model_id: model_id, catalog_id: catalog_id}, 
      dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });
  */
 
  $.ajax(LMT.com.serverUrl + LMT.com.getModelDataUrl+'/', {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: {action: action, models: model_ids, catalog: catalog}, 
      dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });
}




/**
 * event handler 
 * save the resulting model string in the database
 * - model name
 * - model string: the serialized model data (json)
 * - isFinal: is this a temoprary push or a save of a final model
 * 
 * post returns json 
 * {status: "OK" or "BAD..."
 */
com.UploadModel = function(evt) {

  var success = function(jsonResp, statusTxt, XHRRespObj) {
    log('com.UploadModel | success', 'result_id:' + jsonResp.result_id);
    LMT.simulationData.resultId = jsonResp.result_id;
    //LMT.simulationData.resultModelHash = LMT.actionstack.current.stateStr.hashCode();
    $.event.trigger("UploadModelComplete")
  };
  
  var fail = function(a, b, c) {
    log("com.UploadModel | fail", a, b, c, a.responseText);
    var win=window.open('about:blank');
    with(win.document)
    {
      open();
      write(a.responseText);
      close();
    }
  };


  if (LMT.model.Sources.length==0){
    alert("Please create a model first before uploading");
    return false;
  }
  
  var data = {
        modelid: LMT.modelData.id,
        string: LMT.model.getStateAsString(),
        isFinal: ( evt.type=="SaveModel" ? true : false ), //isFinal
        username: LMT.settings.username
    };
  
  LMT.simulationData.resultId = -1;
  LMT.simulationData.resultModelHash = data.string.hashCode();
  
  $.ajax(LMT.com.serverUrl + LMT.com.saveDataUrl, {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: data, 
      dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });

}




/**
 * event handler 
 * save the resulting model string in the database as FINAL RESULT
 * - model name
 * - model string: the serialized model data (json)
 * - isFinal: true
 * 
 * post returns json 
 * {status: "OK" or "BAD..."
 */
com.SaveModel = function(evt) {

  var success = function(jsonResp, statusTxt, XHRRespObj) {
    log('com.SaveModel | success', 'result_id: ' + jsonResp.result_id);
    LMT.simulationData.resultId = jsonResp.result_id;
    //LMT.simulationData.resultModelHash = LMT.actionstack.current.stateStr.hashCode();
    //$.event.trigger("UploadModelComplete")
    /*
      alert("Model saved! \n(result_id: "+jsonResp.result_id+")\n"+
      "access the raw data with:\n"+
      "http://mite.physik.uzh.ch/data/"+jsonResp.result_id);
    */
    $.event.trigger("SavedModel", jsonResp.result_id);
  };
  
  var fail = function(a, b, c) {
    log('com.SaveModel | fail', a, b, c, a.responseText);

    /*
    var win=window.open('about:blank');
    with(win.document)
    {
      open();
      write(a.responseText);
      close();
    }
    */
  };


  if (LMT.model.Sources.length==0){
    alert("Please create a model first before uploading");
    return false;
  }
  
  var data = {
        modelid: LMT.modelData.id,
        resultid: LMT.simulationData.resultId,
        isFinal: ( evt.type=="SaveModel" ? true : false ), //isFinal
        username: LMT.settings.username,
        imgData: LMT.ui.svg.img
    };
  
  //LMT.simulationData.resultId = -1;
  //LMT.simulationData.resultModelHash = data.string.hashCode();
  
  $.ajax(LMT.com.serverUrl + LMT.com.saveDataFinalUrl, {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: data, 
      dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });

}





/*
 * can be called after saving a result
 * will return a json obj with the urls to the images
 * that can be gotten with long pulling later
 */
com.GetSimulation = function(){
  var success = function(jsonResp, statusTxt, XHRRespObj) {
    log("com.GetSimulation | success", 'status:' + jsonResp.status + ' res_id: ' + jsonResp.result_id);
    
    LMT.simulationData.img = [];
    if (jsonResp.status!="READY"){ //polling
      if (jsonResp.status=="FAILURE") { // did the worker crash?
        alert("error with worker: crash");
        $.event.trigger("GetSimulationFail");
        $('body').css('cursor', '');
        return false;
      }
      else if (jsonResp.status=="REVOKED") { // is the server under heavy load?
        alert("the server is currently under heavy load\nYour request couldn't be processed, I've waited 30sec, then gave up.\nTry again later. Sorry!\nIf this happens often please inform Rafi to upgrade the server!");
        $('body').css('cursor', '');
        $.event.trigger("GetSimulationFail");
        return false;
      }
      /*
      if (LMT.com.refreshCounter>LMT.settings.estimate*2+10) { //if more than 10min waiting time... assume 0.5 refresh / sec
        alert("Timeout on the server side..");
        LMT.com.refreshCounter = 0;
        $('body').css('cursor', '');
        return false;
      }*/

      setTimeout(function(){$.event.trigger("GetSimulation");}, 1000);
      LMT.com.refreshCounter += 1;
      return;
    }
    
    var n = parseInt(jsonResp.n_img);
    for (var i = 1; i<=n; i++){
      imgdata = {
        desc: jsonResp['img'+i+'desc'],
        url: jsonResp['img'+i+'url'], 
      }
      LMT.simulationData.img.push(imgdata);
    }
    $('body').css('cursor', '');
    $.event.trigger("ReceivedSimulation");
  };
  
  var fail = function(a, b, c) {
    log('com.GetSimulation | fail', a, b, c, a.responseText);
    if (c && c=='Bad Gateway') {
      alert("the server is currently not online. Please drop a note to Rafael. I'm sorry!");
    }
    else {
      alert('This it bad.. server is not reachable. I\'m sorry! Please let Rafael know about this error!');
    }
    $('body').css('cursor', '');
    $.event.trigger("GetSimulationFail");
  };


  $('body').css('cursor', 'progress');
  $.event.trigger("WaitForSimulation");

  $.ajax(LMT.com.serverUrl + LMT.com.resultUrl + LMT.simulationData.resultId + ".json", {
      type:"GET",
      //contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      //data: {
      //  modelid: LMT.modelData.id,
      //  string: LMT.actionstack.current.stateStr,
      //  isFinal: false //isFinal
      //}, 
      //dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });
}





com.getDatasourcesList = function(evt) {
  
  var success = function(jsonObj, b, c){
    log('com.getDatasourcesList | success');
    $.event.trigger("RcvDatasourcesList", [jsonObj]);
  }
  
  var fail = function(a, b, c){
    log('getDatasourcesList | fail');
    alert("Server api down! I'm sorry! Please drop a mail to rafael about this");
  }  
  
  var data = {action: 'getSrcList'};
  
  $.ajax(LMT.com.serverUrl + "/api", {
      type:"POST",
      success: success,
      error: fail,
      data: data,
      dataType:"json", //data type expected from server
  });
  
}


com.getDatasourceDialog = function(evt, id, uname) {
  
  var success = function(jsonObj, b, c){
    log('com.getDatasourceDialog | success');
    $.event.trigger("RcvDatasourceDialog", [jsonObj]);
  }
  
  var fail = function(a, b, c){
    log('com.getDatasourceDialog | fail');
    alert("Server api down. I'm sorry! Please drop a mail to rafael about this");
  }  
  
  var data = {
    action: 'selectSource',
    id: id,
    uname: uname
  };
  
  $.ajax(LMT.com.serverUrl + "/api", {
      type:"POST",
      success: success,
      error: fail,
      data: data,
      dataType:"json", //data type expected from server
  });
  
}


LMT.com = com;
