from django.urls import path
from . import views

app_name = 'panel'

urlpatterns = [
    path('login/', views.panel_login, name='login'),
    path('logout/', views.panel_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('propiedades/', views.panel_properties, name='properties'),
    path('propiedades/editar/<int:pk>/', views.panel_property_edit, name='property_edit'),
    path('propiedades/eliminar/<int:pk>/', views.panel_property_delete, name='property_delete'),
    # Carrusel
    path('carrusel/', views.panel_carousel_list, name='carousel_list'),
    path('carrusel/agregar/', views.panel_carousel_add, name='carousel_add'),
    path('carrusel/editar/<int:pk>/', views.panel_carousel_edit, name='carousel_edit'),
    path('carrusel/eliminar/<int:pk>/', views.panel_carousel_delete, name='carousel_delete'),
]
