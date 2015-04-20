/**
 * takes care of all the communication to the server 
 */




/**
 * This is the old config.. slowly replace it with the new one below
 */
var com = {
  getCataloguesUrl: "/get_initdata",
  getModelDataUrl: "/get_modeldata",
  saveDataUrl: "/save_model/",
  saveDataFinalUrl: "/save_model_final/",
  resultUrl: "/result/",
  refreshCounter: 0,
};


com.config = {
    lensesAPI: "/lenses/api",
    spaghettiAPI: "/spaghetti/api",
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


com.getAndLoadResult = function(evt, rid, loadHandler) {
  var success = function(obj, status_text, resp) {
    res_data = {
      'model_id': obj.model_id,
      'json_str': obj.json_str,
    };
    loadHandler(res_data);
  }
  
  var fail = function(resp, status_text, code) {
    log("getAndLoadResult | fail", resp, status_text, code);
  };
  
  var data = {
    action: 'getResultData',
    rid: rid,
  };
  
  $.ajax(LMT.com.serverUrl + "/api", {
      type:"POST",
      success: success,
      error: fail,
      data: data,
      dataType:"json", //data type expected from server
  });
  
  
}




/** NEW V2
 * gets lens data from server
 */
com.getLensData = function(evt, lens_id) {

    log("com.getLensData | start", "lens_id: " + lens_id);

    var success = function(json, status, xhr) {
        log("com.getLensData / success ", json.success);
        
        if (json.success) {
            
            var jsonimg = json.data.imgdata.COMPOSITE_PIXEL_IMAGE['0001'].DEFAULT
            
            LMT.lensData = json.data;
//            LMT.lensData.imgurl = json.data.imgdata
//                                           .COMPOSITE_PIXEL_IMAGE['0001']
//                                           .DEFAULT.urls[0];

            var burl = "/media/lenses/"
            var h1 = lens_id.slice(0,2);
            var h2 = lens_id.slice(2);
            var dtype = "COMPOSITE_PIXEL_IMAGE";
            var dsrc = "0001";
            var stype = "DEFAULT";
            var ext = jsonimg.format;
            
            LMT.lensData.imgurl = burl + h1 + "/" + h2 + "/" +
                                  dtype + "-" + dsrc + "-" + stype + "." + ext;
            
            LMT.model.Parameters.orgPxScale = jsonimg.scale[0] || null;
            //TODO ask user if Null

            //TODO read scidata and save it into model.Parameters
//            LMT.model.Parameters.z_src = LMT.modelData.z_source || 1;
//            LMT.model.Parameters.z_lens = LMT.modelData.z_lens || 0.5;
//            LMT.model.Parameters.orgPxScale = LMT.modelData.add_data.orgPxScale || null;

            $.event.trigger('ReceivedModelData');
            
        } else { alert("APIError: " + json.error); }
        
        log("com.getLensData \\ success ");
    };

    var data = {
        action: 'get_lens_data',
        lens_id: lens_id,
    };
    
    $.ajax(com.config.lensesAPI, {
        type:"GET",
        data: data,
        dataType:"json",
        success:success,
        error: function () { alert("lens api not available (server down?)"); },
    });
    
    
    log("com.getLensData | end");
};



//V2 is above!
///**
// * gets the model data such as
// * - model name
// * - channels [1-3] with 
// *   * colorsettings {r, g, b, br, co}
// *   * url to image file  
// * 
// * can call for a specific model_id or a random model
// * if auth user: you'll get a model you havent already done
// */
//com.getModelData = function(evt, model_ids, catalog, action) {
//  
//  var success = function(obj, status_text, resp) {
//    // obj[0].fields['name']
//    // obj[0].fields['channel1_data']
//    // obj[0].fields['channel1_url']
//    
//    log("com.getModelData | success", "pk: " + obj[0].pk);
//    
//    var pid = null;
//    if (LMT.modelData && LMT.modelData.parentId) {pid = LMT.modelData.parentId;}
//    LMT.modelData = obj[0].fields;
//    if (pid) {LMT.modelData.parentId = pid;}
//    LMT.modelData.id = obj[0].pk;
//    LMT.modelData.nTodo = obj[1].todo;
//    LMT.modelData.nDone = obj[1].done;
//    LMT.modelData.nLenses = obj[1].nr;
//    LMT.modelData.nextAvail = obj[1].next_avail;
//    LMT.modelData.prevAvail = obj[1].prev_avail;
//    
//    LMT.modelData.add_data = JSON.parse(obj[0].fields.add_data)
//    
//    LMT.model.Parameters.z_src = LMT.modelData.z_source || 1;
//    LMT.model.Parameters.z_lens = LMT.modelData.z_lens || 0.5;
//    LMT.model.Parameters.orgPxScale = LMT.modelData.add_data.orgPxScale || null;
//    
//    LMT.modelData.ch = [];
//    
//    LMT.modelData.imgurl = JSON.parse(obj[0].fields.img_data).url
//    
//    /*
//    if (LMT.modelData['img_type'] == "CO") {
//      var data = LMT.modelData['channel1_data']=="" ? {co:1, br:0} : JSON.parse(LMT.modelData['channel1_data']);
//      LMT.modelData.ch.push({
//        r: 0,
//        g: 0,
//        b: 0,
//        co: data.co,
//        br: data.br,
//        url: LMT.modelData['channel1_imgurl'],
//        type: LMT.modelData['channel1_type']
//      });
//    }    
//    else {
//      for (var i = 1; i<=5; i++){
//        if (LMT.modelData['channel'+i+'_imgurl']==""){
//          continue;
//        }
//        
//        if (LMT.modelData['channel'+i+'_data'] && LMT.modelData['channel'+i+'_data'].length>0){
//          var data = JSON.parse(LMT.modelData['channel'+i+'_data']);
//        }
//        else {
//          var data = {r:Math.random(), g:Math.random(), b:Math.random(), co:1, br:0};
//        }
//        LMT.modelData.ch.push({
//          r: data.r,
//          g: data.g,
//          b: data.b,
//          co: data.co,
//          br: data.br,
//          url: LMT.modelData['channel'+i+'_imgurl'],
//          type: LMT.modelData['channel'+i+'_type']
//        });
//      }
//    }
//    */    
//    $.event.trigger('ReceivedModelData');
//  };
//  
//  var fail = function(resp, status_text, code) {
//    if (resp.responseText == "this model is not available") {
//      alert("you asked for a model that's not on the server");
//      $.event.trigger("ShowSelectModelDataDialog");
//    }
//    else if (resp.status == 404) {
//      alert("server configuration error: can't get model data from url: "+LMT.com.getModelDataUrl);
//    }
//    else if (status_text == "error") {
//      alert("server is down, please try later");
//    }
//    
//    log("com.getModelData | fail", resp, status_text, code);
//  };
//
//  /*
//  $.ajax(LMT.com.serverUrl + LMT.com.getModelDataUrl+'/'+model_id, {
//      type:"POST",
//      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
//      data: {model_id: model_id, catalog_id: catalog_id}, 
//      dataType:"json", //data type expected from server
//      success:success,
//      error: fail
//      //mimeType: "text/plain"
//  });
//  */
// 
//  $.ajax(LMT.com.serverUrl + LMT.com.getModelDataUrl+'/', {
//      type:"POST",
//      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
//      data: {action: action, models: model_ids, catalog: catalog}, 
//      dataType:"json", //data type expected from server
//      success:success,
//      error: fail
//      //mimeType: "text/plain"
//  });
//}




















/** V2 NEW
 * event handler 
 * save the resulting model string in the database
 * as a temporary result for rendering
 * - model name
 * - model string: the serialized model data (json)
 * - isFinal: false
 * 
 * post returns json 
 * {success: True False
 */
com.UploadModel = function(evt) {
    
    log("com.UploadModel / start ");
    
    if (LMT.model.Sources.length==0){
        alert("Please create a model first before uploading");
        return false;
    }

    console.log(1);
    
//    var nmodel = {
//        ExternalMasses:      jQuery.extend(true, {}, LMT.model.ExternalMasses),
//        MinMmaxSwitchAngle:  jQuery.extend(true, {}, LMT.model.MinMmaxSwitchAngle),
//        NrOf:                jQuery.extend(true, {}, LMT.model.NrOf),
//        Parameters:          jQuery.extend(true, {}, LMT.model.Parameters),
//        Rulers:              jQuery.extend(true, {}, LMT.model.Rulers),
//        Sources:             jQuery.extend(true, {}, LMT.model.Sources),
//    }
    
    var data = {
        action: "save_model",
        lens_id: LMT.lensData._id,
//        lmtmodel: jQuery.extend(true, {}, LMT.model),
        lmtmodel: LMT.model.getStateAsString(),
        username: LMT.settings.username ? LMT.settings.username : '',
        parent: LMT.modelData.parentId ? LMT.modelData.parentId : '',
        comment: '',
        //isFinal: ( evt.type=="SaveModel" ? true : false ), //isFinal
    };

    LMT.simulationResult.modelId = -1;
    LMT.simulationResult.resultModelHash = LMT.model.getStateAsString().hashCode();
    //TODO find a better way to hash the model.. this is a left over from V1
    
    console.log(2);

    var success = function(json, status, xhr) {
        
        log('com.UploadModel.success / ', 'result_id:' + json.model_id);
        
        LMT.simulationResult.modelId = json.model_id;
        //LMT.simulationResult.resultModelHash = LMT.actionstack.current.stateStr.hashCode();
        $.event.trigger("UploadModelComplete")
    };

    console.log(3);

    $.ajax(com.config.spaghettiAPI, {
        type:"POST",
        success:success,
        error: function (a,b,c) { log('fail',a,b,c); alert("api not available"); },
        data: data, 
        dataType: "json"
    });

    log("com.UploadModel \\ end ");
}



// OLD ONE new above
///**
// * event handler 
// * save the resulting model string in the database
// * as a temporary result for rendering
// * - model name
// * - model string: the serialized model data (json)
// * - isFinal: false
// * 
// * post returns json 
// * {status: "OK" or "BAD..."
// */
//com.UploadModel = function(evt) {
//
//  var success = function(jsonResp, statusTxt, XHRRespObj) {
//    log('com.UploadModel | success', 'result_id:' + jsonResp.result_id);
//    LMT.simulationResult.resultId = jsonResp.result_id;
//    //LMT.simulationResult.resultModelHash = LMT.actionstack.current.stateStr.hashCode();
//    $.event.trigger("UploadModelComplete")
//  };
//  
//  var fail = function(a, b, c) {
//    log("com.UploadModel | fail", a, b, c, a.responseText);
//    var win=window.open('about:blank');
//    with(win.document)
//    {
//      open();
//      write(a.responseText);
//      close();
//    }
//  };
//
//
//  if (LMT.model.Sources.length==0){
//    alert("Please create a model first before uploading");
//    return false;
//  }
//  
//  var data = {
//        modelid: LMT.modelData.id,
//        string: LMT.model.getStateAsString(),
//        isFinal: ( evt.type=="SaveModel" ? true : false ), //isFinal
//        username: LMT.settings.username ? LMT.settings.username : '',
//        parentid: (LMT.modelData.parentId ? LMT.modelData.parentId : -1)
//    };
//  
//  LMT.simulationResult.resultId = -1;
//  LMT.simulationResult.resultModelHash = data.string.hashCode();
//  
//  $.ajax(LMT.com.serverUrl + LMT.com.saveDataUrl, {
//      type:"POST",
//      contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
//      data: data, 
//      dataType:"json", //data type expected from server
//      success:success,
//      error: fail
//      //mimeType: "text/plain"
//  });
//
//}




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
    LMT.simulationResult.resultId = jsonResp.result_id;
    //LMT.simulationResult.resultModelHash = LMT.actionstack.current.stateStr.hashCode();
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
        resultid: LMT.simulationResult.resultId,
        isFinal: ( evt.type=="SaveModel" ? true : false ), //isFinal
        username: LMT.settings.username,
        imgData: LMT.ui.svg.img,
        parentid: (LMT.modelData.parentId ? LMT.modelData.parentId : -1)
    };
  
  //LMT.simulationResult.resultId = -1;
  //LMT.simulationResult.resultModelHash = data.string.hashCode();
  
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









/** NEW V2
 * gets the progress of the rendering of a modelID
 */
com.GetRenderingProgress = function () {

    log('com.GetRenderingProgress / start', 'modelId: ' + LMT.simulationResult.modelId);

    var data = {
        action: "get_rendering_status",
        model_id: LMT.simulationResult.modelId
    };

    var success = function (json, status, xhr) {

        log('com.GetRenderingProgress.success', 'status='+json.status);

        if (json.success) {
            if (json.status === 'done') {
                LMT.simulationResult.imgs = json.imgs; /*TODO this part is a quick hack*/
                //LMT.settings.renderedEqualsModel = true; // this is set in lmt.ui.out.load
                $.event.trigger("RenderingComplete");
                
            } else if (json.status === 'pending' || json.status === 'progress') {
                LMT.simulationResult.progress = json.progress;
                $.event.trigger("UpdateRenderingStatus");
                setTimeout(function(){$.event.trigger("GetRenderingProgress");}, 500);
                
            } else { // status = failed??
                $.event.trigger("RenderingFailed");
            }

        } else { alert("APIError: " + json.error); }
    };

    $.ajax(com.config.spaghettiAPI, {
        type: "GET",
        success: success,
        error: function () { alert("api not available"); },
        data: data,
        dataType: "json" //data type expected from server
    });

    log('com.GetRenderingProgress \\ end');

}





/** NEW V2
 * Starts the rendering of a submitted modelID
 */
com.StartRendering = function () {

    log('com.StartRendering / start', 'modelId: ' + LMT.simulationResult.modelId);

    var data = {
        action: "start_rendering",
        model_id: LMT.simulationResult.modelId
    };

    var success = function (json, status, xhr) {
        log('com.StartRendering.success ==', + json.status);

        if (json.success) {
            $.event.trigger("GetRenderingProgress");

        } else { alert("APIError: " + json.error); }
    };

    $.ajax(com.config.spaghettiAPI, {
        type: "GET",
        success: success,
        error: function () { alert("api not available"); },
        data: data,
        dataType: "json" //data type expected from server
    });

    log('com.StartRendering \\ end');

}

// OLD Version V2, no new (new scematics)
///*
// * can be called after saving a result
// * will return a json obj with the urls to the images
// * that can be gotten with long pulling later
// */
//com.GetSimulation = function(){
//  var success = function(jsonResp, statusTxt, XHRRespObj) {
//    log("com.GetSimulation | success", 'status:' + jsonResp.status + ' res_id: ' + jsonResp.result_id);
//    
//    LMT.simulationResult.img = [];
//    if (jsonResp.status!="READY"){ //polling
//      if (jsonResp.status=="FAILURE") { // did the worker crash?
//        alert("error with worker: crash");
//        $.event.trigger("GetSimulationFail");
//        $('body').css('cursor', '');
//        return false;
//      }
//      else if (jsonResp.status=="REVOKED") { // is the server under heavy load?
//        alert("the server is currently under heavy load\nYour request couldn't be processed, I've waited 30sec, then gave up.\nTry again later. Sorry!\nIf this happens often please inform Rafi to upgrade the server!");
//        $('body').css('cursor', '');
//        $.event.trigger("GetSimulationFail");
//        return false;
//      }
//      /*
//      if (LMT.com.refreshCounter>LMT.settings.estimate*2+10) { //if more than 10min waiting time... assume 0.5 refresh / sec
//        alert("Timeout on the server side..");
//        LMT.com.refreshCounter = 0;
//        $('body').css('cursor', '');
//        return false;
//      }*/
//
//      setTimeout(function(){$.event.trigger("GetSimulation");}, 1000);
//      LMT.com.refreshCounter += 1;
//      return;
//    }
//
//    var imgs = jsonResp.imgs;
//    var n = imgs.length;
//    
//    LMT.simulationResult.imgs = new Array(n);
//    
//    for (var i=0; i<n; i++) {
//      LMT.simulationResult.imgs[i] = {
//        type: imgs[i].type,
//        url: imgs[i].url,
//      };
//    }
//    
//    /*
//    var n = parseInt(jsonResp.n_img);
//    for (var i = 1; i<=n; i++){
//      imgdata = {
//        desc: jsonResp['img'+i+'desc'],
//        url: jsonResp['img'+i+'url'], 
//      }
//      LMT.simulationResult.img.push(imgdata);
//    }
//    */
//    
//    $('body').css('cursor', '');
//    $.event.trigger("ReceivedSimulation");
//  };
//  
//  var fail = function(a, b, c) {
//    log('com.GetSimulation | fail', a, b, c, a.responseText);
//    if (c && c=='Bad Gateway') {
//      alert("the server is currently not online. Please drop a note to Rafael. I'm sorry!");
//    }
//    else {
//      alert('This it bad.. server is not reachable. I\'m sorry! Please let Rafael know about this error!');
//    }
//    $('body').css('cursor', '');
//    $.event.trigger("GetSimulationFail");
//  };
//
//
//  $('body').css('cursor', 'progress');
//  $.event.trigger("WaitForSimulation");
//
//  $.ajax(LMT.com.serverUrl + LMT.com.resultUrl + LMT.simulationResult.resultId + ".json", {
//      type:"GET",
//      //contentType: 'application/x-www-form-urlencoded; charset=UTF-8', //default anyways, type of data sent TO server
//      //data: {
//      //  modelid: LMT.modelData.id,
//      //  string: LMT.actionstack.current.stateStr,
//      //  isFinal: false //isFinal
//      //}, 
//      //dataType:"json", //data type expected from server
//      success:success,
//      error: fail
//      //mimeType: "text/plain"
//  });
//}




//v2 new version
com.getSelectDatasourceDialog = function(evt) {
    
    var success = function(json, b, c){
        if (json.success) {
            log('com.getDatasourceSelectionDialog | success');
            //$.event.trigger("RcvDatasourcesList", [jsonObj]);
            f = new Function(json.jsobj);
            $.event.trigger("GotSelectDatasourceDialog", [json.html, f()]);
        } else {alert("APIError: "+json.error);}
    }
  
    var fail = function(a, b, c){
        log('com.getDatasourceSelectionDialog | fail');
        alert("Server api down! I'm sorry! Please drop a mail to rafael about this");
    }  
  
    var data = {action: 'get_select_lens_dialog'};
  
    $.ajax(com.config.lensesAPI, {
        type: "GET",
        data: data,
        success: success,
        error: fail,
        dataType: "json", //data type expected from server
    });

}





LMT.com = com;
