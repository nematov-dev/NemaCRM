from django.db import models


class NotificationModel(models.Model):
    title = models.CharField(max_length=256)
    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.message
    
    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"

class NemaCRMPhonePhotoModel(models.Model):
    image = models.ImageField(upload_to="nemacrm/telefon-lavhalar")

    class Meta:
        verbose_name = "Phone"
        verbose_name_plural = "Phones"

class NemaCRMPCPhotoModel(models.Model):
    image = models.ImageField(upload_to="nemacrm/pc-lavhalar")

    class Meta:
        verbose_name = "PC"
        verbose_name_plural = "PC"

