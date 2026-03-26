"""
URL configuration for total_living project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.views.static import serve as static_serve
from django.utils.text import slugify
from django.db.utils import OperationalError, ProgrammingError
from panel.models import NosotrosContent


def _normalize_private_path(raw_value: str, default_path: str) -> str:
    """Normaliza rutas privadas para evitar errores de slash."""
    value = (raw_value or '').strip().strip('/')
    fallback = (default_path or '').strip().strip('/') or 'admin'
    return f'{value}/' if value else f'{fallback}/'

# Vista mejorada para la página principal
def home_view(request):
    """Vista mejorada para la página principal con estadísticas"""
    from properties.models import Property
    
    # Propiedades destacadas
    featured_properties = Property.objects.filter(
        status='disponible',
        is_featured=True
    ).prefetch_related('images').order_by('-created_at')[:6]
    
    # Últimas propiedades
    latest_properties = Property.objects.filter(
        status='disponible'
    ).prefetch_related('images').order_by('-created_at')[:9]

    # Mapa (solo propiedades con coordenadas registradas)
    map_props = Property.objects.filter(
        status='disponible',
        latitude__isnull=False,
        longitude__isnull=False
    ).only('id', 'title', 'latitude', 'longitude', 'price', 'currency')

    map_markers = []
    for p in map_props:
        map_markers.append({
            'id': p.pk,
            'title': p.title,
            'lat': float(p.latitude),
            'lng': float(p.longitude),
            'url': p.get_absolute_url(),
            'price': p.get_price_display(),
        })
    
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
        'map_markers': map_markers,
        'total_properties': total_properties,
        'cities_count': cities_count,
        'property_types_stats': property_types_stats,
    }
    
    return render(request, 'home.html', context)


def about_view(request):
    """Módulo institucional Nosotros."""
    User = get_user_model()
    team_members = User.objects.filter(
        is_staff=True,
        is_active=True
    ).order_by('first_name', 'last_name', 'username')

    director_photo = None
    manager_photo = None
    for member in team_members:
        full_name = f"{member.first_name} {member.last_name}".strip().lower()
        photo_field = getattr(member, 'profile_photo', None)
        photo_url = getattr(photo_field, 'url', None) if photo_field else None
        if not photo_url:
            continue
        if 'alfredo' in full_name and 'mendiola' in full_name:
            director_photo = photo_url
        if 'patricia' in full_name and ('chavarr' in full_name or 'chavarria' in full_name):
            manager_photo = photo_url

    try:
        nosotros_content, _ = NosotrosContent.objects.get_or_create(pk=1)
    except (OperationalError, ProgrammingError):
        # Evita 500 si todavía no se aplican migraciones del módulo panel.
        nosotros_content = NosotrosContent()

    context = {
        'team_members': team_members,
        'director_photo': director_photo,
        'manager_photo': manager_photo,
        'nosotros_content': nosotros_content,
    }
    return render(request, 'nosotros.html', context)


def team_member_detail_view(request, slug):
    """Perfil detallado de miembro del equipo."""
    User = get_user_model()
    normalized_slug = slugify(slug or '')

    static_profiles = {
        'alfredo-mendiola': {
            'full_name': 'Alfredo Mendiola',
            'role': 'Director General',
            'tag': 'Dirección estratégica',
            'bio': 'Lidera la visión de Total Living, define estándares de servicio y asegura que cada unidad comercial opere con procesos medibles y enfoque en resultados.',
            'expertise': [
                'Estrategia comercial y posicionamiento',
                'Estandarización de procesos',
                'Dirección de equipos de alto desempeño',
            ],
            'email': 'contacto@totalliving.com',
            'instagram': 'https://www.instagram.com/total.living.mx/',
            'facebook': 'https://www.facebook.com/total.living.mx?locale=es_LA',
            'photo_url': None,
        },
        'patricia-chavarria': {
            'full_name': 'Patricia Chavarría',
            'role': 'Gerente Comercial',
            'tag': 'Ventas y captación',
            'bio': 'Coordina el frente comercial, estructura estrategias de captación y supervisa la correcta ejecución de cada operación activa.',
            'expertise': [
                'Gestión de cartera activa',
                'Seguimiento comercial y cierres',
                'Estrategias de captación',
            ],
            'email': 'contacto@totalliving.com',
            'whatsapp': 'https://api.whatsapp.com/send?phone=4428669965',
            'photo_url': None,
        },
    }

    if normalized_slug in static_profiles:
        profile = static_profiles[normalized_slug]
    else:
        team_members = User.objects.filter(is_staff=True, is_active=True)
        selected_member = None
        for member in team_members:
            full_name = f"{member.first_name} {member.last_name}".strip() or member.username
            member_slug = slugify(full_name) or slugify(member.username)
            if member_slug == normalized_slug:
                selected_member = member
                break

        if not selected_member:
            return render(request, 'team_member_detail.html', {'profile': None}, status=404)

        photo_field = getattr(selected_member, 'profile_photo', None)
        profile = {
            'full_name': (f"{selected_member.first_name} {selected_member.last_name}".strip() or selected_member.username),
            'role': 'Asesor Inmobiliario',
            'tag': 'Compra, venta y renta',
            'bio': 'Acompaña al cliente en valuación, prospección y cierre, con foco en tiempos de respuesta y calidad de seguimiento.',
            'expertise': [
                'Prospección y filtrado de oportunidades',
                'Acompañamiento operativo de inicio a cierre',
                'Negociación y seguimiento comercial',
            ],
            'email': selected_member.email or 'contacto@totalliving.com',
            'photo_url': getattr(photo_field, 'url', None) if photo_field else None,
        }

    return render(request, 'team_member_detail.html', {'profile': profile})

# URL patterns
urlpatterns = [
    path(_normalize_private_path(settings.ADMIN_URL_PATH, 'admin'), admin.site.urls),
    path('', home_view, name='home'),
    path('nosotros/', about_view, name='about'),
    path('nosotros/equipo/<slug:slug>/', team_member_detail_view, name='team_member_detail'),
]

# Agregar más URLs
urlpatterns.append(path('properties/', include('properties.urls')))
urlpatterns.append(path('contact/', include('contact.urls')))
urlpatterns.append(path('search/', include('search.urls')))
urlpatterns.append(path('accounts/', include('accounts.urls')))
urlpatterns.append(path(_normalize_private_path(settings.PANEL_URL_PATH, 'panel'), include('panel.urls')))
urlpatterns.append(path('desarrollos/', include('developments.urls')))
urlpatterns.append(path('regiones/', include('regions.urls')))
urlpatterns.append(path('i18n/', include('django.conf.urls.i18n')))

# Servir MEDIA en desarrollo o en predeploy local (Docker) cuando se habilite.
if settings.DEBUG or getattr(settings, 'SERVE_LOCAL_MEDIA', False):
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', static_serve, {'document_root': settings.MEDIA_ROOT}),
    ]

# STATIC solo en DEBUG; en producción lo sirve WhiteNoise/S3.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
