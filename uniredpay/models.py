from django.db import models

from home.models import Users, Course


class PercentageOfSpeaker(models.Model):
    from_own_staff = models.SmallIntegerField(default=90)
    from_user = models.SmallIntegerField(default=70)


class PayForBalance(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=0)
    card_mask = models.CharField(max_length=20, default=None, null=True)
    payment_id = models.PositiveIntegerField()
    uu_id = models.CharField(max_length=50, null=True, default=None, blank=True)
    date = models.DateTimeField(auto_now_add=True)


class UserSms(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    sms_code = models.PositiveIntegerField()
    card_number = models.CharField(max_length=20)
    card_expire = models.CharField(max_length=10)
    amount = models.PositiveIntegerField()
