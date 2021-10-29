# Generated by Django 3.0.9 on 2021-10-19 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0040_auto_20211017_0201'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sms_code', models.PositiveIntegerField()),
                ('card_number', models.CharField(max_length=20)),
                ('card_expire', models.CharField(max_length=10)),
                ('amount', models.PositiveIntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Users')),
            ],
        ),
        migrations.CreateModel(
            name='PayForBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(default=0)),
                ('payment_id', models.PositiveIntegerField()),
                ('uu_id', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Users')),
            ],
        ),
    ]
