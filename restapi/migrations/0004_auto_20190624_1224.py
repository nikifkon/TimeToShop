# Generated by Django 2.2.2 on 2019-06-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0003_auto_20190623_1256'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='item',
            field=models.ManyToManyField(related_name='review', to='restapi.Item'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(max_length=3000),
        ),
        migrations.AlterField(
            model_name='item',
            name='props',
            field=models.TextField(help_text='Possible properties of item like this - "Color: red", write a comma', max_length=1000),
        ),
    ]
