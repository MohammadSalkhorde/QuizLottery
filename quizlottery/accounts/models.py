from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.utils import timezone
from utils import UploadFile
import uuid
#===========================================================================================================
class CustomUserManager(BaseUserManager):
    def create_user(self,mobile_number,name='',family='',email='',active_code=None,gender=None,password=None):
        if not mobile_number:
            raise('لطفا شماره موبایل را وارد کنید')
        
        user=self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_superuser(self,mobile_number,name,family,email='',password=None,active_code=None,gender=None):
        user=self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password
        )
        user.is_active=True
        user.is_admin=True
        user.is_superuser=True
        
        user.save(using=self._db)
        return user
#===========================================================================================================
def generate_unique_public_id():
    return uuid.uuid4().hex[:8]
#===========================================================================================================
class CustomUser(AbstractBaseUser,PermissionsMixin):
    mobile_number=models.CharField(max_length=11,verbose_name='شماره تلفن',unique=True)
    name=models.CharField(max_length=50,verbose_name='نام',blank=True)
    family=models.CharField(max_length=50,verbose_name='نام خانوادگی',blank=True)
    email=models.EmailField(max_length=200,verbose_name='ایمیل',blank=True)
    GENDER_CHOICES=(('True','مرد'),('False','زن'))
    gender=models.CharField(max_length=50,choices=GENDER_CHOICES,default="True",null=True,blank=True,verbose_name='جنسیت')
    file_upload=UploadFile('images','customuser')
    image_name=models.ImageField(upload_to=file_upload.upload_to,null=True,blank=True,verbose_name='عکس پروفایل')
    register_date=models.DateField(default=timezone.now,verbose_name='تاریخ ثبت نام')
    is_active=models.BooleanField(default=False,verbose_name='وضعیت')
    active_code=models.CharField(max_length=100,verbose_name='کد فعالسازی',null=True,blank=True)
    is_admin=models.BooleanField(default=False,verbose_name='ادمین')
    last_login=models.DateTimeField(auto_now=True,verbose_name='تاریخ اخرین ورود')
    cover_upload=UploadFile('images','cover')
    cover_image=models.ImageField(upload_to=cover_upload.upload_to,null=True,blank=True,verbose_name='کاور پروفایل')
    national_id=models.CharField(max_length=18,verbose_name='کد ملی',null=True,blank=True)
    national_id_image_file = UploadFile('images', 'national_id')
    national_id_image = models.ImageField(upload_to=national_id_image_file.upload_to, verbose_name="عکس کارت ملی", null=True, blank=True)

    
    objects=CustomUserManager()
    
    USERNAME_FIELD='mobile_number'
    REQUIRED_FIELDS=['name','family']
    
    def __str__(self):
        return f'{self.name} {self.family}'
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name='کاربر'
        verbose_name_plural='کاربران'
#===========================================================================================================
