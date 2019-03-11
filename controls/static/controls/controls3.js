var csrftoken = $.cookie('csrftoken');
var t;

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function refresh_table(){
    t = $('#table3').DataTable();
}

$(document).ready(function(){
    refresh_table();
    $("#btn_search").click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/search3/",
            data: {
                cogni_id: $("#cogni_id").val(),
            },
            success: function(result) {
                result = result['results'];
                if(result.length > 0){
                    $(".show-on-data").css("visibility", "visible");
                    for (var i = 0; i < result.length; i++) {
                        t.row.add( [
                            result[i]['cogni_id'],
                            result[i]['name'],
                            result[i]['mobile'],
                            result[i]['college'],
                            result[i]['email'],
                            result[i]['gender'],
                            result[i]['controls1_at'],
                            result[i]['controls2_at'],
                        ] ).draw( false );
                    }
                }
                $(".show-on-data").css("display", "block");
            },
            error: function(result) {
                alert(result['responseJSON']['message']);
            }
        });
    });


    $("#btn_caution").click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/controls3_submit/",
            data: {
                cogni_id: $("#cogni_id").val(),
            },
            success: function(result) {
                $(".show-on-data").css("visibility", "hidden");
                $(".show-on-data").checked = false;
                t.clear();
                t.destroy();
                refresh_table();
                alert(result['message'])
            },
            error: function(result) {
                alert(result['responseJSON']['message']);
            }
        });
    });
})
