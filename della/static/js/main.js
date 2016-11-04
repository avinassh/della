$(document).ready(function() {
    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    messageForm = $("form").first()

    messageForm.submit(function () {
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        });
        $.ajax({
            type: messageForm.attr('method'),
            url: messageForm.attr('action'),
            data: messageForm.serialize(),
            success: function (data) {
                console.log("success");
                console.log(data);
            },
            error: function(data) {
                console.log("error");
                console.log(data);
            }
        });
        return false;
    });
});