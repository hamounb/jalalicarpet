# Generated by Django 4.2 on 2024-12-24 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jcompany', '0003_footernewsmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='footernewsmodel',
            name='text',
            field=models.CharField(max_length=200, unique=True, verbose_name='موبایل یا ایمیل'),
        ),
    ]
