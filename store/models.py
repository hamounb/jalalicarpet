from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import os 
from django.db.models.signals import post_delete 
from django.dispatch import receiver

# Create your models here.

def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    
def get_cover_path(obj, fn):
    path = datetime.now().strftime(f"product_covers/%Y/%m/%d/{fn}")
    return path

def get_image_path(obj, fn):
    path = datetime.now().strftime(f"product-images/%Y/%m/%d/{fn}")
    return path


class BaseModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر')
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ آخرین تغییرات', auto_now=True)

    class Meta:
        abstract = True


class CategoryModel(BaseModel):
    CARPET = "carpet"
    WALLCARPET = "wallcarpet"
    KILIM = "kilim"
    C_CHOICES = (
        (CARPET, "فرش دستبافت"),
        (WALLCARPET, "تابلو‌فرش دستبافت"),
        (KILIM, "فرش‌های سنتی")
    )
    number = models.IntegerField(verbose_name="ترتیب نمایش", default=0)
    title = models.CharField(verbose_name="نام دسته‌بندی", max_length=50)
    title_en = models.CharField(verbose_name="نام انگلیسی دسته‌بندی", max_length=50, null=True, blank=True)
    primary_cat = models.CharField(verbose_name="دسته اصلی", max_length=50, choices=C_CHOICES, default=CARPET)
    cover = models.ImageField(verbose_name="تصویر کاور", upload_to=get_cover_path, null=True, blank=True)

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return f"{self.title}"


class DesignPatternModel(BaseModel):
    name = models.CharField(verbose_name="نقشه", max_length=50)
    name_en = models.CharField(verbose_name="نقشه به انگلیسی", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "نقشه"
        verbose_name_plural = "نقشه‌ها"

    def __str__(self):
        return self.name


class TagsModel(BaseModel):
    name = models.CharField(verbose_name="نام برچسب", max_length=100)
    name_en = models.CharField(verbose_name="نام برچسب به انگلیسی", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "برچسب"
        verbose_name_plural = "برچسب‌ها"

    def __str__(self):
        return self.name


class TextureModel(BaseModel):
    name = models.CharField(verbose_name="بافت", max_length=50)
    name_en = models.CharField(verbose_name="بافت به انگلیسی", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "بافت"
        verbose_name_plural = "بافت‌ها"

    def __str__(self):
        return self.name


class WateModel(BaseModel):
    name = models.CharField(verbose_name="رج", max_length=3)
    name_en = models.CharField(verbose_name="رج به انگلیسی", max_length=3, null=True, blank=True)

    class Meta:
        verbose_name = "رج"
        verbose_name_plural = "رج‌ها"

    def __str__(self):
        return self.name
    

class PileModel(BaseModel):
    name = models.CharField(verbose_name="چله", max_length=100)
    name_en = models.CharField(verbose_name="چله به انگلیسی", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "چله"
        verbose_name_plural = "چله‌ها‌"

    def __str__(self):
        return self.name


class ProductModel(BaseModel):
    category = models.ForeignKey(CategoryModel, on_delete=models.SET_NULL, verbose_name="دسته‌بندی", null=True, blank=True)
    available = models.BooleanField(verbose_name="موجود در انبار", default=True)
    name = models.CharField(verbose_name="نام مدل", max_length=150)
    name_en = models.CharField(verbose_name="نام مدل به انگلیسی", max_length=150, null=True, blank=True)
    code = models.CharField(verbose_name="کد فرش", max_length=20, unique=True)
    price = models.CharField(verbose_name="قیمت", max_length=15, null=True, blank=True, validators=[is_number])
    on_sale = models.CharField(verbose_name="قیمت باتخفیف",max_length=15, null=True, blank=True, validators=[is_number])
    price_in = models.CharField(verbose_name="قیمت اقساطی", max_length=15, null=True, blank=True, validators=[is_number])
    price_d = models.CharField(verbose_name="قیمت به دلار", max_length=15, null=True, blank=True)
    width = models.DecimalField(verbose_name="اندازه عرض(متر)", decimal_places=2, max_digits=10)
    length = models.DecimalField(verbose_name="اندازه طول(متر)", decimal_places=2, max_digits=10)
    width_p = models.DecimalField(verbose_name="اندازه عرض جفت(متر)", decimal_places=2, max_digits=10, default=0)
    length_p = models.DecimalField(verbose_name="اندازه طول جفت(متر)", decimal_places=2, max_digits=10, default=0)
    texture = models.ForeignKey(TextureModel, on_delete=models.SET_NULL,verbose_name="بافت", null=True, blank=True)
    wate = models.ForeignKey(WateModel, on_delete=models.SET_NULL, verbose_name="رج", null=True, blank=True)
    pattern = models.ForeignKey(DesignPatternModel, on_delete=models.SET_NULL, verbose_name="نقشه", null=True, blank=True)
    pile = models.ForeignKey(PileModel, on_delete=models.SET_NULL, verbose_name="چله", null=True, blank=True)
    tags = models.ManyToManyField(TagsModel, verbose_name="برچسب‌ها", blank=True)
    short_description = models.TextField(verbose_name="توضیحات کوتاه", null=True, blank=True)
    short_description_en = models.TextField(verbose_name="توضیحات انگلیسی", null=True, blank=True)
    cover = models.ImageField(verbose_name="تصویر کاور", upload_to=get_cover_path, null=True, blank=True)
    visit = models.IntegerField(verbose_name="تعداد بازدید", default=0)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return f"{self.name}-{str(self.code)}"
    
    def delete(self, *args, **kwargs):
        if self.cover and os.path.isfile(self.cover.path): 
            if os.path.isfile(self.cover.path): 
                os.remove(self.cover.path)
        super(ProductModel, self).delete(*args, **kwargs)


class ProductImageModel(models.Model):
    name = models.ForeignKey(ProductModel, on_delete=models.CASCADE, verbose_name="نام مدل")
    images = models.ImageField(verbose_name="تصویر محصول", upload_to=get_image_path)
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)

    class Meta:
        verbose_name = "تصاویر محصول"
        verbose_name_plural = "تصاویر محصولات"
    
    def __str__(self):
        return self.name.code
    
    def delete(self, *args, **kwargs):
        if self.images and os.path.isfile(self.images.path): 
            if os.path.isfile(self.images.path): 
                os.remove(self.images.path)
        super(ProductImageModel, self).delete(*args, **kwargs)


@receiver(post_delete, sender=ProductImageModel)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.images and os.path.isfile(instance.images.path):
        os.remove(instance.images.path)