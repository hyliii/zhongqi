# Generated by Django 2.0.6 on 2019-05-25 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('modelapp', '0007_remove_address_book_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
