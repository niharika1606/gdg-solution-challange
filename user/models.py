from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    def __str__(self):
        return '{self.user.username}.Profile'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        