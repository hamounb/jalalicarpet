# Generated by Django 4.2 on 2024-10-23 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CityModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییرات')),
                ('name', models.CharField(max_length=100, verbose_name='نام شهر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'شهر',
                'verbose_name_plural': 'شهرها',
            },
        ),
        migrations.CreateModel(
            name='ContactUsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, verbose_name='نام کامل')),
                ('phone', models.CharField(max_length=100, verbose_name='شماره یا ایمیل')),
                ('subject', models.CharField(blank=True, max_length=100, null=True, verbose_name='موضوع')),
                ('message', models.TextField(verbose_name='پیام')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
            ],
            options={
                'verbose_name': 'پیام',
                'verbose_name_plural': 'پیام\u200cها',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='VideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییرات')),
                ('src', models.CharField(max_length=300, verbose_name='لینک')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ویدئو',
                'verbose_name_plural': 'ویدئوها',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='PosterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییرات')),
                ('image', models.ImageField(upload_to=store.models.get_cover_path, verbose_name='تصویر پوستر')),
                ('pre_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='پیش عنوان')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان اصلی')),
                ('animation', models.BooleanField(default=False, verbose_name='انیمیشن')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پوستر سایت',
                'verbose_name_plural': 'پوسترهای سایت',
            },
        ),
        migrations.CreateModel(
            name='OnSalePosterModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییرات')),
                ('subject', models.CharField(max_length=100, verbose_name='موضوع')),
                ('image', models.ImageField(upload_to=store.models.get_cover_path, verbose_name='تصویر پوستر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پوستر فروش ویژه',
                'verbose_name_plural': 'پوسترهای فروش ویژه',
            },
        ),
        migrations.CreateModel(
            name='ExibitionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییرات')),
                ('title', models.CharField(max_length=50, verbose_name='عنوان')),
                ('start_date', models.DateField(verbose_name='تاریخ شروع')),
                ('end_date', models.DateField(verbose_name='تاریخ اتمام')),
                ('cover', models.ImageField(blank=True, null=True, upload_to=store.models.get_cover_path, verbose_name='تصویر کاور')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jcompany.citymodel', verbose_name='نام شهر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نمایشگاه',
                'verbose_name_plural': 'نمایشگاه\u200cها',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='CustomerVideoModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('modified_date', models.DateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییرات')),
                ('src', models.CharField(max_length=300, verbose_name='لینک')),
                ('title', models.CharField(max_length=250, verbose_name='عنوان')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'ویدئو مشتریان',
                'verbose_name_plural': 'ویدئوهای مشتریان',
                'ordering': ['-created_date'],
            },
        ),
    ]
