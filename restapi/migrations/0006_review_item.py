# Generated by Django 2.2.2 on 2019-06-24 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0005_remove_review_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='item',
            field=models.ManyToManyField(related_name='review', to='restapi.Item'),
        ),
    ]
