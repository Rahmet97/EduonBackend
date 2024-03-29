# Generated by Django 3.0.9 on 2021-12-11 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0043_auto_20211211_1431'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentHoldLimitTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.PositiveSmallIntegerField(default=3, verbose_name='Kun')),
            ],
            options={
                'verbose_name_plural': "Foydalanuvchilarga to'lovni qaytarish muddati",
            },
        ),
        migrations.CreateModel(
            name='PercentageOfSpeaker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_own_staff', models.SmallIntegerField(default=90)),
                ('from_user', models.SmallIntegerField(default=70)),
            ],
        ),
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
                ('card_mask', models.CharField(default=None, max_length=20, null=True)),
                ('tr_id', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Users')),
            ],
        ),
    ]
