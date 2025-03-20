from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from PIL import Image

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    img=models.ImageField(default='default.jpg',upload_to='profile_pics')
    def __str__(self):
        return '{self.user.username}.Profile'
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        image=Image.open(self.img.path)
        if(image.height>300 or image.width>300):
            output_size=(300,300)
            image.thumbnail(output_size)
            image.save(self.img.path)