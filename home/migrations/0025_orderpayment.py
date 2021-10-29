# Generated by Django 3.0.9 on 2021-05-20 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0024_auto_20210515_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(default=0)),
                ('type', models.CharField(blank=True, choices=[('Click', 'Click'), ('PayMe', 'PayMe')], max_length=50, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Yaratildi'), (2, "To'landi"), (3, 'Bekor qilindi')], default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Users')),
            ],
        ),
    ]
