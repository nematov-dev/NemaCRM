from django.urls import path

from app_product import views

app_name = 'app_product'

urlpatterns = [
    path('list/',views.ProductListView.as_view(),name='product-list'),
    path('detail/<int:pk>/',views.ProductDetail.as_view(),name='product-detail'),
    path('add/',views.ProductAdd.as_view(),name='product-add'),
    path('delete/<int:pk>/',views.ProductDeleteView.as_view(),name="product-delete")

]