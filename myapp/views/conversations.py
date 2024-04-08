from django.http import JsonResponse
from django.views.decorators.http import require_POST
from myapp.models import Conversation

@require_POST
def delete_conversation(request, guid):
    if request.method == 'POST':
        response_data = {'status': 'failed', 'message': 'Invalid request'}
        try:
            conversation = Conversation.objects.get(guid=guid)
            conversation.delete()
            response_data = {'status': 'success', 'message': 'Conversation deleted successfully'}
        except Conversation.DoesNotExist:
            response_data = {'status': 'failed', 'message': 'Conversation not found'}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'status': 'failed', 'message': 'Invalid request method'})
    
@require_POST
def delete_all_conversation(request):
    Conversation.objects.all().delete()
    return JsonResponse({'status': 'success', 'message': 'All conversations deleted successfully'})
    