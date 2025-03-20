from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class essay(models.Model):
    student=models.ForeignKey(User,on_delete=models.CASCADE,db_column='student_id',default=1)
    title=models.CharField(max_length=255)
    content=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title