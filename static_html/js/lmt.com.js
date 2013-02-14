/**
 * takes care of all the communication to the server 
 */





var com = {
  getCataloguesUrl: "/get_initdata",
  getModelDataUrl: "/get_modeldata",
  saveDataUrl: "/save_model/",
  resultUrl: "/result/",
  refreshCounter: 0,
};




com.getInitData = function(evt) {
  
  var success = function(jsonObj, b, c){
    
    
    //LMT.ui.html.SelectModelDialog.onCatalogueLoad(jsonObj);
    $.event.trigger("GotInitData", jsonObj);
  }
  
  var fail = function(a, b, c){
    tmp=0;
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
com.getModelData = function(evt, model_ids, catalog) {
  
  var success = function(obj, status_text, resp) {
    // obj[0].fields['name']
    // obj[0].fields['channel1_data']
    // obj[0].fields['channel1_url']
    
    log.write("success: <br/>" + obj + "<br/>" + status_text + "<br/>" + resp);
    
    LMT.modelData = obj[0].fields;
    LMT.modelData.id = obj[0].pk;
    
    LMT.modelData.ch = [];
    
    
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
    
    log.write("fail: <br/>" + resp + "<br/>" + status_text + "<br/>" + code);
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
      data: {action: 'init', models: model_ids, catalog: catalog}, 
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
com.UploadModel = function() {

  var success = function(jsonResp, statusTxt, XHRRespObj) {
    log.write("success1: <br/>result_id:" + jsonResp.result_id);
    LMT.simulationData.resultId = jsonResp.result_id;
    //LMT.simulationData.resultModelHash = LMT.actionstack.current.stateStr.hashCode();
    $.event.trigger("UploadModelComplete")
  };
  
  var fail = function(a, b, c) {
    log.write("fail: <br/>" + a + "<br/>" + b + "<br/>" + c + "<hr>" + a.responseText);
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
        isFinal: false, //isFinal
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



/*
 * can be called after saving a result
 * will return a json obj with the urls to the images
 * that can be gotten with long pulling later
 */
com.GetSimulation = function(){
  var success = function(jsonResp, statusTxt, XHRRespObj) {
    log.write("success1: " + jsonResp.status + " " + jsonResp.result_id);
    
    LMT.simulationData.img = [];
    if (jsonResp.status!="READY"){ //polling
      if (jsonResp.status=="FAILURE") { // did the worker crash?
        alert("error with worker: crash");
        $('body').css('cursor', '');
        return false;
      }
      if (LMT.com.refreshCounter>30*10) { //if more than 10min waiting time... assume 0.5 refresh / sec
        alert("server not available");
        LMT.com.refreshCounter = 0;
        $('body').css('cursor', '');
        return false;
      }

      setTimeout(function(){$.event.trigger("GetSimulation");}, 2000);
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
    log.write("fail: <br/>" + a + "<br/>" + b + "<br/>" + c + "<hr>" + a.responseText);
  };


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
  $('body').css('cursor', 'progress');
}






LMT.com = com;
