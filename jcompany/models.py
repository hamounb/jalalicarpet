from django.db import models
from django.contrib.auth.models import User
from store.models import get_cover_path
from django_ckeditor_5.fields import CKEditor5Field

# Create your models here.

class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ آخرین تغییرات', auto_now=True)

    class Meta:
        abstract = True


class PosterModel(BaseModel):
    image = models.ImageField(verbose_name="تصویر پوستر", upload_to=get_cover_path)
    pre_title = models.CharField(verbose_name="پیش عنوان", max_length=100, null=True, blank=True)
    title = models.CharField(verbose_name="عنوان اصلی", max_length=100, null=True, blank=True)
    animation = models.BooleanField(verbose_name="انیمیشن", default=False)

    class Meta:
        verbose_name = "پوستر سایت"
        verbose_name_plural = "پوسترهای سایت"

    def __str__(self):
        return self.title
    

class OnSalePosterModel(BaseModel):
    subject = models.CharField(verbose_name="موضوع", max_length=100)
    image = models.ImageField(verbose_name="تصویر پوستر", upload_to=get_cover_path)

    class Meta:
        verbose_name = "پوستر فروش ویژه"
        verbose_name_plural = "پوسترهای فروش ویژه"

    def __str__(self):
        return self.subject


class CityModel(BaseModel):
    name = models.CharField(verbose_name="نام شهر", max_length=100)

    class Meta:
        verbose_name = "شهر"
        verbose_name_plural = "شهرها"
    
    def __str__(self):
        return self.name


class ExibitionModel(BaseModel):
    city = models.ForeignKey(CityModel, on_delete=models.SET_NULL, verbose_name="نام شهر", null=True, blank=True)
    title = models.CharField(verbose_name="عنوان", max_length=50)
    start_date = models.DateField(verbose_name='تاریخ شروع')
    end_date = models.DateField(verbose_name='تاریخ اتمام')
    cover = models.ImageField(verbose_name="تصویر کاور", upload_to=get_cover_path, null=True, blank=True)

    class Meta:
        verbose_name = "نمایشگاه"
        verbose_name_plural = "نمایشگاه‌ها"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title}"


class ContactUsModel(models.Model):
    full_name = models.CharField(verbose_name="نام کامل", max_length=100)
    phone = models.CharField(verbose_name="شماره یا ایمیل", max_length=100)
    subject = models.CharField(verbose_name="موضوع", max_length=100, blank=True, null=True)
    message = models.TextField(verbose_name="پیام")
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.full_name}-({self.subject})"
        
        
class VideoModel(BaseModel):
    src = models.CharField(verbose_name="لینک", max_length=300)
    title = models.CharField(verbose_name="عنوان", max_length=250)

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئوها"
        ordering = ['-created_date']

    def __str__(self):
        return self.title
    

class CustomerVideoModel(BaseModel):
    src = models.CharField(verbose_name="لینک", max_length=300)
    title = models.CharField(verbose_name="عنوان", max_length=250)

    class Meta:
        verbose_name = "ویدئو مشتریان"
        verbose_name_plural = "ویدئوهای مشتریان"
        ordering = ['-created_date']

    def __str__(self):
        return self.title
    

class QuestionModel(BaseModel):
    available = models.BooleanField(verbose_name="فعال", default=True)
    question = models.CharField(verbose_name="سوال", max_length=250)
    answer = CKEditor5Field('متن بلاگ', config_name='extends')

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوالات متداول"
        ordering = ['-created_date']

    def __str__(self):
        if self.available:
            return f"{self.question} - (فعال)"
        return f"{self.question} - (غیرفعال)"