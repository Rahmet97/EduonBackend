from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.PayForBalance)
admin.site.register(models.PercentageOfSpeaker)
admin.site.register(models.UserSms)
