$(document).ready(function() {
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        var user_input = $('#message-input').val();

        if (user_input) {
            $('#message-input').val('');
            $.post('/send-message', {
                'user_input': user_input,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),
                'type': $('#type').val(),
                'guid': $('#guid').val()
            }).done((res) => {
                $('.messages').html(res); // Update chat box with response
               // scrollToBottom();

                let guid = $('#guid').val()
                
                var currentUrl = window.location.href;
                var urlParts = currentUrl.split('/');
                var parameterValue = urlParts[urlParts.length - 2];

                // Check if the parameter value matches your variable
                if (parameterValue !== guid) {
                    // Replace the parameter value in the URL with your desired value
                    // var newUrl = currentUrl.replace(parameterValue, guid);
                    
                    // Redirect to the new URL
                    window.location.href = guid;
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



    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    
    function deleteConversation(guid, agentType) {
        const csrftoken = getCookie('csrftoken');
    
        fetch(`/delete-conversation/${guid}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({'guid': guid})
        })
        .then(response => response.json())
        .then(data => {
            if(data.status === 'success') {
                window.location.href = `/${agentType}/`;
            } else {
                alert(data.message);
            }
        });
    }

    $('body').on('click', 'i[data-guid]', function() {
        var guid = $(this).attr('data-guid');
        var agentType = $(this).data('agent');
        deleteConversation(guid, agentType);
    });

    // $('.agent_button').click(function(event) {
    //     event.preventDefault();
        
    //     var agentType = $(this).attr('data-agent');
        
    //     // Toggle the corresponding conversations
    //     var $conversations = $('[data-conversations-for="' + agentType + '"]');
    //     $conversations.slideToggle();
    
    //     // Change URL - navigate to the agent's page
    //     window.history.pushState(null, '', '/' + agentType + '/');
    // });


    $('body').on('click', '.toggle_conversations', function() {
        var agentType = $(this).data('agent');
        var $conversations = $('[data-conversations-for="' + agentType + '"]');
        $conversations.slideToggle();  
    });

    $('.agent_button').click(function(event) {
        event.preventDefault();
        var agentType = $(this).data('agent');
        window.location.href = `/${agentType}/`;
    });
    
});