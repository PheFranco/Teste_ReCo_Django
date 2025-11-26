from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('chats/', views.inbox, name='chats'),
    path('nova/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/contato/', views.contact_donor, name='contact'),
    path('<int:pk>/chat/', views.chat, name='chat'),
    path('<int:pk>/chat/messages/', views.messages_json, name='messages_json'),
    path('<int:pk>/chat/post/', views.post_message, name='post_message'),
]
