# Generated by Django 2.2.2 on 2019-06-23 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_item_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
