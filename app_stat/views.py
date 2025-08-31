from datetime import timedelta,datetime

from django.shortcuts import render
from django.views import View
from django.db.models import Sum,F
from collections import defaultdict
from django.contrib.auth.mixins import LoginRequiredMixin


from app_order.models import OrderModel
from app_product.models import ProductModel

from datetime import datetime
import pytz

# Toshkent timezone
tashkent_tz = pytz.timezone("Asia/Tashkent")

# Hozirgi vaqt Toshkent bo‘yicha
now_in_tashkent = datetime.now(tashkent_tz)

# Bugungi sana (har kuni o‘zgaradi, Toshkent bo‘yicha)
today_date = now_in_tashkent.date()

week_ago = today_date - timedelta(days=7)
month_ago = today_date - timedelta(days=30)
month_ago_3 = today_date - timedelta(days=90)


class StatView(LoginRequiredMixin,View):
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
        product_all_count = ProductModel.objects.filter(user=request.user).count()
        # Kam qolgan mahsulotlar 
        product_less_count = ProductModel.objects.filter(
            count__lte=10,user=request.user
        ).count()
        # Tugab qolgan mahsulotlar 
        product_not_count = ProductModel.objects.filter(
            count=0,user=request.user
        ).count()

        # Top 5 eng ko‘p sotilgan mahsulotlar
        product_sell_top = (
        OrderModel.objects
        .filter(user=request.user)
        .values('product__name', 'product__unity')
        .annotate(total_sold=Sum('count'))
        .order_by('-total_sold')[:5]
    )

        # Kategoriya bo‘yicha top 5 sotuv (umumiy summa bo‘yicha)
        category_sell_top = OrderModel.objects.filter(user=request.user).values('product__category__name').annotate(
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
    

class DateStatView(LoginRequiredMixin,View):
    def get(self, request):
        context = {
            "today_date": today_date,
            "orders": None,
            "error": None
        }
        return render(request, "stat/date-stat.html", context)

    def post(self, request):
        date = request.POST.get("date")
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except (ValueError, TypeError):
            context = {
                "orders": None,
                "error": "❌ Noto‘g‘ri sana formati. Iltimos, YYYY-MM-DD formatda kiriting!",
                "today_date": today_date
            }
            return render(request, "stat/date-stat.html", context)

        orders = OrderModel.objects.filter(created_at__date=date_obj, user=request.user)
        # Mahsulot nomi bo‘yicha guruhlab, count va price ni yig‘amiz
        grouped_orders = defaultdict(lambda: {'count': 0, 'price': 0, 'unity': '', 'product': None})

        for order in orders:
            product_name = order.product.name
            grouped_orders[product_name]['count'] += order.count
            grouped_orders[product_name]['price'] += order.price
            grouped_orders[product_name]['unity'] = order.product.unity
            grouped_orders[product_name]['product'] = order.product

        if orders.exists():
            total_price = orders.aggregate(total=Sum('price'))['total'] or 0
            context = {
                "grouped_orders": dict(grouped_orders),
                "total_price": total_price,
                "selected_date": date_obj,
                "today_date": today_date,
                "error": None
            }
        else:
            context = {
                "orders": None,
                "error": "Bu sanada ma'lumotlar mavjud emas!",
                "selected_date": date_obj,
                "today_date": today_date
            }

        return render(request, "stat/date-stat.html", context)
    

class StatDiagrammaView(LoginRequiredMixin,View):
    def get(self, request):

        # 7 kunlik
        sales_7 = []
        labels_7 = []
        for i in range(7):
            day = today_date - timedelta(days=6 - i)
            total = OrderModel.objects.filter(
                created_at__date=day,
                user=request.user
            ).aggregate(sum=Sum('price'))['sum'] or 0
            sales_7.append(int(total))
            labels_7.append(day.strftime('%d-%b'))

        # 30 kunlik
        sales_30 = []
        labels_30 = []
        for i in range(30):
            day = today_date - timedelta(days=29 - i)
            total = OrderModel.objects.filter(
                created_at__date=day,
                user=request.user
            ).aggregate(sum=Sum('price'))['sum'] or 0
            sales_30.append(int(total))
            labels_30.append(day.strftime('%d-%b'))

        # 3 oylik (oylar bo‘yicha)
        sales_3_months = []
        labels_3_months = []
        for i in range(3):
            month_start = (today_date.replace(day=1) - timedelta(days=30*i)).replace(day=1)
            month_end = (month_start + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            total = OrderModel.objects.filter(
                created_at__date__range=(month_start, month_end),
                user=request.user
            ).aggregate(sum=Sum('price'))['sum'] or 0
            sales_3_months.insert(0, int(total))  # eng eski chapda bo'lishi uchun
            labels_3_months.insert(0, month_start.strftime('%B'))  # Oy nomi

        context = {
            'sales_7_days': sales_7,
            'labels_7_days': labels_7,
            'sales_30_days': sales_30,
            'labels_30_days': labels_30,
            'sales_3_months': sales_3_months,
            'labels_3_months': labels_3_months,
        }

        return render(request, 'stat/diagramma.html', context)
