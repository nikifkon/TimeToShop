# Generated by Django 2.2.2 on 2019-06-24 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0004_auto_20190624_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='item',
        ),
    ]