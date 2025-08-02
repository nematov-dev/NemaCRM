from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    image = models.ImageField(upload_to="avatar/",blank=True,null=True)
    phone = models.TextField(max_length=30,blank=True,null=True)

    subscription = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
