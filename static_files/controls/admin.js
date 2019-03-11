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

$(document).ready(function(){
    $("#btn_sync").click(function(e) {
        e.preventDefault();
        $.ajax({
            type: "GET",
            url: "/sync_db/",
            success: function(result) {
                alert('done');
            },
            error: function(result) {
                alert(result['responseJSON']['message']);
            }
        });
    });
})
