from django.db import models
from django.contrib.auth import get_user_model

from app_category.models import CategoryModel

User = get_user_model()

class Unit(models.TextChoices):
    KG = 'kg', 'Kg'
    DONA = 'dona', 'Dona'

class ProductModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="products")
    image = models.ImageField(upload_to="products/",null=True,blank=True)
    name = models.CharField(max_length=255,unique=True)
    price = models.DecimalField(max_digits=15,decimal_places=2)
    count = models.BigIntegerField()
    category = models.ManyToManyField(CategoryModel,related_name="products")
    unity = models.CharField(
        max_length=5,
        choices=Unit.choices,
        default=Unit.DONA)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
    


