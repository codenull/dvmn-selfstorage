# Generated by Django 3.2.9 on 2021-11-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventory',
            name='picture',
            field=models.ImageField(upload_to='iventory/', verbose_name='изображение инвентаря'),
        ),
        migrations.AlterField(
            model_name='storage',
            name='picture',
            field=models.ImageField(upload_to='storage/', verbose_name='изображение'),
        ),
    ]