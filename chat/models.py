from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

# Create your models here.

class ChatRoom(models.Model):
    name = models.CharField(max_length=255)
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(User, related_name='chat_rooms')
    def __str__(self):
        return self.name

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    reactions = GenericRelation('Reaction')
    
    def __str__(self):
        return f"{self.sender} at {self.timestamp}: {self.content[:50]}"

class Reply(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    reactions = GenericRelation('Reaction')
    
    def __str__(self):
        return f"Reply by {self.sender} at {self.timestamp}: {self.content[:50]}"

class Reaction(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction = models.CharField(max_length=50)
    
    class Meta:
        unique_together = ('content_type', 'object_id', 'user', 'reaction')

    def __str__(self):
        return f"Reaction by {self.user} on {self.content_object} : {self.reaction}"
