from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

from app_product.models import ProductModel

class OrderModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE,related_name="orders")
    count = models.IntegerField()
    price = models.DecimalField(max_digits=15,decimal_places=0)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self) -> str:
        return self.user.username
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Order"
        verbose_name_plural = "Orders"
