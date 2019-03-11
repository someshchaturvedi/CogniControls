var csrftoken = $.cookie('csrftoken');
var t;

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function refresh_table() {
    t = $('#table_controls2').DataTable({
        "columnDefs": [
            { className: "cell", "targets": [ 0, 1, 2, 3, 4, 5, 6 ] },
     ]}
    );
    $.ajax({
        type: "GET",
        url: "/controls2_data/",
        success: function(result) {
            result = result['results'];
            console.log(result)
            console.log(result);
            if(result.length > 0){
                for (var i = 0; i < result.length; i++) {
                    type = 'non-acco'
                    if(result[i]['amount'] == 2047){
                        type = 'acco';
                    }

                    kit_issued = '<input type="checkbox" id="kit_issued_' + result[i]["checkin_id"] + '"></input>'
                    if(result[i]['kit_issued'] == true){
                        kit_issued = '<input type="checkbox" id="kit_issued_' + result[i]["checkin_id"] + '" checked disabled></input>'
                    }
                    id_issued = '<input type="checkbox" id="id_issued_' + result[i]["checkin_id"] + '"></input>'
                    if(result[i]['id_issued'] == true){
                        id_issued = '<input type="checkbox" id="id_issued_' + result[i]["checkin_id"] + '" checked disabled></input>'
                    }
                    t.row.add( [
                        result[i]['cogni_id'],
                        result[i]['checkin_id'],
                        type,
                        result[i]['name'],
                        result[i]['college'],
                        kit_issued,
                        id_issued,
                        '<button id="allot_' + result[i]["checkin_id"] +'" onclick="allot(this)" >Allot</button>',

                    ] ).draw( false );
                }
            }

        },
        error: function(result) {
            alert(result['message']);
        }
    });
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function allot(e) {
    checkin_id = e['id'].split('_')[1];
    if($('#id_issued_' + String(checkin_id)).is(":checked") == false){
        alert("Cant make an entry without issuing ID card");
        return;
    }
    else{
        data = {
            "checkin_id": checkin_id,
            "id_issued": true,
            "kit_issued": $('#kit_issued_' + String(checkin_id)).is(":checked")
        };
        $.ajax({
            type: "POST",
            url: "/controls2_allot/",
            data: data,
            success: function(result) {
                t.clear();
                t.destroy();
                refresh_table();
            },
            error: function(result) {
                alert(result['message']);
            }
        });
    }
}


$(document).ready(function(){
    refresh_table();
});
