from django.urls import path
from . import views

urlpatterns = [
    # path('', views.welcome, name='Welcome'),
    path('', views.welcome, name='welcome'),
]