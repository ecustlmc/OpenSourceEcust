from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings
# Create your models here.

report_tag = (
    ("1","日常汇报"),
    ("2","每周PPT"),
    ("3","文章分享"),
)

class Report(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name="发表时间")
    title = models.CharField(max_length=100,verbose_name="标题",default="无标题")
    content = models.TextField(verbose_name="正文")
    tag = models.CharField(verbose_name="类型",max_length=2,choices=report_tag,default="1")
    def getUsername(self):
        return self.user.first_name
    def getFileList(self):
        return ReportFile.objects.filter(report=self)
    def getLikeCounter(self):
        return len(ReportLikes.objects.filter(report=self,like=1))
    def getCommentList(self):
        return ReportComments.objects.filter(report=self).order_by("-time")

def user_dir_path(instance,filename):
    if os.name == "nt":
        return os.path.join(settings.MEDIA_ROOT,"app_report",instance.report.user.username, 'doc', filename)
    return os.path.join("app_report",instance.report.user.username,'doc',filename)

class ReportFile(models.Model):
    report = models.ForeignKey(Report,on_delete=models.CASCADE)
    file = models.FileField(upload_to=user_dir_path,verbose_name="文件名")

class ReportLikes(models.Model):
    report = models.ForeignKey(Report,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.SmallIntegerField(choices=(("已赞",1),("未赞",0)),default=0)

class ReportComments(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    report = models.ForeignKey(Report,on_delete=models.CASCADE)
    comment = models.TextField()
    time = models.DateTimeField()
    def getUsername(self):
        return self.user.username


#class like_counter_cache(models.Model):
#    report = models.ForeignKey(Report,on_delete=models.CASCADE)
#    counter = models.IntegerField(default=0)
#