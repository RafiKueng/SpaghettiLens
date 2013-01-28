/**
 * takes care of all the communication to the server 
 */





var com = {
  serverUrl: "http://localhost:8000",
  
  getModelDataUrl: "/get_modeldata",
  
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
    
    log.write("success1: <br/>" + a + "<br/>" + b + "<br/>" + c);
  };
  
  var fail = function(resp, status_text, code) {
    if (resp.status == 404) {}
    if (resp.responseText == "this model is not available") {}
    
    log.write("fail: <br/>" + a + "<br/>" + b + "<br/>" + c);
  };


  $.ajax(LMT.com.serverUrl + LMT.com.getModelDataUrl+'/'+model_id {
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
 * save the resulting model string in the database
 * - model name
 * - model string: the serialized model data (json)
 * - isFinal: is this a temoprary push or a save of a final model
 * 
 * post returns json 
 * {status: "OK" or "BAD..."
 */
com.saveModel = function(model_id, modelstring, isFinal) {

  var success = function(jsonResp, statusTxt, XHRRespObj) {
    log.write("success1: <br/>" + jsonResp + "<br/>" + statusTxt + "<br/>" + XHRRespObj);
  };
  
  var fail = function(a, b, c) {
    log.write("fail: <br/>" + a + "<br/>" + b + "<br/>" + c + "<hr>" + a.responseText);
  };


  $.ajax(LMT.com.serverUrl, {
      type:"POST",
      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
      data: {
        modelid: model_id,
        string: modelstring,
        isFinal: isFinal
      }, 
      dataType:"json", //data type expected from server
      success:success,
      error: fail
      //mimeType: "text/plain"
  });

}









LMT.com = com;