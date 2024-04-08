from django.urls import path
from .views.conversations import delete_all_conversation, delete_conversation
from .views.messages import send_message
from .views.chat import main, agent
from .views.test import test

urlpatterns = [
    # path('', views.welcome, name='Welcome'),
    path('test/', test, name='main'),
    path('main/', main, name='main'),
    path('main/<str:guid>/', main, name='bot_with_guid'),
    path('send-message', send_message, name='sendMessage'),
    path('delete-conversation/<str:guid>', delete_conversation, name='deleteConversation'),
    path('delete-all-conversations', delete_all_conversation, name='deleteAllConversations'),
    path('<str:type>/', agent, name='soc_with_param'),
    path('<str:type>/<str:guid>', agent, name='soc_with_param'),

]