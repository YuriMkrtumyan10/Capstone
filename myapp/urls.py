from django.urls import path
from . import views

urlpatterns = [
    # path('', views.welcome, name='Welcome'),
    path('', views.soc, name='soc'),
    path('send-message', views.send_message, name='sendMessage'),
    path('<str:parameter>/', views.soc, name='soc_with_param'),
]