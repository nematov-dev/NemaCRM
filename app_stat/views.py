from datetime import date,timedelta,datetime

from django.shortcuts import render
from django.views import View
from django.db.models import Sum,Max,F

from app_order.models import OrderModel
from app_product.models import ProductModel

today_date = date.today()
week_ago = today_date - timedelta(days=7)
month_ago = today_date - timedelta(days=30)
month_ago_3 = today_date - timedelta(days=90)


class StatView(View):
    def get(self,request):
        # Foydalanuvchining bugungi buyurtmalari jami summasi
        total_price_today = OrderModel.objects.filter(
            created_at__date=today_date,
            user=request.user
        ).aggregate(total=Sum('price'))['total'] or 0

        # Oxirgi 7 kunlik buyurtmalar jami summasi
        total_price_week = OrderModel.objects.filter(
            created_at__date__gte=week_ago,
            created_at__date__lte=today_date,
            user=request.user
        ).aggregate(total=Sum('price'))['total'] or 0

        # Oxirgi 30 kunlik buyurtmalar jami summasi
        total_price_month = OrderModel.objects.filter(
            created_at__date__gte=month_ago,
            created_at__date__lte=week_ago,
            user=request.user
        ).aggregate(total=Sum('price'))['total'] or 0

        # Oxirgi 90 kunlik buyurtmalar jami summasi
        total_price_90days = OrderModel.objects.filter(
            created_at__date__gte=month_ago_3,
            created_at__date__lte=month_ago,
            user=request.user
        ).aggregate(total=Sum('price'))['total'] or 0

        # Barcha mahsulotlar soni
        product_all_count = ProductModel.objects.all().count()
        # Kam qolgan mahsulotlar 
        product_less_count = ProductModel.objects.filter(
            count__lte=10
        ).count()
        # Tugab qolgan mahsulotlar 
        product_not_count = ProductModel.objects.filter(
            count=0
        ).count()

        # Top 5 eng ko‘p sotilgan mahsulotlar
        product_sell_top = OrderModel.objects.values('product__name','product__unity').annotate(
            total_sold=Sum('count')
        ).order_by('-total_sold')[:5]


        # Kategoriya bo‘yicha top 5 sotuv (umumiy summa bo‘yicha)
        category_sell_top = OrderModel.objects.values('product__category__name').annotate(
            total_sales=Sum(F('count') * F('price'))
        ).order_by('-total_sales')[:5]

        context = {
            "total_price_today": total_price_today,
            "total_price_week":total_price_week,
            "total_price_month":total_price_month,
            "total_price_90days":total_price_90days,
            "product_all_count":product_all_count,
            "product_less_count":product_less_count,
            "product_not_count":product_not_count,
            "product_sell_top":product_sell_top,
            "category_sell_top":category_sell_top
        }
        return render(request,"stat/stat.html",context)
    
    # def post(self, request):
        date = request.POST.get("date")
        try:
            # Matndan date turiga o‘tkazish
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            # Noto‘g‘ri formatdagi sana kiritilsa
            context = {"orders": "❌ Noto‘g‘ri sana formati. Iltimos, YYYY-MM-DD formatda kiriting!"}
            return render(request, "stat/stat.html", context)

        # Shu sanadagi foydalanuvchining buyurtmalari
        orders = OrderModel.objects.filter(created_at__date=date_obj, user=request.user)

        if orders.exists():
            total_price = orders.aggregate(total=Sum('price'))['total'] or 0
            context = {
                "orders": orders,
                "total_price": total_price,
                "selected_date": date_obj  # Agar templateda sana ko‘rsatmoqchi bo‘lsangiz
            }
        else:
            context = {
                "orders": "Bu sanada ma'lumotlar mavjud emas!",
                "selected_date": date_obj
            }

        return render(request, "stat/stat.html", context)