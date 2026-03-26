from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from .login_ratelimit import panel_login_is_limited
from django.core.paginator import Paginator
from django.db.models import Count, Q
from properties.models import Property, PropertyImage, CarouselSlide
from regions.models import Region
from contact.models import Contact, ContactNote
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.db.utils import OperationalError, ProgrammingError
from .models import NosotrosContent


def is_staff_user(user):
    return user.is_authenticated and user.is_staff


def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel:dashboard')
    
    if request.method == 'POST':
        if panel_login_is_limited(request):
            messages.error(
                request,
                'Demasiados intentos de inicio de sesión. Espera unos minutos e inténtalo de nuevo.',
            )
            return render(request, 'panel/login.html')

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('panel:dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos, o no tienes permisos de acceso.')
    
    return render(request, 'panel/login.html')


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_logout(request):
    logout(request)
    messages.success(request, 'Sesión cerrada exitosamente.')
    return redirect('panel:login')


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
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


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_nosotros_edit(request):
    try:
        content, _ = NosotrosContent.objects.get_or_create(pk=1)
    except (OperationalError, ProgrammingError):
        messages.error(
            request,
            'Falta aplicar migraciones del módulo Nosotros. Ejecuta: python manage.py migrate',
        )
        return redirect('panel:dashboard')

    if request.method == 'POST':
        editable_fields = [
            'hero_title', 'hero_line_1', 'hero_line_2',
            'pillar_1', 'pillar_2', 'pillar_3', 'pillar_4',
            'pillar_5', 'pillar_6', 'pillar_7', 'pillar_8',
            'manifest_title',
            'manifest_t_meaning', 'manifest_t_desc',
            'manifest_o_meaning', 'manifest_o_desc',
            'manifest_t2_meaning', 'manifest_t2_desc',
            'manifest_a_meaning', 'manifest_a_desc',
            'manifest_l_meaning', 'manifest_l_desc',
            'mission_vision_title',
            'mission_title', 'mission_text',
            'vision_title', 'vision_text',
            'team_banner_title',
        ]
        for field in editable_fields:
            setattr(content, field, request.POST.get(field, '').strip())
        content.save()
        messages.success(request, 'Sección Nosotros actualizada correctamente.')
        return redirect('panel:nosotros_edit')

    return render(request, 'panel/nosotros_edit.html', {'content': content})


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
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


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_property_edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        try:
            def parse_decimal_field(raw_value, current_value):
                """
                Convierte strings numéricos conservando el valor actual si viene vacío o inválido.
                Soporta formatos con coma/punto.
                """
                if raw_value is None:
                    return current_value

                value = str(raw_value).strip()
                if value == '':
                    return current_value

                # Normalizar separadores: "1,234.56" -> "1234.56", "1234,56" -> "1234.56"
                if ',' in value and '.' in value:
                    value = value.replace(',', '')
                elif ',' in value and '.' not in value:
                    value = value.replace(',', '.')

                try:
                    return float(value)
                except (ValueError, TypeError):
                    return current_value

            property_obj.title = request.POST.get('title')
            property_obj.description = request.POST.get('description')
            property_obj.property_type = request.POST.get('property_type')
            property_obj.operation_type = request.POST.get('operation_type')
            property_obj.status = request.POST.get('status')
            property_obj.process = request.POST.get('process', 'en_busqueda')

            # Precio: conservar si llega vacío/incorrecto
            from decimal import Decimal
            parsed_price = parse_decimal_field(request.POST.get('price'), property_obj.price)
            if parsed_price is not None:
                property_obj.price = Decimal(str(parsed_price))

            property_obj.currency = request.POST.get('currency', 'MXN')
            property_obj.address = request.POST.get('address')
            property_obj.city = request.POST.get('city')
            region_id = request.POST.get('region')
            property_obj.region = Region.objects.filter(pk=region_id, is_active=True).first() if region_id else None
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
            property_obj.area = parse_decimal_field(request.POST.get('area'), property_obj.area)
            property_obj.construction_area = parse_decimal_field(request.POST.get('construction_area'), property_obj.construction_area)
            property_obj.lot_area = parse_decimal_field(request.POST.get('lot_area'), property_obj.lot_area)
            property_obj.front_measure = parse_decimal_field(request.POST.get('front_measure'), property_obj.front_measure)
            property_obj.back_measure = parse_decimal_field(request.POST.get('back_measure'), property_obj.back_measure)
            property_obj.floors = int(request.POST.get('floors') or 1)
            property_obj.year_built = int(request.POST.get('year_built')) if request.POST.get('year_built') else None
            property_obj.rooms = int(request.POST.get('rooms') or 0)
            property_obj.maintenance_fee = parse_decimal_field(request.POST.get('maintenance_fee'), property_obj.maintenance_fee)
            property_obj.is_featured = 'is_featured' in request.POST
            property_obj.is_new = 'is_new' in request.POST
            property_obj.is_advisor_exclusive = 'is_advisor_exclusive' in request.POST
            exclusive_advisor_id = request.POST.get('exclusive_advisor')
            selected_advisor = get_user_model().objects.filter(
                pk=exclusive_advisor_id,
                is_staff=True,
                is_active=True
            ).first() if exclusive_advisor_id else None
            property_obj.exclusive_advisor = selected_advisor if property_obj.is_advisor_exclusive else None
            property_obj.financing_options = request.POST.getlist('financing_options')
            
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
        'regions': Region.objects.filter(is_active=True).order_by('order', 'name'),
        'advisors': get_user_model().objects.filter(is_staff=True, is_active=True).order_by('username'),
        'financing_choices': Property.FINANCING_CHOICES,
    }
    
    return render(request, 'panel/property_edit.html', context)


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
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

@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_carousel_list(request):
    """Lista de slides del carrusel"""
    slides = CarouselSlide.objects.all().order_by('order', '-created_at')
    
    context = {
        'slides': slides,
    }
    
    return render(request, 'panel/carousel_list.html', context)


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
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


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
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


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
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


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_inbox(request):
    """Buzon interno de solicitudes de informacion."""
    contacts = Contact.objects.select_related('property', 'assigned_to').order_by('-created_at')
    staff_users = get_user_model().objects.filter(is_staff=True, is_active=True).order_by('username')

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()
    priority = request.GET.get('priority', '').strip()
    assigned_to = request.GET.get('assigned_to', '').strip()
    mine = request.GET.get('mine', '').strip()
    overdue = request.GET.get('overdue', '').strip()

    if request.method == 'POST':
        action = request.POST.get('bulk_action', '').strip()
        selected_ids = request.POST.getlist('selected_contacts')
        selected_qs = Contact.objects.filter(pk__in=selected_ids)

        if not selected_ids:
            messages.warning(request, 'Selecciona al menos una solicitud para aplicar accion masiva.')
            return redirect('panel:inbox')

        if action == 'mark_read':
            updated = selected_qs.update(is_read=True)
            messages.success(request, f'{updated} solicitudes marcadas como leidas.')
        elif action == 'mark_in_progress':
            updated = selected_qs.update(is_read=True, is_responded=False, status=Contact.STATUS_IN_PROGRESS)
            messages.success(request, f'{updated} solicitudes marcadas en seguimiento.')
        elif action == 'mark_responded':
            updated = selected_qs.update(
                is_read=True,
                is_responded=True,
                status=Contact.STATUS_RESPONDED,
                responded_at=timezone.now()
            )
            messages.success(request, f'{updated} solicitudes marcadas como respondidas.')
        elif action == 'mark_closed':
            updated = selected_qs.update(status=Contact.STATUS_CLOSED)
            messages.success(request, f'{updated} solicitudes cerradas.')
        elif action == 'assign_to_me':
            updated = selected_qs.update(assigned_to=request.user)
            messages.success(request, f'{updated} solicitudes asignadas a tu usuario.')
        else:
            messages.warning(request, 'Accion masiva no valida.')

        return redirect('panel:inbox')

    if search:
        contacts = contacts.filter(
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search) |
            Q(subject__icontains=search) |
            Q(message__icontains=search) |
            Q(property__title__icontains=search)
        )

    if status:
        contacts = contacts.filter(status=status)

    if priority:
        contacts = contacts.filter(priority=priority)

    if assigned_to == 'none':
        contacts = contacts.filter(assigned_to__isnull=True)
    elif assigned_to:
        contacts = contacts.filter(assigned_to_id=assigned_to)

    if mine == '1':
        contacts = contacts.filter(assigned_to=request.user)

    if overdue == '1':
        contacts = contacts.filter(
            follow_up_at__isnull=False,
            follow_up_at__lt=timezone.now()
        ).exclude(status__in=[Contact.STATUS_RESPONDED, Contact.STATUS_CLOSED])

    paginator = Paginator(contacts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    base_qs = Contact.objects.all()
    context = {
        'contacts': page_obj,
        'search': search,
        'status_filter': status,
        'priority_filter': priority,
        'assigned_to_filter': assigned_to,
        'mine_filter': mine,
        'overdue_filter': overdue,
        'staff_users': staff_users,
        'status_choices': Contact.STATUS_CHOICES,
        'priority_choices': Contact.PRIORITY_CHOICES,
        'counts': {
            'total': base_qs.count(),
            'new': base_qs.filter(status=Contact.STATUS_NEW).count(),
            'in_progress': base_qs.filter(status=Contact.STATUS_IN_PROGRESS).count(),
            'responded': base_qs.filter(status=Contact.STATUS_RESPONDED).count(),
            'closed': base_qs.filter(status=Contact.STATUS_CLOSED).count(),
            'overdue': base_qs.filter(
                follow_up_at__isnull=False,
                follow_up_at__lt=timezone.now()
            ).exclude(status__in=[Contact.STATUS_RESPONDED, Contact.STATUS_CLOSED]).count(),
        },
    }
    return render(request, 'panel/inbox.html', context)


@login_required(login_url='panel:login')
@user_passes_test(is_staff_user, login_url='panel:login')
def panel_inbox_detail(request, pk):
    """Detalle y gestion de una solicitud del buzon."""
    contact = get_object_or_404(Contact.objects.select_related('property', 'assigned_to'), pk=pk)
    staff_users = get_user_model().objects.filter(is_staff=True, is_active=True).order_by('username')

    if not contact.is_read:
        contact.is_read = True
        if contact.status == Contact.STATUS_NEW:
            contact.status = Contact.STATUS_IN_PROGRESS
        contact.save(update_fields=['is_read', 'status', 'updated_at'])

    if request.method == 'POST':
        action = request.POST.get('action', '')

        if action == 'save_details':
            status = request.POST.get('status', '').strip()
            priority = request.POST.get('priority', '').strip()
            assigned_to_id = request.POST.get('assigned_to', '').strip()
            follow_up_raw = request.POST.get('follow_up_at', '').strip()
            internal_summary = request.POST.get('internal_summary', '').strip()

            if status in dict(Contact.STATUS_CHOICES):
                contact.status = status

            if priority in dict(Contact.PRIORITY_CHOICES):
                contact.priority = priority

            if assigned_to_id:
                contact.assigned_to = get_user_model().objects.filter(
                    pk=assigned_to_id,
                    is_staff=True,
                    is_active=True
                ).first()
            else:
                contact.assigned_to = None

            if follow_up_raw:
                dt = parse_datetime(follow_up_raw)
                if dt and timezone.is_naive(dt):
                    dt = timezone.make_aware(dt, timezone.get_current_timezone())
                contact.follow_up_at = dt
            else:
                contact.follow_up_at = None

            contact.internal_summary = internal_summary
            contact.is_read = True

            if contact.status in [Contact.STATUS_RESPONDED, Contact.STATUS_CLOSED]:
                contact.is_responded = True
                if not contact.responded_at:
                    contact.responded_at = timezone.now()
            else:
                contact.is_responded = False
                if contact.status != Contact.STATUS_CLOSED:
                    contact.responded_at = None

            contact.save()
            messages.success(request, 'Solicitud actualizada correctamente.')

        elif action == 'add_note':
            note_text = request.POST.get('note', '').strip()
            if note_text:
                ContactNote.objects.create(
                    contact=contact,
                    author=request.user,
                    note=note_text
                )
                messages.success(request, 'Nota agregada.')
            else:
                messages.warning(request, 'Escribe una nota antes de guardar.')

        elif action == 'mark_read':
            contact.is_read = True
            if contact.status == Contact.STATUS_NEW:
                contact.status = Contact.STATUS_IN_PROGRESS
            contact.save(update_fields=['is_read', 'status', 'updated_at'])
            messages.success(request, 'Solicitud marcada como leida.')
        elif action == 'mark_unread':
            contact.is_read = False
            if contact.status == Contact.STATUS_IN_PROGRESS:
                contact.status = Contact.STATUS_NEW
            contact.save(update_fields=['is_read', 'status', 'updated_at'])
            messages.success(request, 'Solicitud marcada como no leida.')
        elif action == 'mark_responded':
            contact.is_read = True
            contact.is_responded = True
            contact.status = Contact.STATUS_RESPONDED
            contact.responded_at = timezone.now()
            contact.save(update_fields=['is_read', 'is_responded', 'status', 'responded_at', 'updated_at'])
            messages.success(request, 'Solicitud marcada como respondida.')
        elif action == 'mark_pending':
            contact.is_read = True
            contact.is_responded = False
            contact.status = Contact.STATUS_IN_PROGRESS
            contact.responded_at = None
            contact.save(update_fields=['is_read', 'is_responded', 'status', 'responded_at', 'updated_at'])
            messages.success(request, 'Solicitud marcada en seguimiento.')
        elif action == 'mark_closed':
            contact.status = Contact.STATUS_CLOSED
            contact.is_read = True
            contact.is_responded = True
            if not contact.responded_at:
                contact.responded_at = timezone.now()
            contact.save(update_fields=['status', 'is_read', 'is_responded', 'responded_at', 'updated_at'])
            messages.success(request, 'Solicitud cerrada.')

        return redirect('panel:inbox_detail', pk=contact.pk)

    context = {
        'contact': contact,
        'staff_users': staff_users,
        'status_choices': Contact.STATUS_CHOICES,
        'priority_choices': Contact.PRIORITY_CHOICES,
        'notes': contact.notes.select_related('author').all(),
    }
    return render(request, 'panel/inbox_detail.html', context)

