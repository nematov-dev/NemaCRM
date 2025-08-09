from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages

from app_product.models import ProductModel

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

        cart = request.session.get("cart", {})
        total_quantity = len(cart) 
        context = {
            'products': page_obj,
            'categories':categories,
            'total_quantity':total_quantity
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'dashboard/_dashboard.html', context)

        return render(request, 'dashboard/dashboard.html', context)
    
class AddCartView(LoginRequiredMixin,View):
    def post(self, request, product_id):
        cart = request.session.get("cart", {})
        count = int(request.POST.get('count', 1))
        next_url = request.POST.get('next', '/')

        try:
            product = ProductModel.objects.get(id=product_id, user=request.user)
        except ProductModel.DoesNotExist:
            messages.error(request, "❌ Mahsulot topilmadi.")
            return redirect(next_url)

        current_quantity_in_cart = cart.get(str(product_id), 0)
        total_requested = current_quantity_in_cart + count

        if total_requested > product.count:
            messages.error(
                request,
                f"❌ {product.name} mahsulotidan faqat {product.count} dona mavjud. Siz jami {total_requested} dona qo‘shmoqchisiz."
            )
        else:
            cart[str(product_id)] = total_requested
            request.session["cart"] = cart
            messages.success(request, f"Mahsulotdan {count} ta savatga qo‘shildi.")

        return redirect(next_url)
    
        
    
class CartView(LoginRequiredMixin,View):
    def get(self,request):
        cart = request.session.get("cart", {})
        cart_items = []
        total_price = 0

        for product_id, quantity in cart.items():
            try:
                product = ProductModel.objects.get(id=product_id,user=request.user)
            
                if product.image and hasattr(product.image, 'url'):
                    image_url = product.image.url
                else:
                    image_url = None  # yoki default rasm yo‘li
                
                total_price += product.price * quantity

                cart_items.append({
                    'product': product,
                    'quantity': quantity,
                    'total_price': product.price * quantity,
                    'image': image_url,
                })

            except ProductModel.DoesNotExist:
                continue
        paginator = Paginator(cart_items, 10)
        page_number = request.GET.get('cart-page')
        page_obj = paginator.get_page(page_number)

        context = {'cart_items': page_obj,'total_price':total_price}

        return render(request, 'dashboard/cart.html',context)
    
class CartClearView(LoginRequiredMixin,View):
    def post(self,request):
        request.session.pop("cart",None)
        return redirect('app_dashboard:dashboard')
    
class CartProductCancel(LoginRequiredMixin,View):
    def post(self, request, pk):
        cart = request.session.get("cart", {})
        pk_str = str(pk)
        if pk_str in cart:
            cart.pop(pk_str)
            request.session["cart"] = cart  # sessiyani yangilab qo‘yamiz
        return redirect("app_dashboard:cart-list")