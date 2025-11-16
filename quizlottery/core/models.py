from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from utils import UploadFile

class Comments(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='کاربر',related_name='comment_user')
    text=models.TextField(verbose_name='متن نظر')
    register_date=models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ثبت نظر')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    
    def __str__(self):
        return f'{self.user} {self.text}'
    
    class Meta:
        verbose_name='نظر'
        verbose_name_plural='نظر ها'
    
class Timer(models.Model):
    title=models.CharField(max_length=100,verbose_name='عنوان تایمر')
    start_time=models.DateTimeField(default=timezone.now,verbose_name='تاریخ شروع')
    end_time=models.DateTimeField(default=timezone.now,verbose_name='تاریخ پایان')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    
    def __str__(self):
        return f'{self.title} {self.start_time} {self.end_time}'
    
    class Meta:
        verbose_name='تایمر'
        verbose_name_plural='تایمر ها'
        
class Org(models.Model):
    title=models.CharField(max_length=100,verbose_name='عنوان/نام')
    description=models.TextField(verbose_name='توضیحات',null=True,blank=True)
    image_upload=UploadFile('images','org')
    image=models.ImageField(verbose_name='عکس',upload_to=image_upload.upload_to,null=True,blank=True)
    phone=models.CharField(max_length=15,verbose_name='شماره موبایل',null=True,blank=True)
    address=models.TextField(verbose_name='ادرس',null=True,blank=True)
    link=models.URLField(max_length=200,verbose_name='لینک',null=True,blank=True)
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    
    def __str__(self):
        return f'{self.title} {self.is_active}'
    
    class Meta:
        verbose_name='ارگان'
        verbose_name_plural='ارگان ها'
        