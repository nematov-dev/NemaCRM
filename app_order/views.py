from django.shortcuts import redirect
from django.views import View

from app_product.models import ProductModel
from app_order.models import OrderModel

class ConfirmOrder(View):
    def post(self, request):
        cart = request.session.get("cart", {})
        for product_id, quantity in cart.items():
            try:
                product = ProductModel.objects.get(id=product_id, user=request.user)

                # Ombordan mahsulotni kamaytirish
                if product.count >= quantity:
                    product.count -= quantity
                    product.save()

                    price = quantity * product.price
                    OrderModel.objects.create(
                        user=request.user,
                        product=product,
                        count=quantity,
                        price=price
                    )

                # Agar yetarli mahsulot bo'lmasa - o‘tkazib yuboriladi
            except ProductModel.DoesNotExist:
                continue

        # Savatchani tozalash
        request.session.pop("cart", None)
        return redirect("app_dashboard:dashboard")

    
