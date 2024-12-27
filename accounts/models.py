from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from jalali_date import datetime2jalali
from store.models import ProductModel
from django.core.validators import MinValueValidator

# Create your models here.

def is_number(value):
    if not str(value).isnumeric():
        raise ValidationError('لطفا فقط عدد وارد نمایید!')
    

class BaseModel(models.Model):
    created_date = models.DateTimeField(verbose_name='تاریخ ایجاد', auto_now_add=True)
    modified_date = models.DateTimeField(verbose_name='تاریخ آخرین تغییرات', auto_now=True)

    class Meta:
        abstract = True


class TokenModel(BaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT, verbose_name='کاربر')
    token = models.CharField(verbose_name="رمزیکبارمصرف", max_length=6)
    status = models.CharField(verbose_name="وضعیت", max_length=100)
    recid = models.CharField(verbose_name="شماره پیگیری", max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["-created_date"]
        verbose_name = "رمز یکبارمصرف"
        verbose_name_plural = "رمزهای یکبارمصرف"

    def __str__(self):
        return f"{self.user.username} - {self.token}"


class AddressModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر')
    country = models.CharField(verbose_name="کشور", max_length=50)
    province = models.CharField(verbose_name="استان", max_length=50)
    city = models.CharField(verbose_name="شهر", max_length=50)
    postal_code = models.CharField(verbose_name="کد پستی", max_length=50)
    address = models.TextField(verbose_name="آدرس", null=True, blank=True)

    class Meta:
        verbose_name = "آدرس"
        verbose_name_plural = "آدرس‌ها"

    def __str__(self):
        return f"{self.user.username} - {self.country},{self.province},{self.city},{self.postal_code}"
    

class InvoiceModel(BaseModel):
    STATE_WAIT = 'wait'
    STATE_ACCEPT = 'accept'
    STATE_DEPOSIT = 'deposit'
    STATE_CHOICES = (
        (STATE_WAIT, 'در انتظار پرداخت'),
        (STATE_ACCEPT, 'پرداخت شده'),
        (STATE_DEPOSIT, 'پیش پرداخت')
    )
    is_active = models.BooleanField(verbose_name="فعال", default=True)
    user = models.ForeignKey(User, verbose_name="کاربر", on_delete=models.PROTECT)
    state = models.CharField(verbose_name='وضعیت', max_length=50, choices=STATE_CHOICES, default=STATE_WAIT)
    total_price = models.CharField(verbose_name='مبلغ کل', max_length=12, validators=[is_number])
    address = models.TextField(verbose_name="آدرس", null=True, blank=True)
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)
    
    class Meta:
        ordering = ["-created_date"]
        verbose_name = "فاکتور"
        verbose_name_plural = "فاکتورها"

    def __str__(self):
        if self.state == self.STATE_ACCEPT:
            return f"{self.pk}--پرداخت شده--{self.total_price}--{datetime2jalali(self.created_date).strftime('%Y/%m/%d')}"
        elif self.state == self.STATE_DEPOSIT:
            return f"{self.pk}--پیش پرداخت--{self.total_price}--{datetime2jalali(self.created_date).strftime('%Y/%m/%d')}"
        else:
            return f"{self.pk}--درانتظار پرداخت--{self.total_price}--{datetime2jalali(self.created_date).strftime('%Y/%m/%d')}"


class InvoiceItemModel(BaseModel):
    invoice = models.ForeignKey(InvoiceModel, verbose_name="فاکتور", on_delete=models.CASCADE)
    # product = models.ForeignKey(ProductModel, verbose_name="محصول", on_delete=models.SET_DEFAULT, default="وجود ندارد")
    code = models.CharField(verbose_name="کد محصول", max_length=50)
    price = models.CharField(verbose_name="قیمت", max_length=12, validators=[is_number])
    description = models.TextField(verbose_name='توضیحات', null=True, blank=True)

    def __str__(self):
        if self.invoice.state == self.invoice.STATE_ACCEPT:
            return f"{self.invoice.pk}--پرداخت شده--{self.invoice.user.username} ({self.code})"
        elif self.invoice.state == self.invoice.STATE_DEPOSIT:
            return f"{self.invoice.pk}--پیش پرداخت--{self.invoice.user.username} ({self.code})"
        else:
            return f"{self.invoice.pk}--در انتظار پرداخت--{self.invoice.user.username} ({self.code})"
    
    class Meta:
        ordering = ["-created_date","invoice"]
        verbose_name = "اقلام فاکتور"
        verbose_name_plural = "اقلام فاکتورها"


# class PaymentModel(models.Model):
#     STATE_WAIT = 'wait'
#     STATE_DEPOSIT = 'deposit'
#     STATE_PAID = 'paid'
#     STATE_CHOICES = (
#         (STATE_WAIT, "در انتظار پرداخت"),
#         (STATE_DEPOSIT, "پیش پرداخت"),
#         (STATE_PAID, "پرداخت شده"),
#     )
#     state = models.CharField(verbose_name='وضعیت', max_length=50, choices=STATE_CHOICES, default=STATE_WAIT)
#     invoice = models.ForeignKey(InvoiceModel, verbose_name="فاکتور", on_delete=models.SET_NULL, null=True, blank=True)
#     amount = models.IntegerField(verbose_name="مبلغ", validators=[MinValueValidator(0)])
#     authority = models.CharField(verbose_name="شناسه مرجع", max_length=36, null=True, blank=True)
#     status = models.IntegerField(verbose_name="کد وضعیت", default=0)
#     refid = models.IntegerField(verbose_name="شماره تراکنش خرید", default=0)
#     mobile = models.CharField(verbose_name="شماره تماس خریدار", max_length=11, null=True, blank=True)
#     email = models.CharField(verbose_name="ایمیل خریدار", max_length=100, null=True, blank=True)
#     description = models.CharField(verbose_name="توضیحات", max_length=150, null=True, blank=True)
#     created_date = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    
#     class Meta:
#         ordering = ["-created_date"]
#         verbose_name = "فیش پرداخت"
#         verbose_name_plural = "فیش‌های پرداخت"

#     def __str__(self):
#         if self.invoice.state == self.invoice.STATE_ACCEPT:
#             return f"[{self.invoice.pk}]{self.invoice.user.username}--پرداخت شده--({self.refid})"
#         elif self.invoice.state == self.invoice.STATE_DEPOSIT:
#             return f"[{self.invoice.pk}]{self.invoice.user.username}--پرداخت نشده--({self.refid})"
#         else:
#             return f"[{self.invoice.pk}]{self.invoice.user.username}--در انتظار پرداخت--({self.refid})"