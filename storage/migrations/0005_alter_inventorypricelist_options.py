# Generated by Django 3.2.9 on 2021-11-20 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_alter_town_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inventorypricelist',
            options={'verbose_name': 'инвентарь для хранения - цена', 'verbose_name_plural': 'прайс по инвентарю'},
        ),
    ]