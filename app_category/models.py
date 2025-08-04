from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryModel(models.Model):
    name = models.CharField(max_length=255,unique=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="categories")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"