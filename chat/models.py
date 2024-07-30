from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class PrivateChatRoom(models.Model):
    member1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_chat_member1")
    member2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="private_chat_member2")
    class Meta:
        unique_together = ('member1', 'member2')

    def __str__(self):
        return f"{self.member1.username} and {self.member2.username}"
    
class GroupChatRoom(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User)
    def __str__(self):
        return self.name
    
class PrivateMessage(models.Model):
    private_chat_room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    img_file = models.FileField(upload_to='private_chat_files/', null=True, blank=True)
    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.content[:10]}"
    
class GroupMessage(models.Model):
    group_chat_room = models.ForeignKey(GroupChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    img_file = models.FileField(upload_to='group_chat_files/', null=True, blank=True)
    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.content[:10]}"
    
class Reply(models.Model):
    message = models.ForeignKey(GroupMessage, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    img_file = models.FileField(upload_to='group_chat_files/', null=True, blank=True)
    def __str__(self):
        return f"Reply by {self.sender} at {self.timestamp}: {self.content[:10]}"


