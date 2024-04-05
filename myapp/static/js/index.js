$(document).ready(function() {
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        sendMessage();
    });

    function sendMessage() {
        var user_input = $('#message-input').val();
        if (user_input) {
            $('#message-input').val('');
            var fileInput = $('#file-upload')[0].files[0];

            var formData = new FormData();

            formData.append('file_upload', fileInput);

            formData.append('user_input', user_input);
            formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
            formData.append('type', $('#type').val());
            formData.append('guid', $('#guid').val());

            $.ajax({
                url: '/send-message',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function(res) {
                    $('.messages').html(res); // Update chat box with response
                   // scrollToBottom();
    
                    let guid = $('#guid').val()
                    
                    var currentUrl = window.location.href;
                    var urlParts = currentUrl.split('/');
                    var parameterValue = urlParts[urlParts.length - 2];
    
                    if (parameterValue !== guid) {
                        window.location.href = guid;
                    }
                },
                error: function(xhr, status, status) {
                    console.error("Request failed: " + status + ", " + status);
                }
            });
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

    
    // function deleteConversation(guid, agentType) {
    //     const csrftoken = getCookie('csrftoken');
    
    //     fetch(`/delete-conversation/${guid}/`, {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'X-CSRFToken': csrftoken,
    //         },
    //         body: JSON.stringify({'guid': guid})
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if(data.status === 'success') {
    //             window.location.href = `/${agentType}/`;
    //         } else {
    //             alert(data.message);
    //         }
    //     });
    // }

    $('.remove-conversation').on('click', function() {
        if (confirm('Are you sure?')) {
            $.post(
                '/delete-conversation/' + $(this).closest('.convo').data('guid'), {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),                
            }).done((res) => {
                window.location = '/' + $(this).closest('.conversations').data('conversations-for');
            });
        }
    });

    $('body').on('click', '.toggle_conversations', function() {
        $(this).next().toggle();
    });

    $('.toggle_conversations.active').click();

    // $('.agent_button').click(function(event) {
    //     event.preventDefault();
    //     var agentType = $(this).data('agent');
    //     window.location.href = `/${agentType}/`;
    // });
    
    // $('body').on('click', '.clear_conversations', function() {
    //     event.preventDefault();
    //     console.log('Clear conversation button clicked');
    //     clearConversations();
    // });

    // function clearConversations() {
    //     console.log('Entered - conversation button clicked');
    //     fetch('/clear-conversations/', {
    //         method: 'POST',
    //         headers: {
    //             'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').value
    //         }
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         if (data.status === 'success') {
    //             alert('All conversations deleted successfully');
    //             // Optionally, you can reload the page after deleting conversations
    //             location.reload();
    //         } else {
    //             alert('Failed to delete conversations');
    //         }
    //     })
    //     .catch(error => {
    //         console.error('Error:', error);
    //         alert('An error occurred while deleting conversations');
    //     });
    // }


    // function getClassFromFragment() {
    //     return window.location.hash.substring(1); // Exclude the '#' symbol
    // }

    // // Get the class from the URL fragment
    // var className = getClassFromFragment();

    // // Check if the class exists in the document
    // var divWithClass = document.querySelector('.' + className);
    // if (divWithClass) {
    //     // Scroll to the div
    //     divWithClass.scrollIntoView();
    // } else {
    //     console.error('Div with class', className, 'not found');
    // }
});