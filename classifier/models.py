from django.db import models
from utils.models import CreateUpdateTracker
from typing import Optional


class ClassificationRequest(CreateUpdateTracker):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="User")
    phone = models.CharField(max_length=64, unique=True, verbose_name="Phone Number")
    country = models.CharField(max_length=64, verbose_name="Country")
    telegram_age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Telegram Age")
    whatsapp_age = models.PositiveIntegerField(null=True, blank=True, verbose_name="Whatsapp Age")
    telegram_avatar_url = models.URLField(max_length=256, null=True, blank=True, verbose_name="Telegram Avatar URL")
    whatsapp_avatar_url = models.URLField(max_length=256, null=True, blank=True, verbose_name="Whatsapp Avatar URL")

    @property
    def average_age(self) -> Optional[int]:
        if self.telegram_age and self.whatsapp_age:
            return (self.telegram_age + self.whatsapp_age) / 2
        elif self.telegram_age:
            return self.telegram_age
        elif self.whatsapp_age:
            return self.whatsapp_age
        else:
            return None

    class Meta:
        verbose_name = "Request"
        verbose_name_plural = "Requests"

    def __str__(self):
        return f"{self.phone}"
