from ast import BinOp
from datetime import datetime
from tkinter import CASCADE
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from platformdirs import user_cache_dir
# Create your models here.
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(default = 'default.png', upload_to='profile_img')
    location = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.user.username


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_img')
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.now())
    no_of_likes = models.IntegerField(default=0)

    def __str__(self):
        return self.caption

class LikePost(models.Model):
    post_id = models.CharField(max_length=500)
    user_name = models.CharField(max_length=500)

    def __str__(self):
        return self.user_name