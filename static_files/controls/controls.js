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
    t = $('#table').DataTable();
}
$(document).ready(function(){
    refresh_table();
    $("#btn_search").click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/search/",
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
                            result[i]['address'],
                            result[i]['contact'],
                            result[i]['college'],
                            result[i]['payment_id'],
                            result[i]['amount'],
                            result[i]['method'],
                            result[i]['type'],
                            result[i]['events']
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


    $("#btn_checkin").click(function(e) {
        if($('#id_verification_checkbox').is(":checked") == false || $('#noc_submission_checkbox').is(":checked") == false){
            alert('Please verify and ID and submit NOC');
            return;
        }

        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/controls1_submit/",
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
