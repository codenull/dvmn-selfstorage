# Generated by Django 3.2.9 on 2021-11-18 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='birthday',
            field=models.DateField(null=True, verbose_name='Дата рождения'),
        ),
    ]
