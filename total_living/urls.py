"""
URL configuration for total_living project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.db.models import Count, Q

# Vista mejorada para la página principal
def home_view(request):
    """Vista mejorada para la página principal con estadísticas"""
    from properties.models import Property
    
    # Propiedades destacadas
    featured_properties = Property.objects.filter(
        status='disponible',
        is_featured=True
    ).order_by('-created_at')[:6]
    
    # Últimas propiedades
    latest_properties = Property.objects.filter(
        status='disponible'
    ).order_by('-created_at')[:6]
    
    # Estadísticas
    total_properties = Property.objects.filter(status='disponible').count()
    cities_count = Property.objects.filter(status='disponible').values('city').distinct().count()
    
    # Tipos más comunes
    property_types_stats = Property.objects.filter(
        status='disponible'
    ).values('property_type').annotate(
        count=Count('id')
    ).order_by('-count')[:4]
    
    context = {
        'featured_properties': featured_properties,
        'latest_properties': latest_properties,
        'total_properties': total_properties,
        'cities_count': cities_count,
        'property_types_stats': property_types_stats,
    }
    
    return render(request, 'home.html', context)

# URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
]

# Agregar más URLs
urlpatterns.append(path('properties/', include('properties.urls')))
urlpatterns.append(path('contact/', include('contact.urls')))
urlpatterns.append(path('search/', include('search.urls')))
urlpatterns.append(path('accounts/', include('accounts.urls')))
urlpatterns.append(path('panel/', include('panel.urls')))
urlpatterns.append(path('desarrollos/', include('developments.urls')))
urlpatterns.append(path('regiones/', include('regions.urls')))

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
