from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from .models import Property, PropertyImage, PropertyFeature
from .forms import PropertyForm, PropertyImageForm


def property_list(request):
    """Vista para listar todas las propiedades"""
    from properties.models import PropertyType, PropertyOperation
    
    # Obtener todas las propiedades disponibles
    properties = Property.objects.filter(status='disponible').order_by('-created_at')
    
    # Filtros básicos
    property_type = request.GET.get('tipo', '')
    operation_type = request.GET.get('operacion', '')
    state = request.GET.get('estado', '')
    city = request.GET.get('ciudad', '')  # Mantener para compatibilidad
    region = request.GET.get('region', '')
    
    # Filtros avanzados
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    recamaras = request.GET.get('recamaras', '')
    banos = request.GET.get('banos', '')
    medios_banos = request.GET.get('medios_banos', '')
    estacionamiento = request.GET.get('estacionamiento', '')
    area_min = request.GET.get('area_min', '')
    area_max = request.GET.get('area_max', '')
    area_construccion_min = request.GET.get('area_construccion_min', '')
    area_construccion_max = request.GET.get('area_construccion_max', '')
    area_terreno_min = request.GET.get('area_terreno_min', '')
    area_terreno_max = request.GET.get('area_terreno_max', '')
    niveles = request.GET.get('niveles', '')
    year_built_min = request.GET.get('year_built_min', '')
    year_built_max = request.GET.get('year_built_max', '')
    ambientes = request.GET.get('ambientes', '')
    cuota_mantenimiento_max = request.GET.get('cuota_mantenimiento_max', '')
    
    # Aplicar filtros básicos
    if property_type:
        properties = properties.filter(property_type=property_type)
    if operation_type:
        properties = properties.filter(operation_type=operation_type)
    if state:
        properties = properties.filter(state__icontains=state)
    elif city:  # Mantener compatibilidad con búsquedas antiguas
        properties = properties.filter(city__icontains=city)
    if region:
        # Buscar propiedades que tengan la región en la dirección o en regiones relacionadas
        from regions.models import Region
        try:
            region_obj = Region.objects.filter(name__icontains=region, is_active=True).first()
            if region_obj:
                properties = properties.filter(address__icontains=region)
            else:
                properties = properties.filter(address__icontains=region)
        except:
            properties = properties.filter(address__icontains=region)
    
    # Aplicar filtros de precio
    if precio_min:
        try:
            properties = properties.filter(price__gte=float(precio_min))
        except (ValueError, TypeError):
            pass
    if precio_max:
        try:
            properties = properties.filter(price__lte=float(precio_max))
        except (ValueError, TypeError):
            pass
    
    # Aplicar filtros de características
    if recamaras:
        try:
            properties = properties.filter(bedrooms__gte=int(recamaras))
        except (ValueError, TypeError):
            pass
    if banos:
        try:
            properties = properties.filter(bathrooms__gte=int(banos))
        except (ValueError, TypeError):
            pass
    if medios_banos:
        try:
            properties = properties.filter(half_bathrooms__gte=int(medios_banos))
        except (ValueError, TypeError):
            pass
    if estacionamiento:
        try:
            properties = properties.filter(parking_spaces__gte=int(estacionamiento))
        except (ValueError, TypeError):
            pass
    if ambientes:
        try:
            properties = properties.filter(rooms__gte=int(ambientes))
        except (ValueError, TypeError):
            pass
    
    # Aplicar filtros de área
    if area_min:
        try:
            properties = properties.filter(area__gte=float(area_min))
        except (ValueError, TypeError):
            pass
    if area_max:
        try:
            properties = properties.filter(area__lte=float(area_max))
        except (ValueError, TypeError):
            pass
    if area_construccion_min:
        try:
            properties = properties.filter(construction_area__gte=float(area_construccion_min))
        except (ValueError, TypeError):
            pass
    if area_construccion_max:
        try:
            properties = properties.filter(construction_area__lte=float(area_construccion_max))
        except (ValueError, TypeError):
            pass
    if area_terreno_min:
        try:
            properties = properties.filter(lot_area__gte=float(area_terreno_min))
        except (ValueError, TypeError):
            pass
    if area_terreno_max:
        try:
            properties = properties.filter(lot_area__lte=float(area_terreno_max))
        except (ValueError, TypeError):
            pass
    
    # Aplicar filtros adicionales
    if niveles:
        try:
            properties = properties.filter(floors__gte=int(niveles))
        except (ValueError, TypeError):
            pass
    if year_built_min:
        try:
            properties = properties.filter(year_built__gte=int(year_built_min))
        except (ValueError, TypeError):
            pass
    if year_built_max:
        try:
            properties = properties.filter(year_built__lte=int(year_built_max))
        except (ValueError, TypeError):
            pass
    if cuota_mantenimiento_max:
        try:
            properties = properties.filter(maintenance_fee__lte=float(cuota_mantenimiento_max))
        except (ValueError, TypeError):
            pass
    
    # Paginación
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Obtener tipos y operaciones para filtros
    property_types = PropertyType.choices
    operation_types = PropertyOperation.choices
    
    context = {
        'properties': page_obj,
        'property_types': property_types,
        'operation_types': operation_types,
        'current_filters': {
            'tipo': property_type,
            'operacion': operation_type,
            'ciudad': city,
        }
    }
    
    return render(request, 'properties/list.html', context)


def departamentos_list(request):
    """Vista para listar solo departamentos en venta"""
    from properties.models import PropertyType, PropertyOperation
    
    # Filtrar solo departamentos disponibles para venta
    properties = Property.objects.filter(
        status='disponible',
        property_type='departamento',
        operation_type__in=['venta', 'venta_renta']
    )
    
    # Aplicar filtros adicionales
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    recamaras = request.GET.get('recamaras', '')
    banos = request.GET.get('banos', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if recamaras:
        properties = properties.filter(bedrooms__gte=recamaras)
    if banos:
        properties = properties.filter(bathrooms__gte=banos)
    
    properties = properties.order_by('-created_at')
    
    # Paginación
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Departamentos en Venta',
        'subtitle': 'Encuentra el departamento perfecto para ti',
    }
    
    return render(request, 'properties/departamentos.html', context)


def casas_list(request):
    """Vista para listar solo casas en venta"""
    properties = Property.objects.filter(
        status='disponible',
        property_type='casa',
        operation_type__in=['venta', 'venta_renta']
    )
    
    # Aplicar filtros
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    recamaras = request.GET.get('recamaras', '')
    banos = request.GET.get('banos', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if recamaras:
        properties = properties.filter(bedrooms__gte=recamaras)
    if banos:
        properties = properties.filter(bathrooms__gte=banos)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Casas en Venta',
        'subtitle': 'Encuentra la casa de tus sueños',
        'icon': 'house-door',
    }
    
    return render(request, 'properties/categoria.html', context)


def terrenos_list(request):
    """Vista para listar solo terrenos en venta"""
    properties = Property.objects.filter(
        status='disponible',
        property_type='terreno',
        operation_type__in=['venta', 'venta_renta']
    )
    
    # Aplicar filtros
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    area_min = request.GET.get('area_min', '')
    area_max = request.GET.get('area_max', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if area_min:
        properties = properties.filter(area__gte=area_min)
    if area_max:
        properties = properties.filter(area__lte=area_max)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Terrenos en Venta',
        'subtitle': 'Invierte en el terreno ideal',
        'icon': 'map',
        'show_area': True,
    }
    
    return render(request, 'properties/categoria.html', context)


def locales_list(request):
    """Vista para listar solo locales comerciales en venta"""
    properties = Property.objects.filter(
        status='disponible',
        property_type='local',
        operation_type__in=['venta', 'venta_renta']
    )
    
    # Aplicar filtros
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    area_min = request.GET.get('area_min', '')
    area_max = request.GET.get('area_max', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if area_min:
        properties = properties.filter(area__gte=area_min)
    if area_max:
        properties = properties.filter(area__lte=area_max)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Locales Comerciales en Venta',
        'subtitle': 'El espacio perfecto para tu negocio',
        'icon': 'shop',
        'show_area': True,
    }
    
    return render(request, 'properties/categoria.html', context)


def renta_list(request):
    """Vista para listar todas las propiedades en renta"""
    properties = Property.objects.filter(
        status='disponible',
        operation_type__in=['renta', 'venta_renta']
    )
    
    # Aplicar filtros
    property_type = request.GET.get('tipo', '')
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    recamaras = request.GET.get('recamaras', '')
    banos = request.GET.get('banos', '')
    
    if property_type:
        properties = properties.filter(property_type=property_type)
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if recamaras:
        properties = properties.filter(bedrooms__gte=recamaras)
    if banos:
        properties = properties.filter(bathrooms__gte=banos)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Propiedades en Renta',
        'subtitle': 'Encuentra tu próximo hogar',
        'icon': 'key',
        'operation': 'renta',
        'current_filters': {
            'tipo': property_type,
            'ciudad': city,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'recamaras': recamaras,
            'banos': banos,
        }
    }
    
    return render(request, 'properties/renta.html', context)


def renta_departamentos_list(request):
    """Vista para listar departamentos en renta"""
    properties = Property.objects.filter(
        status='disponible',
        property_type='departamento',
        operation_type__in=['renta', 'venta_renta']
    )
    
    # Aplicar filtros
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    recamaras = request.GET.get('recamaras', '')
    banos = request.GET.get('banos', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if recamaras:
        properties = properties.filter(bedrooms__gte=recamaras)
    if banos:
        properties = properties.filter(bathrooms__gte=banos)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Departamentos en Renta',
        'subtitle': 'Encuentra el departamento ideal',
        'icon': 'building',
        'operation': 'renta',
        'current_filters': {
            'ciudad': city,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'recamaras': recamaras,
            'banos': banos,
        }
    }
    
    return render(request, 'properties/categoria.html', context)


def renta_casas_list(request):
    """Vista para listar casas en renta"""
    
    properties = Property.objects.filter(
        status='disponible',
        property_type='casa',
        operation_type__in=['renta', 'venta_renta']
    )
    
    # Aplicar filtros
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    recamaras = request.GET.get('recamaras', '')
    banos = request.GET.get('banos', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if recamaras:
        properties = properties.filter(bedrooms__gte=recamaras)
    if banos:
        properties = properties.filter(bathrooms__gte=banos)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Casas en Renta',
        'subtitle': 'Tu próximo hogar te espera',
        'icon': 'house-door',
        'operation': 'renta',
        'current_filters': {
            'ciudad': city,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'recamaras': recamaras,
            'banos': banos,
        }
    }
    
    return render(request, 'properties/categoria.html', context)


def renta_locales_list(request):
    """Vista para listar locales comerciales en renta"""
    properties = Property.objects.filter(
        status='disponible',
        property_type='local',
        operation_type__in=['renta', 'venta_renta']
    )
    
    # Aplicar filtros
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    area_min = request.GET.get('area_min', '')
    area_max = request.GET.get('area_max', '')
    
    if city:
        properties = properties.filter(city__icontains=city)
    if precio_min:
        properties = properties.filter(price__gte=precio_min)
    if precio_max:
        properties = properties.filter(price__lte=precio_max)
    if area_min:
        properties = properties.filter(area__gte=area_min)
    if area_max:
        properties = properties.filter(area__lte=area_max)
    
    properties = properties.order_by('-created_at')
    
    paginator = Paginator(properties, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'title': 'Locales Comerciales en Renta',
        'subtitle': 'El espacio ideal para tu negocio',
        'icon': 'shop',
        'show_area': True,
        'operation': 'renta',
        'current_filters': {
            'ciudad': city,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'area_min': area_min,
            'area_max': area_max,
        }
    }
    
    return render(request, 'properties/categoria.html', context)


def property_detail(request, pk):
    """Vista para mostrar el detalle de una propiedad"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Obtener todas las imágenes de la propiedad
    images = property_obj.images.all().order_by('is_main', 'order')
    
    # Obtener características de la propiedad
    features = property_obj.features.all()
    
    # Obtener propiedades relacionadas (misma ciudad, mismo tipo)
    related_properties = Property.objects.filter(
        city=property_obj.city,
        property_type=property_obj.property_type,
        status='disponible'
    ).exclude(pk=pk)[:4]
    
    context = {
        'property': property_obj,
        'images': images,
        'features': features,
        'related_properties': related_properties,
    }
    
    return render(request, 'properties/detail.html', context)


def is_staff_user(user):
    """Verificar si el usuario es staff (administrador)"""
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def add_property(request):
    """Vista para agregar una nueva propiedad (solo administradores)"""
    
    if request.method == 'POST':
        try:
            # Crear propiedad directamente desde POST
            property_obj = Property(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                property_type=request.POST.get('property_type'),
                operation_type=request.POST.get('operation_type'),
                status='disponible',
                price=request.POST.get('price'),
                currency='MXN',
                address=request.POST.get('address'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                zip_code=request.POST.get('zip_code', ''),
                country='México',
                google_maps_url=request.POST.get('google_maps_url', ''),
                latitude=float(request.POST.get('latitude')) if request.POST.get('latitude') else None,
                longitude=float(request.POST.get('longitude')) if request.POST.get('longitude') else None,
                bedrooms=int(request.POST.get('bedrooms') or 0),
                bathrooms=int(request.POST.get('bathrooms') or 0),
                half_bathrooms=int(request.POST.get('half_bathrooms') or 0),
                parking_spaces=int(request.POST.get('parking_spaces') or 0),
                area=float(request.POST.get('area') or 0),
                construction_area=float(request.POST.get('construction_area') or 0) if request.POST.get('construction_area') else None,
                lot_area=float(request.POST.get('lot_area')) if request.POST.get('lot_area') else None,
                front_measure=float(request.POST.get('front_measure')) if request.POST.get('front_measure') else None,
                back_measure=float(request.POST.get('back_measure')) if request.POST.get('back_measure') else None,
                floors=int(request.POST.get('floors') or 1),
                year_built=int(request.POST.get('year_built')) if request.POST.get('year_built') else None,
                rooms=int(request.POST.get('rooms') or 0),
                maintenance_fee=float(request.POST.get('maintenance_fee')) if request.POST.get('maintenance_fee') else None,
                is_featured='is_featured' in request.POST,
                is_new='is_new' in request.POST,
                published_at=timezone.now(),
                # Distribución
                has_sala='has_sala' in request.POST,
                has_comedor='has_comedor' in request.POST,
                has_cocina='has_cocina' in request.POST,
                has_estudio='has_estudio' in request.POST,
                has_despensa='has_despensa' in request.POST,
                has_cuarto_tv='has_cuarto_tv' in request.POST,
                has_gimnasio='has_gimnasio' in request.POST,
                has_balcon='has_balcon' in request.POST,
                has_jardin='has_jardin' in request.POST,
                has_patio='has_patio' in request.POST,
                has_roof_garden='has_roof_garden' in request.POST,
                has_area_lavado='has_area_lavado' in request.POST,
                has_bodega='has_bodega' in request.POST,
                # Amenidades
                amenity_salon='amenity_salon' in request.POST,
                amenity_vigilancia='amenity_vigilancia' in request.POST,
                amenity_acceso='amenity_acceso' in request.POST,
                amenity_areas_verdes='amenity_areas_verdes' in request.POST,
                amenity_juegos='amenity_juegos' in request.POST,
                amenity_gimnasio='amenity_gimnasio' in request.POST,
                amenity_alberca='amenity_alberca' in request.POST,
                amenity_cancha_futbol='amenity_cancha_futbol' in request.POST,
                amenity_cancha_tenis='amenity_cancha_tenis' in request.POST,
                amenity_cancha_basket='amenity_cancha_basket' in request.POST,
                amenity_asadores='amenity_asadores' in request.POST,
                amenity_pet_friendly='amenity_pet_friendly' in request.POST,
                # Servicios
                service_agua='service_agua' in request.POST,
                service_drenaje='service_drenaje' in request.POST,
                service_luz='service_luz' in request.POST,
                service_gas='service_gas' in request.POST,
                service_internet='service_internet' in request.POST,
                service_fibra='service_fibra' in request.POST,
                service_cable='service_cable' in request.POST,
                service_telefono='service_telefono' in request.POST,
                service_cisterna='service_cisterna' in request.POST,
                service_hidroneumatico='service_hidroneumatico' in request.POST,
                service_aire='service_aire' in request.POST,
                service_boiler='service_boiler' in request.POST,
            )
            
            property_obj.save()
            
            # Guardar imágenes
            images = request.FILES.getlist('images')
            if images:
                for idx, image in enumerate(images):
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=image,
                        is_main=(idx == 0),
                        order=idx,
                        alt_text=f"Imagen {idx + 1} de {property_obj.title}"
                    )
                
                if property_obj.is_featured:
                    messages.success(request, f'Propiedad "{property_obj.title}" creada exitosamente y marcada como DESTACADA. Aparecerá en el carrusel principal.')
                else:
                    messages.success(request, f'Propiedad "{property_obj.title}" creada exitosamente con {len(images)} imágenes.')
            else:
                messages.warning(request, f'Propiedad "{property_obj.title}" creada sin imágenes. Puedes agregarlas después.')
            
            return redirect('properties:detail', pk=property_obj.pk)
            
        except Exception as e:
            messages.error(request, f'Error al crear la propiedad: {str(e)}')
            return render(request, 'properties/add_property.html', {'title': 'Agregar Nueva Propiedad'})
    
    context = {
        'title': 'Agregar Nueva Propiedad'
    }
    
    return render(request, 'properties/add_property.html', context)


@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def edit_property(request, pk):
    """Vista para editar una propiedad existente (solo administradores)"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        try:
            # Actualizar propiedad
            property_obj.title = request.POST.get('title')
            property_obj.description = request.POST.get('description')
            property_obj.property_type = request.POST.get('property_type')
            property_obj.operation_type = request.POST.get('operation_type')
            price_value = request.POST.get('price', '').strip()
            property_obj.price = float(price_value) if price_value else property_obj.price
            property_obj.address = request.POST.get('address')
            property_obj.city = request.POST.get('city')
            property_obj.state = request.POST.get('state')
            property_obj.zip_code = request.POST.get('zip_code', '')
            property_obj.latitude = float(request.POST.get('latitude')) if request.POST.get('latitude') else None
            property_obj.longitude = float(request.POST.get('longitude')) if request.POST.get('longitude') else None
            property_obj.bedrooms = int(request.POST.get('bedrooms') or 0)
            property_obj.bathrooms = int(request.POST.get('bathrooms') or 0)
            property_obj.half_bathrooms = int(request.POST.get('half_bathrooms') or 0)
            property_obj.parking_spaces = int(request.POST.get('parking_spaces') or 0)
            property_obj.area = float(request.POST.get('construction_area') or 0)
            property_obj.construction_area = float(request.POST.get('construction_area') or 0)
            property_obj.lot_area = float(request.POST.get('lot_area') or 0)
            property_obj.front_measure = request.POST.get('front_measure') or None
            property_obj.back_measure = request.POST.get('back_measure') or None
            property_obj.floors = int(request.POST.get('floors') or 1)
            property_obj.year_built = int(request.POST.get('year_built')) if request.POST.get('year_built') else None
            property_obj.rooms = int(request.POST.get('rooms') or 0)
            property_obj.maintenance_fee = request.POST.get('maintenance_fee') or None
            property_obj.is_featured = 'is_featured' in request.POST
            property_obj.is_new = 'is_new' in request.POST
            # Distribución
            property_obj.has_sala = 'has_sala' in request.POST
            property_obj.has_comedor = 'has_comedor' in request.POST
            property_obj.has_cocina = 'has_cocina' in request.POST
            property_obj.has_estudio = 'has_estudio' in request.POST
            property_obj.has_despensa = 'has_despensa' in request.POST
            property_obj.has_cuarto_tv = 'has_cuarto_tv' in request.POST
            property_obj.has_gimnasio = 'has_gimnasio' in request.POST
            property_obj.has_balcon = 'has_balcon' in request.POST
            property_obj.has_jardin = 'has_jardin' in request.POST
            property_obj.has_patio = 'has_patio' in request.POST
            property_obj.has_roof_garden = 'has_roof_garden' in request.POST
            property_obj.has_area_lavado = 'has_area_lavado' in request.POST
            property_obj.has_bodega = 'has_bodega' in request.POST
            # Amenidades
            property_obj.amenity_salon = 'amenity_salon' in request.POST
            property_obj.amenity_vigilancia = 'amenity_vigilancia' in request.POST
            property_obj.amenity_acceso = 'amenity_acceso' in request.POST
            property_obj.amenity_areas_verdes = 'amenity_areas_verdes' in request.POST
            property_obj.amenity_juegos = 'amenity_juegos' in request.POST
            property_obj.amenity_gimnasio = 'amenity_gimnasio' in request.POST
            property_obj.amenity_alberca = 'amenity_alberca' in request.POST
            property_obj.amenity_cancha_futbol = 'amenity_cancha_futbol' in request.POST
            property_obj.amenity_cancha_tenis = 'amenity_cancha_tenis' in request.POST
            property_obj.amenity_cancha_basket = 'amenity_cancha_basket' in request.POST
            property_obj.amenity_asadores = 'amenity_asadores' in request.POST
            property_obj.amenity_pet_friendly = 'amenity_pet_friendly' in request.POST
            # Servicios
            property_obj.service_agua = 'service_agua' in request.POST
            property_obj.service_drenaje = 'service_drenaje' in request.POST
            property_obj.service_luz = 'service_luz' in request.POST
            property_obj.service_gas = 'service_gas' in request.POST
            property_obj.service_internet = 'service_internet' in request.POST
            property_obj.service_fibra = 'service_fibra' in request.POST
            property_obj.service_cable = 'service_cable' in request.POST
            property_obj.service_telefono = 'service_telefono' in request.POST
            property_obj.service_cisterna = 'service_cisterna' in request.POST
            property_obj.service_hidroneumatico = 'service_hidroneumatico' in request.POST
            property_obj.service_aire = 'service_aire' in request.POST
            property_obj.service_boiler = 'service_boiler' in request.POST
            
            property_obj.save()
            
            # Agregar nuevas imágenes si se subieron
            images = request.FILES.getlist('images')
            if images:
                current_count = property_obj.images.count()
                for idx, image in enumerate(images):
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=image,
                        is_main=False,
                        order=current_count + idx,
                        alt_text=f"Imagen {current_count + idx + 1} de {property_obj.title}"
                    )
            
            messages.success(request, f'Propiedad "{property_obj.title}" actualizada exitosamente.')
            return redirect('properties:detail', pk=property_obj.pk)
            
        except Exception as e:
            messages.error(request, f'Error al actualizar la propiedad: {str(e)}')
            return render(request, 'properties/edit_property.html', {'property': property_obj, 'title': 'Editar Propiedad'})
    
    context = {
        'property': property_obj,
        'title': 'Editar Propiedad'
    }
    
    return render(request, 'properties/edit_property.html', context)



@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def manage_images(request, pk):
    """Vista para gestionar imágenes de una propiedad"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'set_main':
            # Establecer imagen principal
            image_id = request.POST.get('image_id')
            PropertyImage.objects.filter(property=property_obj).update(is_main=False)
            PropertyImage.objects.filter(id=image_id).update(is_main=True)
            messages.success(request, 'Imagen principal actualizada.')
        
        elif action == 'delete':
            # Eliminar imagen
            image_id = request.POST.get('image_id')
            PropertyImage.objects.filter(id=image_id).delete()
            messages.success(request, 'Imagen eliminada.')
        
        elif action == 'upload':
            # Subir nuevas imágenes
            images = request.FILES.getlist('images')
            if images:
                current_count = property_obj.images.count()
                for idx, image in enumerate(images):
                    PropertyImage.objects.create(
                        property=property_obj,
                        image=image,
                        is_main=False,
                        order=current_count + idx,
                        alt_text=f"Imagen {current_count + idx + 1} de {property_obj.title}"
                    )
                messages.success(request, f'{len(images)} imágenes agregadas.')
        
        return redirect('properties:manage_images', pk=pk)
    
    images = property_obj.images.all().order_by('-is_main', 'order')
    
    context = {
        'property': property_obj,
        'images': images,
    }
    
    return render(request, 'properties/manage_images.html', context)



@login_required
@user_passes_test(is_staff_user, login_url='/admin/login/')
def download_property_pdf(request, pk):
    from django.http import HttpResponse
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
    import os
    from django.conf import settings
    
    property_obj = get_object_or_404(Property, pk=pk)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="TotalLiving_{property_obj.slug}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    olive = colors.HexColor('#3B3E2A')
    gold = colors.HexColor('#D6B585')
    beige = colors.HexColor('#F2ECE0')
    
    # Logo
    logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'SharedScreenshot.png')
    if os.path.exists(logo_path):
        logo = RLImage(logo_path, width=1.5*inch, height=1.5*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 0.2*inch))
    
    # Header
    h = Table([[Paragraph('<b><font size=28 color="#3B3E2A">TOTAL LIVING</font></b><br/><font size=12 color="#D6B585">Tu Inmobiliaria de Confianza</font>', ParagraphStyle('H', parent=styles['Normal'], alignment=TA_CENTER))]], colWidths=[7*inch])
    h.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),beige),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),20),('BOTTOMPADDING',(0,0),(-1,-1),20),('BOX',(0,0),(-1,-1),2,olive)]))
    elements.append(h)
    elements.append(Spacer(1, 0.3*inch))
    
    # Título y Precio
    elements.append(Paragraph(property_obj.title.upper(), ParagraphStyle('T', parent=styles['Heading1'], fontSize=20, textColor=olive, alignment=TA_CENTER, fontName='Helvetica-Bold')))
    elements.append(Paragraph(property_obj.get_price_display(), ParagraphStyle('P', parent=styles['Normal'], fontSize=24, textColor=gold, alignment=TA_CENTER, fontName='Helvetica-Bold')))
    elements.append(Spacer(1, 0.2*inch))
    
    # Fotos de la propiedad
    images = property_obj.images.all().order_by('-is_main', 'order')[:6]
    if images:
        ph = Table([[Paragraph('<b><font size=14 color="white">FOTOGRAFÍAS</font></b>', styles['Normal'])]], colWidths=[7*inch])
        ph.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
        elements.append(ph)
        elements.append(Spacer(1, 0.1*inch))
        
        img_data = []
        img_row = []
        for idx, img in enumerate(images):
            try:
                img_path = os.path.join(settings.MEDIA_ROOT, str(img.image))
                if os.path.exists(img_path):
                    prop_img = RLImage(img_path, width=3.3*inch, height=2.5*inch)
                    img_row.append(prop_img)
                    if len(img_row) == 2 or idx == len(images) - 1:
                        img_data.append(img_row)
                        img_row = []
            except:
                pass
        
        if img_data:
            img_table = Table(img_data, colWidths=[3.5*inch, 3.5*inch])
            img_table.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
            elements.append(img_table)
            elements.append(Spacer(1, 0.2*inch))
    
    # Info General
    ih = Table([[Paragraph('<b><font size=14 color="white">INFORMACIÓN GENERAL</font></b>', styles['Normal'])]], colWidths=[7*inch])
    ih.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    elements.append(ih)
    
    md = [
        ['Tipo:', property_obj.get_property_type_display(), 'Operación:', property_obj.get_operation_type_display()],
        ['Recámaras:', str(property_obj.bedrooms), 'Baños:', str(property_obj.bathrooms)],
        ['Medios Baños:', str(getattr(property_obj,'half_bathrooms',0)), 'Estacionamientos:', str(property_obj.parking_spaces)],
        ['Terreno:', f"{property_obj.lot_area} m²" if property_obj.lot_area else 'N/A', 'Construcción:', f"{property_obj.construction_area} m²" if property_obj.construction_area else 'N/A'],
        ['Niveles:', str(property_obj.floors), 'Año:', str(property_obj.year_built) if property_obj.year_built else 'N/A'],
        ['Ambientes:', str(getattr(property_obj,'rooms',0)), 'Mantenimiento:', f"${getattr(property_obj,'maintenance_fee',0)}" if getattr(property_obj,'maintenance_fee',None) else 'N/A']
    ]
    mt = Table(md, colWidths=[1.5*inch,2*inch,1.5*inch,2*inch])
    mt.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),beige),('BACKGROUND',(2,0),(2,-1),beige),('FONTNAME',(0,0),(0,-1),'Helvetica-Bold'),('FONTNAME',(2,0),(2,-1),'Helvetica-Bold'),('FONTSIZE',(0,0),(-1,-1),10),('GRID',(0,0),(-1,-1),1,colors.grey),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]))
    elements.append(mt)
    elements.append(Spacer(1, 0.2*inch))
    
    # Distribución
    di = []
    if getattr(property_obj,'has_sala',False): di.append('Sala')
    if getattr(property_obj,'has_comedor',False): di.append('Comedor')
    if getattr(property_obj,'has_cocina',False): di.append('Cocina Integral')
    if getattr(property_obj,'has_estudio',False): di.append('Estudio')
    if getattr(property_obj,'has_despensa',False): di.append('Despensa')
    if getattr(property_obj,'has_cuarto_tv',False): di.append('Cuarto TV')
    if getattr(property_obj,'has_gimnasio',False): di.append('Gimnasio')
    if getattr(property_obj,'has_balcon',False): di.append('Balcón')
    if getattr(property_obj,'has_jardin',False): di.append('Jardín')
    if getattr(property_obj,'has_patio',False): di.append('Patio')
    if getattr(property_obj,'has_roof_garden',False): di.append('Roof Garden')
    if getattr(property_obj,'has_area_lavado',False): di.append('Área de Lavado')
    if getattr(property_obj,'has_bodega',False): di.append('Bodega')
    
    if di:
        dh = Table([[Paragraph('<b><font size=14 color="white">DISTRIBUCIÓN</font></b>', styles['Normal'])]], colWidths=[7*inch])
        dh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
        elements.append(dh)
        dt = Table([[Paragraph('• '+'<br/>• '.join(di), ParagraphStyle('D',parent=styles['Normal'],fontSize=10))]], colWidths=[7*inch])
        dt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.grey),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15)]))
        elements.append(dt)
        elements.append(Spacer(1, 0.2*inch))
    
    # Amenidades
    am = []
    if getattr(property_obj,'amenity_salon',False): am.append('Salón de Usos Múltiples')
    if getattr(property_obj,'amenity_vigilancia',False): am.append('Vigilancia 24/7')
    if getattr(property_obj,'amenity_acceso',False): am.append('Acceso Controlado')
    if getattr(property_obj,'amenity_areas_verdes',False): am.append('Áreas Verdes')
    if getattr(property_obj,'amenity_juegos',False): am.append('Juegos Infantiles')
    if getattr(property_obj,'amenity_gimnasio',False): am.append('Gimnasio')
    if getattr(property_obj,'amenity_alberca',False): am.append('Alberca')
    if getattr(property_obj,'amenity_cancha_futbol',False): am.append('Cancha de Fútbol')
    if getattr(property_obj,'amenity_cancha_tenis',False): am.append('Cancha de Tenis')
    if getattr(property_obj,'amenity_cancha_basket',False): am.append('Cancha de Basketball')
    if getattr(property_obj,'amenity_asadores',False): am.append('Zona de Asadores')
    if getattr(property_obj,'amenity_pet_friendly',False): am.append('Pet Friendly')
    
    if am:
        ah = Table([[Paragraph('<b><font size=14 color="white">AMENIDADES</font></b>', styles['Normal'])]], colWidths=[7*inch])
        ah.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
        elements.append(ah)
        at = Table([[Paragraph('• '+'<br/>• '.join(am), ParagraphStyle('A',parent=styles['Normal'],fontSize=10))]], colWidths=[7*inch])
        at.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.grey),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15)]))
        elements.append(at)
        elements.append(Spacer(1, 0.2*inch))
    
    # Servicios
    sv = []
    if getattr(property_obj,'service_agua',False): sv.append('Agua')
    if getattr(property_obj,'service_drenaje',False): sv.append('Drenaje')
    if getattr(property_obj,'service_luz',False): sv.append('Luz')
    if getattr(property_obj,'service_gas',False): sv.append('Gas Estacionario')
    if getattr(property_obj,'service_internet',False): sv.append('Internet')
    if getattr(property_obj,'service_fibra',False): sv.append('Fibra Óptica')
    if getattr(property_obj,'service_cable',False): sv.append('TV Cable')
    if getattr(property_obj,'service_telefono',False): sv.append('Línea Telefónica')
    if getattr(property_obj,'service_cisterna',False): sv.append('Cisterna')
    if getattr(property_obj,'service_hidroneumatico',False): sv.append('Hidroneumático')
    if getattr(property_obj,'service_aire',False): sv.append('Aire Acondicionado')
    if getattr(property_obj,'service_boiler',False): sv.append('Boiler')
    
    if sv:
        sh = Table([[Paragraph('<b><font size=14 color="white">SERVICIOS</font></b>', styles['Normal'])]], colWidths=[7*inch])
        sh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
        elements.append(sh)
        st = Table([[Paragraph('• '+'<br/>• '.join(sv), ParagraphStyle('S',parent=styles['Normal'],fontSize=10))]], colWidths=[7*inch])
        st.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.grey),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15)]))
        elements.append(st)
        elements.append(Spacer(1, 0.2*inch))
    
    # Ubicación
    lh = Table([[Paragraph('<b><font size=14 color="white">UBICACIÓN</font></b>', styles['Normal'])]], colWidths=[7*inch])
    lh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    elements.append(lh)
    lt = Table([[Paragraph(f"<b>{property_obj.address}</b><br/>{property_obj.city}, {property_obj.state}<br/>C.P. {property_obj.zip_code if property_obj.zip_code else 'N/A'}", ParagraphStyle('L',parent=styles['Normal'],fontSize=11,alignment=TA_CENTER))]], colWidths=[7*inch])
    lt.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.grey),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15)]))
    elements.append(lt)
    
    # Mapa (si hay coordenadas)
    if property_obj.latitude and property_obj.longitude:
        try:
            import urllib.request
            import tempfile
            import os
            lat = float(property_obj.latitude)
            lon = float(property_obj.longitude)
            zoom = 15
            width = 800
            height = 400
            
            # URL del mapa estático con marcador
            map_url = f"https://staticmap.openstreetmap.de/staticmap.php?center={lat},{lon}&zoom={zoom}&size={width}x{height}&markers={lat},{lon},red-pushpin"
            
            # Descargar imagen
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            tmp_file.close()
            
            req = urllib.request.Request(map_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                with open(tmp_file.name, 'wb') as f:
                    f.write(response.read())
            
            # Verificar que el archivo existe y tiene contenido
            if os.path.exists(tmp_file.name) and os.path.getsize(tmp_file.name) > 0:
                map_img = RLImage(tmp_file.name, width=6.5*inch, height=3.25*inch)
                map_img.hAlign = 'CENTER'
                elements.append(map_img)
                # Limpiar archivo temporal
                try:
                    os.unlink(tmp_file.name)
                except:
                    pass
            else:
                raise Exception("Imagen vacía")
        except Exception as e:
            # Si falla, mostrar coordenadas
            coord_text = Paragraph(f"<b>Coordenadas GPS:</b> Lat: {property_obj.latitude}, Lon: {property_obj.longitude}", ParagraphStyle('C',parent=styles['Normal'],fontSize=10,alignment=TA_CENTER))
            elements.append(coord_text)
    
    elements.append(Spacer(1, 0.2*inch))
    
    # Descripción
    deh = Table([[Paragraph('<b><font size=14 color="white">DESCRIPCIÓN</font></b>', styles['Normal'])]], colWidths=[7*inch])
    deh.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),olive),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10)]))
    elements.append(deh)
    det = Table([[Paragraph(property_obj.description, ParagraphStyle('DE',parent=styles['Normal'],fontSize=10,alignment=TA_JUSTIFY,leading=14))]], colWidths=[7*inch])
    det.setStyle(TableStyle([('GRID',(0,0),(-1,-1),1,colors.grey),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15)]))
    elements.append(det)
    elements.append(Spacer(1, 0.3*inch))
    
    # Footer
    f = Table([[Paragraph('<b><font size=12 color="#3B3E2A">TOTAL LIVING</font></b><br/><font size=9 color="#D6B585">www.totalliving.com | contacto@totalliving.com | Tel: +52 55 1234 5678</font><br/><font size=8>Esta ficha técnica es informativa y no constituye una oferta vinculante</font>', ParagraphStyle('F',parent=styles['Normal'],alignment=TA_CENTER))]], colWidths=[7*inch])
    f.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),beige),('ALIGN',(0,0),(-1,-1),'CENTER'),('TOPPADDING',(0,0),(-1,-1),15),('BOTTOMPADDING',(0,0),(-1,-1),15),('BOX',(0,0),(-1,-1),2,olive)]))
    elements.append(f)
    
    doc.build(elements)
    return response

