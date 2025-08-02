from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator

from app_category.models import CategoryModel


class CategoryList(View):
    def get(self, request):
        user = request.user
        categories = user.categories.all()
        search_query = request.GET.get('category-search', '')

        if search_query:
            categories = categories.filter(name__icontains=search_query)
        
        paginator = Paginator(categories, 15)
        page_number = request.GET.get('category-page')
        page_obj = paginator.get_page(page_number)
        
        context = {"categories": page_obj}
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'category/_categories-table.html', context)

        return render(request, 'category/categories-table.html', context)


class CategoryDetail(View):
    def get(self,request):
        return render(request,'category/category-detail.html')
    
class CategoryAdd(View):
    def get(self, request):
        return render(request, 'category/categories-add.html')

    def post(self, request):
        nomlar = request.POST.getlist('nomlar[]')
        success_count = 0

        mahsulotlar_soni = len(nomlar)
        for i in range(mahsulotlar_soni):
            try:                
                CategoryModel.objects.create(
                    user=request.user,
                    name=nomlar[i]
                )
                success_count +=1
                
            except Exception as e:
                messages.error(request, f"{i+1}-kategoriya qo‘shishda xatolik: {str(e)}")

        if success_count > 0:
            messages.success(request, f"{success_count} ta kategoriya muvaffaqiyatli qo‘shildi!")

        return redirect('app_category:category-add')  # O'zingizga mos yo'nalishga

    