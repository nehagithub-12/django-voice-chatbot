from django.urls import path
from . import views

urlpatterns = [
path('', views.chatbot_home, name='chatbot_home'),
path('response/', views.chat_response, name='chat_response'),
]
