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

                var success = function (data, status, xhr) {
                    response(data.data);
                };

                var fail = function (data, status, xhr) {
                };

                $.ajax('/lenses/api', {
                    type: "GET",
                    success: success,
                    error: fail,
                    data: data,
                    dataType: "json" //data type expected from server
                });

                return;
            },
/*
            change: function (event, ui) {

            },

            // Triggered before a search is performed, after minLength and delay.
            search: function (event, ui) {

            },
*/

            response: function (event, ui) {
                if (ui.content.length == 0) {
                    $("#select_lens_datasource").show();
                    $("#sele_ok").button("disable") ;
                    $("#sele_fetch").button("enable") ;
                }
                else {
                    $("#select_lens_datasource").hide();
                    $("#sele_ok").button("enable") ;
                    $("#sele_fetch").button("disable") ;
                }
            },
        });

        $("#select_lens_datasource").hide();
        $("#select_lens_status_text").html("");
    },

    buttons: [
        {
            text: "DC",
            click: function(){
                $("#username").val('');
                $.removeCookie('username');
                $.removeCookie('ds');
            }
        },
        {
            text: "SC",
            click: function(){
                $.cookie('username', $("#username").val(), { expires: 365 });
                $.cookie('ds', $("#sel_datasource").val(), { expires: 365 });
            }
        },
        {
            id: "sele_fetch",
            text: "Fetch",
            click: function(){
                $.cookie('username', $("#username").val(), { expires: 365 });
                $.cookie('ds', $("#sel_datasource").val(), { expires: 365 });
            }
        },
        {
            id: "sele_edit",
            text: "Edit",
            click: function(){
                $.cookie('username', $("#username").val(), { expires: 365 });
                $.cookie('ds', $("#sel_datasource").val(), { expires: 365 });
            }
        },
        {
            id: "sele_ok",
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