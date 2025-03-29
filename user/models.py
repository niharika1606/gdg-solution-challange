from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    positive = models.FloatField(default=0.0)
    neutral = models.FloatField(default=0.0)
    negative = models.FloatField(default=0.0)
    total_posts = models.IntegerField(default=0)
    def __str__(self):
        return '{self.user.username}.Profile'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
   
        