from django.utils import timezone
from datetime import timedelta
from django.shortcuts import redirect
from django.contrib.auth import logout
from app_order.models import OrderModel
from django.db.models import Max

class OrderCleanupMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated:
            # Eng oxirgi orderini olish
            last_order = (
                OrderModel.objects.filter(user=user)
                .order_by('-created_at')  # created_at maydon nomini o'zingga moslashtir
                .first()
            )

            if last_order:
                # 4 oydan eski bo'lgan barcha orderlarni o'chirish (eng oxirgisidan tashqari)
                four_months_ago = timezone.now() - timedelta(days=120)
                OrderModel.objects.filter(
                    user=user,
                    created_at__lt=four_months_ago
                ).exclude(id=last_order.id).delete()

        return self.get_response(request)
