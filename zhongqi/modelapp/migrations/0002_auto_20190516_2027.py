# Generated by Django 2.0.6 on 2019-05-16 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='sales',
            field=models.IntegerField(),
        ),
    ]
