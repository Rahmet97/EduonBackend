# Generated by Django 3.0.9 on 2021-08-18 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_phonecodespeaker'),
    ]

    operations = [
        migrations.AddField(
            model_name='speaker',
            name='gender',
            field=models.CharField(blank=True, choices=[('Erkak', 'Erkak'), ('Ayol', 'Ayol')], default=None, max_length=30, null=True),
        ),
    ]
