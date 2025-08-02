from django.urls import path

from app_category import views

app_name = 'app_category'

urlpatterns = [
    path('list/',views.CategoryList.as_view(),name='category-list'),
    path('detail/',views.CategoryDetail.as_view(),name='category-detail'),
    path('add/',views.CategoryAdd.as_view(),name='category-add')
]