function textAreaAdjust(element) {
    element.style.height = "1px";
    element.style.height = (10+element.scrollHeight)+"px";
  }

$(document).ready(function() {
    $('#chat-form').submit(function(event) {
        event.preventDefault();
        sendMessage();
    });

    // $('#chat-form').keypress(function(event) {
    //     if (event.key === 'Enter') {
    //         sendMessage();
    //         event.preventDefault(); 
    //     }
    // });

    function sendMessage() {
        var userInput = $('#message-input').val();
        var fileInput = $('#file-upload')[0].files[0];
        if (userInput || fileInput) {
            $(".loading-message").show();
            $(".loading-message .message.user p").eq(1).text(userInput);
            debugger
            $('#message-input').val('');

            var formData = new FormData();

            formData.append('file_upload', fileInput);

            formData.append('user_input', userInput);
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
                    $('.messages').html(res); 
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

    $('.copy-btn').on('click', copyCode);

    $('.remove-conversation').on('click', function() {
        if ($(this).closest('#confirmationModal').attr('data-id')) {
            $.post(
                '/delete-conversation/' + $(this).closest('#confirmationModal').attr('data-id'), {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),                
            }).done((res) => {
                window.location = '/' + $(this).closest('#confirmationModal').attr('data-for');
            });
        } else {

            $.post('/delete-all-conversations', {
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val(),                
            }).done((res) => {
                window.location = '/main';
            });
        }
    });

    $('.remove-button').on('click', function() {
        let guid = $(this).closest('.convo').data('guid');
        $('#confirmationModal').attr('data-id', guid)
        $('#confirmationModal').attr('data-for', $(this).closest('.conversations').data('conversations-for'))
    })

    $('body').on('click', '.toggle_conversations', function() {
        $(this).next().toggle();
    });

    $('.toggle_conversations.active').click();
    
    $('.upload-image').on('click', function() {
        $('#file-upload').click();
    });

    document.getElementById('file-upload').addEventListener('change', function() {
        var formContent = document.getElementById('form-content');
        if (this.files && this.files.length > 0) {
            formContent.classList.add('file-selected');
        } else {
            formContent.classList.remove('file-selected');
        }
    });

    
});
