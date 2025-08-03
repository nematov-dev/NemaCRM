from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator

from app_category.models import CategoryModel
from app_category.forms import CategoryEditForm


class CategoryListView(View):
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
    def get(self,request,pk):
        category = get_object_or_404(CategoryModel,id=pk,user=request.user)

        context = {
            "category":category
        }
        return render(request,'category/category-detail.html',context)
    
    def post(self,request,pk):
        category_form = CategoryEditForm(request.POST)
        category = get_object_or_404(CategoryModel,id=pk,user=request.user)

        if category_form.is_valid():
            category_name = category_form.cleaned_data["name"]
            category.name = category_name
            category.save()
            messages.success(request, "Kategoriya tahrirlandi!")
            return redirect("app_category:category-detail", pk=category.id)
        
        category_form.add_error(None,"Formani to'ldiring!")
        return render(request,"category/category-detail.html",{"category_form":category_form})
    
class CategoryAddView(View):
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

class CategoryDeleteView(View):
    def post(self,request,pk):
        category = get_object_or_404(CategoryModel, user=request.user, id=pk)
        category.delete()
        messages.success(request,"Kategoriya o'chirildi")
        return redirect('app_category:category-list')  # Sahifaga qaytish yo‘nalishi
