from django.urls import path
from django.shortcuts import redirect
from .views import PrivateChatList, GroupChatList, SearchPrivateChat, SearchGroupChat, create_group_chat, create_private_chat, show_group_messages, show_private_messages
from .views import send_group_message, send_private_message, reply_group_message

urlpatterns = [
    path('', lambda request: redirect('private_chat_list'), name='chat_home'),
    path('private/', PrivateChatList, name='private_chat_list'),
    path('group/', GroupChatList, name='group_chat_list'),
    path('search/private/', SearchPrivateChat, name='search_private_chat'),
    path('search/group/', SearchGroupChat, name='search_group_chat'),
    path('create/group/', create_group_chat, name='create_group_chat'),
    path('create/private/', create_private_chat, name='create_private_chat'),
    path('private-chat/<int:chat_id>/', show_private_messages, name='private_chat_messages'),
    path('group-chat/<int:chat_id>/', show_group_messages, name='group_chat_messages'),
    path('private-chat/<int:chat_id>/send/', send_private_message, name='send_private_message'),
    path('group-chat/<int:chat_id>/send/', send_group_message, name='send_group_message'),
    path('group-chat/<int:chat_id>/reply/<int:message_id>/', reply_group_message, name='reply_group_message'),
]
