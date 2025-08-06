from django.urls import path

from app_stat import views

app_name = 'app_stat'

urlpatterns = [
    path('',views.StatView.as_view(),name='stat'),
    path('date-stat/',views.DateStatView.as_view(),name='date-stat'),
    path('diagramma-stat/',views.StatDiagrammaView.as_view(),name="diagramma-stat")
]