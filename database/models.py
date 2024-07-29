from django.db import models

# Create your models here.

class User (models.Model):
    username = models.CharField(max_length=50)
    nickname = models.CharField(max_length=50)
    icon     = models.ImageField(upload_to="media")
    email    = models.EmailField(max_length=254, unique=True)
    log_date = models.DateTimeField(auto_now=True)
    log_state= models.BooleanField(default=False)

    def __str__(self):
        return self.nickname
