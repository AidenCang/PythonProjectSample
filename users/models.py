from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserProfile(AbstractUser):
    username = models.CharField(max_length=30, null=True, blank=True, unique=True, verbose_name=u'用户名', help_text='用户名')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    gender = models.CharField(max_length=6, choices=(('male', '男'), ('female', '女')), verbose_name=u'性别')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'电话号码', help_text='电话号码')
    email = models.EmailField(max_length=100, null=True, blank=True, verbose_name=u'邮箱', help_text='邮箱')

    # add_time = models.DateTimeField(datetime.now)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    # def save(self, *args, **kwargs):
    #     self.userID = self.get_increment_number()

    def __str__(self):
        return self.name


class VerifyCode(models.Model):
    # 邮件和短信验证
    code = models.CharField(max_length=4, verbose_name='验证码')
    mobile = models.CharField(max_length=50, verbose_name="电话号码")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
