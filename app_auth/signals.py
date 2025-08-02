from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from app_auth.models import ProfileModel

User = get_user_model()

# Signal: Foydalanuvchi yaratilganda unga profil yaratish
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user=instance)
