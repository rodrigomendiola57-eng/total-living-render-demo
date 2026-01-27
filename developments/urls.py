from django.urls import path
from . import views

app_name = 'developments'

urlpatterns = [
    path('', views.developments_list, name='list'),
    path('<int:pk>/', views.development_detail, name='detail'),
    path('panel/', views.panel_developments, name='panel_list'),
    path('panel/add/', views.panel_development_add, name='panel_add'),
    path('panel/<int:pk>/edit/', views.panel_development_edit, name='panel_edit'),
    path('panel/<int:pk>/delete/', views.panel_development_delete, name='panel_delete'),
    path('panel/<int:pk>/images/', views.panel_development_images, name='panel_images'),
]
