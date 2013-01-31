/**
 * takes care of all the communication to the server 
 */





var com = {
  serverUrl: "http://localhost:8000",
  
  getModelDataUrl: "/get_modeldata",
  saveDataUrl: "/save_model/"
  
};


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
com.getModelData = function(model_id) {
  
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
    if (resp.status == 404) {}
    if (resp.responseText == "this model is not available") {}
    
    log.write("fail: <br/>" + obj + "<br/>" + b + "<br/>" + c);
  };


  $.ajax(LMT.com.serverUrl + LMT.com.getModelDataUrl+'/'+model_id, {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: {action: "something"}, 
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
  };
  
  var fail = function(a, b, c) {
    log.write("fail: <br/>" + a + "<br/>" + b + "<br/>" + c + "<hr>" + a.responseText);
  };


  $.ajax(LMT.com.serverUrl + LMT.com.saveDataUrl, {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: {
        modelid: LMT.modelData.id,
        string: LMT.actionstack.current.stateStr,
        isFinal: false //isFinal
      }, 
      dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });

}




com.GetSimulation = function(){
  log.append("get sim");
}






LMT.com = com;