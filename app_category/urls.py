from django.urls import path

from app_category import views

app_name = 'app_category'

urlpatterns = [
    path('list/',views.CategoryListView.as_view(),name='category-list'),
    path('detail/<int:pk>/',views.CategoryDetail.as_view(),name='category-detail'),
    path('add/',views.CategoryAddView.as_view(),name='category-add'),
    path('delete/<int:pk>/',views.CategoryDeleteView.as_view(),name="category-delete"),
]