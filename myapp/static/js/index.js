$(document).ready(function() {
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        var user_input = $('#user_input').val();

        if (user_input) {
            $('#user_input').val('');
            $.post('/soc/send-message', {
                'user_input': user_input,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'type': $('#type').val()
            }).done((res) => {
                $('.messages').html(res); // Update chat box with response
                scrollToBottom();
            }).fail((jqXHR, textStatus, errorThrown) => {
                console.error("Request failed: " + textStatus + ", " + errorThrown);
            });;
        }
    }

    // Function to scroll chat container to the bottom
    function scrollToBottom() {
        var chatContainer = $('.messages');
        chatContainer.css('overflow', 'hidden')
        chatContainer.scrollTop(chatContainer.prop("scrollHeight"));
        chatContainer.css('overflow', 'auto')
    }

    // Initially scroll to the bottom when the page is loaded
    scrollToBottom();
    

});