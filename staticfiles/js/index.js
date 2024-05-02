function textAreaAdjust(element) {
    element.style.height = "1px";
    element.style.height = (10+element.scrollHeight) - 7 +"px";
}


function copyCode(button) {
    // Get the <code> element containing the text
    const code = button.previousElementSibling.querySelector('code');
    // Create a temporary textarea element to copy the text
    const textarea = document.createElement('textarea');
    textarea.textContent = code.textContent;
    document.body.appendChild(textarea);
    textarea.select(); // Select the text
    document.execCommand('copy'); // Copy the selected text
    document.body.removeChild(textarea); // Remove the temporary element
    // Optionally, display a message or change the button text
    button.textContent = 'Copied!';
    setTimeout(() => { button.textContent = 'Copy'; }, 2000);
}
$(document).ready(function() {

    $('pre code').each(function() {
        hljs.highlightElement(this);
    });

    $('#chat-form').submit(function(event) {
        event.preventDefault();
        sendMessage();
    });
    $('#file-upload').on('change', function(e){
        var file = e.target.files[0];
        var fileDiv = $('.uploaded-file-temp').clone().removeClass('uploaded-file-temp').addClass('uploaded-file');
        fileDiv.prependTo('.user-input');
        fileDiv.find('span').text(file.name);
        // $('.uploaded-file-temp').remove(); 
    });
    
    $(document).on('click', '.delete-file', function() {
        clearInputFile($("#file-upload"));
        $(this).parent().remove();
    });

    function clearInputFile(input) {
        if (input.val()) {
          try {
            input.val('');
          } catch (err) {}
          if (input.val()) {
            var form = $('<form></form>'),
              ref = input.next();
            form.append(input);
            form[0].reset();
            ref.before(input);
          }
        }
      }

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
        scrollToBottom();

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
                window.location = '/orchestrator';
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

    function scrollToBottom() {
        var chatContainer = $('.messages');
        chatContainer.css('overflow', 'hidden')
        chatContainer.scrollTop(chatContainer.prop("scrollHeight"));
        chatContainer.css('overflow', 'auto')
    }

    scrollToBottom();

    // document.getElementById('file-upload').addEventListener('change', function() {
    //     var formContent = document.getElementById('form-content');
    //     if (this.files && this.files.length > 0) {
    //         formContent.classList.add('file-selected');
    //     } else {
    //         formContent.classList.remove('file-selected');
    //     }
    // });

    
});
