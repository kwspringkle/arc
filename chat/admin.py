from django.contrib import admin
from .models import PrivateChatRoom, PrivateMessage, GroupChatRoom, GroupMessage

# Register your models here.
admin.site.register(PrivateChatRoom)
admin.site.register(PrivateMessage)
admin.site.register(GroupChatRoom)
admin.site.register(GroupMessage)