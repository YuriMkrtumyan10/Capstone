$(document).ready(function() {
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        var user_input = $('#message-input').val();

        if (user_input) {
            $('#message-input').val('');
            $.post('/soc/send-message', {
                'user_input': user_input,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'type': $('#type').val()
            }).done((res) => {
                $('.messages').html(res); // Update chat box with response
               // scrollToBottom();

                let guid = $('#guid').value()
                
                var currentUrl = window.location.href;

                var urlParts = currentUrl.split('/');
                var parameterValue = urlParts[urlParts.length - 1];

                // Check if the parameter value matches your variable
                if (parameterValue !== guid) {
                    // Replace the parameter value in the URL with your desired value
                    var newUrl = currentUrl.replace(parameterValue, guid);
                    
                    // Redirect to the new URL
                    window.location.href = newUrl;
                }
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
   // scrollToBottom();
    

    // $('.agent').submit(function(event) {
    //     event.preventDefault();
    //     changeAgent();
    // });

    // function changeAgent() {
        
    //     document.addEventListener('DOMContentLoaded', (event) => {
    //         // Select all elements with the class 'agent'
    //         const agents = document.querySelectorAll('.agent');
        
    //         agents.forEach((agent, index) => {
    //             // Add a click event listener to each agent
    //             agent.addEventListener('click', function() {
    //                 // Change the URL hash based on the agent index
    //                 // Increment index by 1 to start counting from 1 instead of 0
    //                 window.location.hash = 'agent' + (index + 1);
    //             });
    //         });
    //     });
    // }
    function copyCode() {
        var codeBlock = $(this).next("pre");
        var text = codeBlock.text();

        navigator.clipboard.writeText(text)
            .then(() => {
                alert("Code copied to clipboard!");
            })
            .catch(err => {
                console.error('Failed to copy: ', err);
            });
    }

    // Attach click event to all copy buttons
    $('.copy-btn').on('click', copyCode);
});