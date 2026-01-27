from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from properties.models import Property, PropertyImage, CarouselSlide
from django.utils import timezone


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('panel:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos, o no tienes permisos de acceso.')
    
    return render(request, 'panel/login.html')


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_logout(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('panel:login')


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def dashboard(request):
    total_properties = Property.objects.count()
    disponibles = Property.objects.filter(status='disponible').count()
    vendidas = Property.objects.filter(status='vendida').count()
    rentadas = Property.objects.filter(status='rentada').count()
    destacadas = Property.objects.filter(is_featured=True).count()
    
    recent_properties = Property.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_properties': total_properties,
        'disponibles': disponibles,
        'vendidas': vendidas,
        'rentadas': rentadas,
        'destacadas': destacadas,
        'recent_properties': recent_properties,
    }
    
    return render(request, 'panel/dashboard.html', context)


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_properties(request):
    properties = Property.objects.all().order_by('-created_at')
    
    # Filtros
    search = request.GET.get('search', '')
    status = request.GET.get('status', '')
    property_type = request.GET.get('tipo', '')
    process = request.GET.get('process', '')
    
    if search:
        properties = properties.filter(
            Q(title__icontains=search) | 
            Q(city__icontains=search) | 
            Q(address__icontains=search)
        )
    if status:
        properties = properties.filter(status=status)
    if property_type:
        properties = properties.filter(property_type=property_type)
    if process:
        properties = properties.filter(process=process)
    
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'search': search,
        'status_filter': status,
        'type_filter': property_type,
        'process_filter': process,
    }
    
    return render(request, 'panel/properties.html', context)


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_property_edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        try:
            property_obj.title = request.POST.get('title')
            property_obj.description = request.POST.get('description')
            property_obj.property_type = request.POST.get('property_type')
            property_obj.operation_type = request.POST.get('operation_type')
            property_obj.status = request.POST.get('status')
            property_obj.process = request.POST.get('process', 'en_busqueda')
            # Arreglar bug del precio - convertir a Decimal
            price_value = request.POST.get('price')
            if price_value:
                from decimal import Decimal
                property_obj.price = Decimal(str(price_value))
            else:
                property_obj.price = Decimal('0')
            property_obj.currency = request.POST.get('currency', 'MXN')
            property_obj.address = request.POST.get('address')
            property_obj.city = request.POST.get('city')
            property_obj.state = request.POST.get('state')
            property_obj.zip_code = request.POST.get('zip_code', '')
            property_obj.country = request.POST.get('country', 'México')
            property_obj.google_maps_url = request.POST.get('google_maps_url', '')
            # Coordenadas
            latitude = request.POST.get('latitude')
            property_obj.latitude = float(latitude) if latitude else None
            longitude = request.POST.get('longitude')
            property_obj.longitude = float(longitude) if longitude else None
            property_obj.bedrooms = int(request.POST.get('bedrooms') or 0)
            property_obj.bathrooms = int(request.POST.get('bathrooms') or 0)
            property_obj.half_bathrooms = int(request.POST.get('half_bathrooms') or 0)
            property_obj.parking_spaces = int(request.POST.get('parking_spaces') or 0)
            # Áreas
            property_obj.area = float(request.POST.get('area') or 0)
            property_obj.construction_area = float(request.POST.get('construction_area') or 0) if request.POST.get('construction_area') else None
            property_obj.lot_area = float(request.POST.get('lot_area')) if request.POST.get('lot_area') else None
            property_obj.front_measure = float(request.POST.get('front_measure')) if request.POST.get('front_measure') else None
            property_obj.back_measure = float(request.POST.get('back_measure')) if request.POST.get('back_measure') else None
            property_obj.floors = int(request.POST.get('floors') or 1)
            property_obj.year_built = int(request.POST.get('year_built')) if request.POST.get('year_built') else None
            property_obj.rooms = int(request.POST.get('rooms') or 0)
            maintenance_fee = request.POST.get('maintenance_fee')
            property_obj.maintenance_fee = float(maintenance_fee) if maintenance_fee else None
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
            
            messages.success(request, f'Propiedad "{property_obj.title}" actualizada exitosamente.')
            return redirect('panel:properties')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar la propiedad: {str(e)}')
    
    context = {
        'property': property_obj,
    }
    
    return render(request, 'panel/property_edit.html', context)


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        title = property_obj.title
        property_obj.delete()
        messages.success(request, f'Propiedad "{title}" eliminada exitosamente.')
        return redirect('panel:properties')
    
    context = {
        'property': property_obj,
    }
    
    return render(request, 'panel/property_delete.html', context)


# ========== GESTIÓN DEL CARRUSEL ==========

@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_carousel_list(request):
    """Lista de slides del carrusel"""
    slides = CarouselSlide.objects.all().order_by('order', '-created_at')
    
    context = {
        'slides': slides,
    }
    
    return render(request, 'panel/carousel_list.html', context)


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_carousel_add(request):
    """Agregar nuevo slide al carrusel"""
    if request.method == 'POST':
        try:
            slide = CarouselSlide()
            slide.title = request.POST.get('title')
            slide.subtitle = request.POST.get('subtitle', '')
            slide.link_url = request.POST.get('link_url', '')
            slide.link_text = request.POST.get('link_text', 'Ver Más')
            slide.is_active = 'is_active' in request.POST
            slide.order = int(request.POST.get('order', 0))
            
            if 'image' in request.FILES:
                slide.image = request.FILES['image']
            
            slide.save()
            
            messages.success(request, f'Slide "{slide.title}" agregado exitosamente.')
            return redirect('panel:carousel_list')
            
        except Exception as e:
            messages.error(request, f'Error al agregar el slide: {str(e)}')
    
    return render(request, 'panel/carousel_add.html')


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_carousel_edit(request, pk):
    """Editar slide del carrusel"""
    slide = get_object_or_404(CarouselSlide, pk=pk)
    
    if request.method == 'POST':
        try:
            slide.title = request.POST.get('title')
            slide.subtitle = request.POST.get('subtitle', '')
            slide.link_url = request.POST.get('link_url', '')
            slide.link_text = request.POST.get('link_text', 'Ver Más')
            slide.is_active = 'is_active' in request.POST
            slide.order = int(request.POST.get('order', 0))
            
            if 'image' in request.FILES:
                slide.image = request.FILES['image']
            
            slide.save()
            
            messages.success(request, f'Slide "{slide.title}" actualizado exitosamente.')
            return redirect('panel:carousel_list')
            
        except Exception as e:
            messages.error(request, f'Error al actualizar el slide: {str(e)}')
    
    context = {
        'slide': slide,
    }
    
    return render(request, 'panel/carousel_edit.html', context)


@login_required(login_url='/panel/login/')
@user_passes_test(is_staff_user, login_url='/panel/login/')
def panel_carousel_delete(request, pk):
    """Eliminar slide del carrusel"""
    slide = get_object_or_404(CarouselSlide, pk=pk)
    
    if request.method == 'POST':
        title = slide.title
        slide.delete()
        messages.success(request, f'Slide "{title}" eliminado exitosamente.')
        return redirect('panel:carousel_list')
    
    context = {
        'slide': slide,
    }
    
    return render(request, 'panel/carousel_delete.html', context)
