from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from app_category.models import CategoryModel
from app_product.models import ProductModel
from app_product.forms import ProductEditForm

class ProductListView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        products = user.products.all()

        category_id = request.GET.get('category')  # ID keladi
        quantity_status = request.GET.get('quantity_status')  # 'yoq', 'kam', 'bor'
        search_query = request.GET.get('product-search')

        # Kategoriya bo‘yicha filter
        if category_id:
            products = products.filter(category__id=category_id)

        # Qidiruv filter
        if search_query:
            products = products.filter(name__icontains=search_query)

        # Quantity status bo‘yicha filter
        if quantity_status == 'yoq':
            products = products.filter(count=0)
        elif quantity_status == 'kam':
            products = products.filter(count__gt=0, count__lte=10)
        elif quantity_status == 'bor':
            products = products.filter(count__gt=10)
        
        categories = CategoryModel.objects.filter(user=user)

        paginator = Paginator(products, 15)
        page_number = request.GET.get('product-page')
        page_obj = paginator.get_page(page_number)

        context = {
            "products": page_obj,
            "categories": categories
        }

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # AJAX request bo‘lsa faqat jadval qismini qaytaramiz
            return render(request, 'product/_products-table.html', context)

        return render(request, 'product/products-table.html', context)

class ProductDetail(LoginRequiredMixin,View):
    def get(self,request,pk):
        product_edit_form = ProductEditForm()
        user = request.user
        product = user.products.get(id=pk)
        categories = CategoryModel.objects.filter(user=user)

        context = {"product":product,
                   "categories":categories,
                   "product_edit_form":product_edit_form
        }
        
        return render(request,'product/product-detail.html',context)
    
    def post(self, request, pk):
        product_edit_form = ProductEditForm(request.POST, request.FILES, user=request.user)
        context = {"product_edit_form": product_edit_form}
        
        if product_edit_form.is_valid():
            image = product_edit_form.cleaned_data["image"]
            name = product_edit_form.cleaned_data["name"]
            price = product_edit_form.cleaned_data["price"]
            unity = product_edit_form.cleaned_data["unity"]
            count = product_edit_form.cleaned_data["count"]
            categories = product_edit_form.cleaned_data["category"]

            product = get_object_or_404(request.user.products, id=pk)

            if image:
                product.image = image
            if name:
                product.name = name
            if price:
                product.price = price
            if unity:
                product.unity = unity
            if count:
                product.count = count
            if categories:
                product.category.set(categories)
            product.save()

            messages.success(request, "Mahsulot tahrirlandi!")
            return redirect("app_product:product-detail", pk=product.id)

        product_edit_form.add_error(None, "Formani to‘ldiring!")
        return render(request, 'product/product-detail.html', context)

class ProductAdd(View):
    def get(self, request):
        categories = CategoryModel.objects.filter(user=request.user)
        return render(request, 'product/products-add.html', {'categories': categories})

    def post(self, request):
        success_count = 0
        rasmlar = request.FILES.getlist('rasmlar[]')
        nomlar = request.POST.getlist('nomlar[]')
        narxlar = request.POST.getlist('narxlar[]')
        birliklar = request.POST.getlist('birliklar[]')
        miqdorlar = request.POST.getlist('miqdorlar[]')
        kategoriyalar = request.POST.getlist('kategoriyalar[]')

        mahsulotlar_soni = len(nomlar)
        for i in range(mahsulotlar_soni):
            try:
                kategoriya_id = kategoriyalar[i]

                # Avval tekshiramiz — agar yo‘q yoki bo‘sh bo‘lsa, None
                if not kategoriya_id or kategoriya_id == 'Tanlang':
                    kategoriya = None
                else:
                    kategoriya = CategoryModel.objects.get(id=int(kategoriya_id), user=request.user)
                
                # Rasm bo‘lsa olamiz, bo‘lmasa None
                rasm = rasmlar[i] if i < len(rasmlar) else None

                product = ProductModel.objects.create(
                    user=request.user,
                    image=rasm,
                    name=nomlar[i],
                    price=narxlar[i],
                    unity=birliklar[i],
                    count=miqdorlar[i],
                )
                if kategoriya:
                    product.category.set([kategoriya])  # ManyToManyField uchun to‘g‘ri usul

                success_count += 1

            except Exception as e:
                messages.error(request, f"{i+1}-mahsulotni qo‘shishda xatolik: {str(e)}")


        if success_count > 0:
            messages.success(request, f"{success_count} ta mahsulot muvaffaqiyatli qo‘shildi!")

        return redirect('app_product:product-add')  # O'zingizga mos yo'nalishga

class ProductDeleteView(View):
    def post(self, request, pk):
        product = get_object_or_404(ProductModel, user=request.user, id=pk)
        product.delete()
        return redirect('app_product:product-list')  # Sahifaga qaytish yo‘nalishi