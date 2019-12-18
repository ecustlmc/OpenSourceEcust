from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user = models.ForeignKey(User,verbose_name="用户",on_delete=models.CASCADE)
    name = models.CharField(max_length=50,verbose_name="姓名")

class Message(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="发表时间")
    title = models.CharField(max_length=100,verbose_name="标题")
    text = models.TextField(verbose_name="正文")
