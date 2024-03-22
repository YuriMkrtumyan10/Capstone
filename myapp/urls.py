from django.urls import path
from . import views

urlpatterns = [
    # path('', views.welcome, name='Welcome'),
    path('main/', views.main, name='main'),
    path('main/<str:guid>/', views.main, name='bot_with_guid'),
    path('<str:type>/', views.agent, name='soc_with_param'),
    path('<str:type>/<str:guid>', views.agent, name='soc_with_param'),
    path('send-message', views.send_message, name='sendMessage'),
    path('delete-conversation/<str:guid>/', views.delete_conversation, name='deleteConversation'),
]