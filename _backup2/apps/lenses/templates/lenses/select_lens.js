/**
 * This object will be passed to the html.dialog() constructor
 */ 
return {

    autoOpen: false,
    minWidth: 550,
    minHeight: 550,
    modal: true,

    open: function () {

        $("#sel_lens").autocomplete({
            minLength: 3,
            delay: 500,
            source: function (request, response) {
                // checkout docu for improvments like cache..
                var data = {
                    action: "get_list_of_lenses",
                    term: request.term
                };

                var success = function (json, status, xhr) {
                    if (json.success) {
                        response(json.data);
                    } else { alert("APIError: " + json.error); }
                };

                $.ajax('/lenses/api', {
                    type: "GET",
                    success: success,
                    error: function () { alert("api not available"); },
                    data: data,
                    dataType: "json" //data type expected from server
                });

                return;
            },
            
            focus: function (event, ui) {
                $("#sel_lens").val(ui.item.label);
                return false; // cancel default event (replace label with value)
            },
            
            select: function (event, ui) {
                $("#sel_lens").val(ui.item.label);
                $("#sel_lens_id").val(ui.item.value);   // probably can remove those and
                                                        // the hidden form files and just
                                                        // save it at the correct spot in js tree
                return false; // cancel default event (replace label with value)
            },
/*
            change: function (event, ui) {

            },

            // Triggered before a search is performed, after minLength and delay.
            search: function (event, ui) {

            },
*/

            response: function (event, ui) {
                if (ui.content.length === 0) {
                    $("#select_lens_datasource").show();
                    $("#sele_ok").button("disable");
                    
                    // so the enered name doen't already exist in the database..
                    // check if its pattern is a valid one given the current datasource
                    // (update of datasource should trigger a search 
                    // $(#datasource).autocomplete("search");)
                    // if it is, enable the fetch button
                    
                    var data = {
                        action: "check_lensname_pattern",
                        lensname: $("#sel_lens").val(),
                        datasource: $("#sel_datasource").val()
                    };

                    var success = function (json, status, xhr) {
                        if (json.success) {
                            if (json.data === true) {
                                $("#sele_fetch").button("enable");
                                $("#select_lens_status_text").html(
                                    "this name looks valid.<br />" +
                                    "try to fetch it to the database"
                                );
                            } else {
                                $("#sele_fetch").button("disable");
                                $("#select_lens_status_text").html("this name looks not valid.");
                            }
                        } else { alert("APIError: " + json.error); }
                    };

                    $.ajax('/lenses/api', {
                        type: "GET",
                        success: success,
                        error: function () { alert("api not available"); },
                        data: data,
                        dataType: "json" //data type expected from server
                    });
                } else {
                    $("#select_lens_datasource").hide();
                    $("#sele_ok").button("enable");
                    $("#sele_fetch").button("disable");
                    $("#select_lens_status_text").html("found maching entries in the database");
                }
            }
        });

        $("#sel_datasource").change(function () {
            $("#sel_lens").autocomplete("search"); //trigger an update
            //alert('selds changed');
        });
        
        $("#select_lens_datasource").hide();
        $("#select_lens_status_text").html("");
        
        var uname = $.cookie('username');
        if (uname) {
            $("#username").val(uname);
//            $('.ui-dialog-buttonpane button:last').focus();
        }
        var ds = $.cookie('datasource');
        if (ds) { $("#sel_datasource").val(ds).trigger("liszt:updated"); }
        
        
    },

    buttons: [
        {
            text: "DC",
            click: function () {
                $("#username").val('');
                $.removeCookie('username');
                $.removeCookie('datasource');
            }
        },
        {
            text: "SC",
            click: function () {
                $.cookie('username', $("#username").val(), { expires: 365 });
                $.cookie('datasource', $("#sel_datasource").val(), { expires: 365 });
            }
        },
        {
            id: "sele_fetch",
            text: "Fetch",
            click: function (evt, ui) {
                
                var data = {
                    action: "fetch_lens",
                    lensname: $("#sel_lens").val(),
                    datasource: $("#sel_datasource").val()
                };

                var success = function (json, status, xhr) {
                    if (json.success === true) {
                        $("#sele_ok").button("enable");
                        $("#sele_fetch").button("disable");
                        $("#select_lens_status_text").html("sucessfully added lens to database.<br/>click ok to continue.");
                        $("#sel_lens_id").val(json.data.lens_id);
                    } else {
                        $("#select_lens_status_text").html(
                            "Something went wrong!<br>" +
                            "( " + json.error + " )<br>" +
                            "If you are sure that the entered ID correct is, " +
                            "please drop me a mail with the error, datasource and the ID!"
                        );
                        alert("APIError: " + json.error); }
                };

                $.ajax('/lenses/api', {
                    type: "GET",
                    success: success,
                    error: function () { alert("api not available"); },
                    data: data,
                    dataType: "json" //data type expected from server
                });
                
                $("#select_lens_status_text").html(
                    "...fetching data...<br>" +
                    "please be patient..."
                );
                
            }
        },
        {
            id: "sele_edit",
            text: "Edit",
            click: function () {
                alert("noop: not implemented"); //TODO
            }
        },
        {
            id: "sele_ok",
            text: "Ok",
            click: function (evt) {
                var lens_name = $("#sel_lens").val();
                var lens_id = $("#sel_lens_id").val();
                var uname = $("#username").val();

                if ( ! lens_name || ! lens_id || lens_id.length < 64) {
                    alert("OUuups, that should not pappen.. Please inform Rafa what you did!");
                    return;
                } else if (!uname){
                    alert("Please enter your name");
                } else
                {
                    LMT.settings.username = uname;
                    $.event.trigger("LensSelected", [lens_id]);
                    $("#select_lens_dialog").dialog("close");
                    $("#select_lens_dialog").dialog("destroy");
                }
            }

        }
    ]
};
    
    

/*
open: function(){
    var uname = $.cookie('username');
    if (uname){
        $("#username").val(uname);
        $('.ui-dialog-buttonpane button:last').focus();
    }
    var ds = $.cookie('ds');
    if (ds){$("#sel_datasource").val(ds).trigger("liszt:updated");}
},
buttons: [
    {
        text: "Delete defaults",
        click: function(){
            $("#username").val('');
            $.removeCookie('username');
            $.removeCookie('ds');
        }
    },
    {
        text: "Save defaults",
        click: function(){
            $.cookie('username', $("#username").val(), { expires: 365 });
            $.cookie('ds', $("#sel_datasource").val(), { expires: 365 });
        }
    },
    {
        text: "Ok",
        click: function(evt){
            var val = $("#sel_datasource").val();
            if (!val){
                alert("Please choose one datasource to continue");
                return;
            }
            else {
                var uname = $("#username").val();
                LMT.settings.username = uname;
                self.dialog("close");
                $.event.trigger("GetDatasourceDialog", [id = val, uname = uname]);
            }
        }

    },
    ]
}
*/