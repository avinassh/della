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
                if (data.status) {
                    update_thread(data=data.data);
                }
                else {
                    console.log('ajax was successful... but')
                    console.log(data.data)
                }
            },
            error: function(data) {
                console.log("error");
                console.log(data);
            }
        });
        return false;
    });

    function update_thread(data) {
        var sampleMessageBox = $(".sample-message-block").children()
        var messageBox = sampleMessageBox.clone();
        messageBox.find('.message-body').text(data.text)
        messageBox.find('.text-muted').text(data.signature)
        messageBox.find('.sender-avatar').attr('src', data.avatar)

        // add this to UI
        $(".media-list").append(messageBox)
        // clear text box from form
        $("form").trigger('reset');
    }

});