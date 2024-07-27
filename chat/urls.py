from django.urls import path, include
from . import views 

urlpatterns = [
    path('group_chats/', views.group_chat_list, name='group_chat_list'),
    path('private_chats/', views.private_chat_list, name='private_chat_list'),
    path('chat_room/<int:room_id>/', views.chat_room, name='chat_room'),
    path('create_group_chat/', views.create_group_chat, name='create_group_chat'),
    path('add_member/<int:room_id>/', views.add_member, name='add_member'),
    path('search_users/', views.search_users, name='search_users'),
    path('create_private_chat/', views.create_private_chat, name='create_private_chat'),
    path('get_messages/<int:room_id>/', views.get_messages, name='get_messages'),
    path('suggest/', views.suggest, name='suggest'),
]