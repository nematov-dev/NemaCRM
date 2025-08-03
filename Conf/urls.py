from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/',include('app_dashboard.urls',namespace='app_dashboard')),
    path('product/',include('app_product.urls',namespace='app_product')),
    path('category/',include('app_category.urls',namespace='app_category')),
    # path('order/',include('app_order.urls',namespace='app_order')),
    path('stat/',include('app_stat.urls',namespace='app_stat')),
    path('auth/',include('app_auth.urls',namespace='app_auth')),
    path('',include('app_page.urls',namespace='app_page'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    