from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator


class Dashboard(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        products = user.products.all()
        categories = user.categories.all()
        search_query = request.GET.get('dashboard-search', '')
        category_id = request.GET.get('category')

        if category_id:
            products = products.filter(category=category_id)
        
        if search_query:
            products = products.filter(name__icontains=search_query)

        # Sahifalash
        paginator = Paginator(products, 12)
        page_number = request.GET.get('dashboard-page')
        page_obj = paginator.get_page(page_number)

        context = {
            'products': page_obj,
            'categories':categories
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/_dashboard.html', context)

        return render(request, 'dashboard/dashboard.html', context)

class CartView(View):
    def get(self,request):
        return render(request,'dashboard/cart.html')