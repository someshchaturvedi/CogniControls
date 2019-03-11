var csrftoken = $.cookie('csrftoken');

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

$("#btn_login").click(function(e) {
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "/login/",
      data: {
        username: $("#username").val(),
        password: $("#password").val()
      },
      success: function(result) {
        alert(result);
      },
      error: function(result) {
        alert('error');
      }
    });
  });
