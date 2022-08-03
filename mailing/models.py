from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, MinLengthValidator
from pytz import all_timezones

TIMEZONES = tuple(zip(all_timezones, all_timezones))

class Mailing(models.Model):
    time_start = models.DateTimeField(blank=False, null=False)
    message_text = models.CharField(max_length=1024, blank=False, null=False)
    mobile_code = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100), MaxValueValidator(999)])
    tag = models.CharField(max_length=32, blank=True, null=True)
    time_end = models.DateTimeField(blank=False, null=False)

class Client(models.Model):
    phone_number = models.CharField(unique=True, blank=False, null=False, validators=[RegexValidator(r"\b7[0-9]{10}\b"), MinLengthValidator(11)], max_length=11)
    mobile_code = models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(100), MaxValueValidator(999)])
    tag = models.CharField(max_length=32, blank=True, null=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')

class Message(models.Model):
    time_sent = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(blank=True, null=True)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)