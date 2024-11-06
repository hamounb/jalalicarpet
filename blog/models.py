from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from store.models import get_cover_path
from django.contrib.auth.models import User

# Create your models here.

class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ آخرین تغییرات', auto_now=True)

    class Meta:
        abstract = True


class BlogCategoryModel(BaseModel):
    title = models.CharField(verbose_name="عنوان", max_length=100)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return f"{self.title}"


class BlogModel(BaseModel):
    category = models.ForeignKey(BlogCategoryModel, on_delete=models.SET_NULL, verbose_name='دسته‌بندی', null=True, blank=True)
    title = models.CharField(verbose_name="عنوان", max_length=100)
    content = CKEditor5Field('متن بلاگ', config_name='extends')
    cover = models.ImageField(verbose_name='تصویر کاور', upload_to=get_cover_path, null=True, blank=True)
    available = models.BooleanField(verbose_name='انتشار', default=True)
    visit = models.IntegerField(verbose_name="تعداد بازدید", default=0)

    class Meta:
        verbose_name = "بلاگ"
        verbose_name_plural = "بلاگ‌ها"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title}"
    

class BlogEnModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر')
    category = models.ForeignKey(BlogCategoryModel, on_delete=models.SET_NULL, verbose_name='دسته‌بندی', null=True, blank=True)
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ آخرین تغییرات', auto_now=True)
    title = models.CharField(verbose_name="عنوان به انگلیسی", max_length=100)
    content = CKEditor5Field('متن بلاگ به انگلیسی', config_name='extends')
    cover = models.ImageField(verbose_name='تصویر کاور', upload_to=get_cover_path, null=True, blank=True)
    available = models.BooleanField(verbose_name='انتشار', default=True)
    visit = models.IntegerField(verbose_name="تعداد بازدید", default=0)

    class Meta:
        verbose_name = "بلاگ انگلیسی"
        verbose_name_plural = "بلاگ‌های انگلیسی"
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.title}"