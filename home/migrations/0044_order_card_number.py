# Generated by Django 3.0.9 on 2021-12-13 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0043_auto_20211211_1431'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='card_number',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
