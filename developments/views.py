from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import models
from .models import Development, DevelopmentImage

def developments_list(request):
    """Vista pública para mostrar todos los desarrollos"""
    operation = request.GET.get('operation', 'all')
    city = request.GET.get('ciudad', '')
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')
    search = request.GET.get('search', '')
    
    developments = Development.objects.filter(is_active=True).prefetch_related('images').order_by('-is_featured', '-created_at')
    
    if operation == 'venta':
        developments = developments.filter(operation_type__in=['venta', 'venta_renta'])
    elif operation == 'renta':
        developments = developments.filter(operation_type__in=['renta', 'venta_renta'])
    
    if city:
        developments = developments.filter(city__icontains=city)
    if precio_min:
        try:
            developments = developments.filter(price_from__gte=float(precio_min))
        except (ValueError, TypeError):
            pass
    if precio_max:
        try:
            developments = developments.filter(price_from__lte=float(precio_max))
        except (ValueError, TypeError):
            pass
    if search:
        developments = developments.filter(name__icontains=search)
    
    context = {
        'developments': developments,
        'title': 'Desarrollos Exclusivos',
        'operation': operation,
        'current_filters': {
            'ciudad': city,
            'precio_min': precio_min,
            'precio_max': precio_max,
            'search': search,
        }
    }
    
    return render(request, 'developments/list.html', context)

def development_detail(request, pk):
    """Vista pública para mostrar el detalle de un desarrollo"""
    development = get_object_or_404(Development, pk=pk, is_active=True)
    
    # Obtener todas las imágenes del desarrollo
    images = development.images.all().order_by('-is_main', 'order')
    
    # Obtener desarrollos relacionados (misma ciudad o estado)
    related_developments = Development.objects.filter(
        is_active=True,
    ).filter(
        models.Q(city=development.city) | models.Q(state=development.state)
    ).exclude(pk=pk).prefetch_related('images')[:4]
    
    context = {
        'development': development,
        'images': images,
        'related_developments': related_developments,
    }
    
    return render(request, 'developments/detail.html', context)

def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_staff_user, login_url='admin:login')
def panel_developments(request):
    """Panel de gestión de desarrollos"""
    developments = Development.objects.all().prefetch_related('images')
    
    context = {
        'developments': developments,
        'title': 'Gestión de Desarrollos',
    }
    
    return render(request, 'developments/panel/list.html', context)

@login_required
@user_passes_test(is_staff_user, login_url='admin:login')
def panel_development_add(request):
    """Agregar nuevo desarrollo"""
    if request.method == 'POST':
        try:
            development = Development(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
                location=request.POST.get('location'),
                city=request.POST.get('city'),
                state=request.POST.get('state'),
                google_maps_url=request.POST.get('google_maps_url', ''),
                operation_type=request.POST.get('operation_type'),
                total_units=int(request.POST.get('total_units') or 0),
                available_units=int(request.POST.get('available_units') or 0),
                price_from=float(request.POST.get('price_from') or 0),
                delivery_date=request.POST.get('delivery_date') or None,
                is_featured='is_featured' in request.POST,
                is_active='is_active' in request.POST,
            )
            development.save()
            
            # Agregar imágenes
            images = request.FILES.getlist('images')
            for idx, image in enumerate(images):
                DevelopmentImage.objects.create(
                    development=development,
                    image=image,
                    is_main=(idx == 0),
                    order=idx
                )
            
            messages.success(request, f'Desarrollo "{development.name}" creado exitosamente.')
            return redirect('developments:panel_list')
        except Exception as e:
            messages.error(request, f'Error al crear desarrollo: {str(e)}')
    
    return render(request, 'developments/panel/add.html', {'title': 'Nuevo Desarrollo'})

@login_required
@user_passes_test(is_staff_user, login_url='admin:login')
def panel_development_edit(request, pk):
    """Editar desarrollo"""
    development = get_object_or_404(Development, pk=pk)
    
    if request.method == 'POST':
        try:
            development.name = request.POST.get('name')
            development.description = request.POST.get('description')
            development.location = request.POST.get('location')
            development.city = request.POST.get('city')
            development.state = request.POST.get('state')
            development.google_maps_url = request.POST.get('google_maps_url', '')
            development.operation_type = request.POST.get('operation_type')
            development.total_units = int(request.POST.get('total_units') or 0)
            development.available_units = int(request.POST.get('available_units') or 0)
            development.price_from = float(request.POST.get('price_from') or 0)
            development.delivery_date = request.POST.get('delivery_date') or None
            development.is_featured = 'is_featured' in request.POST
            development.is_active = 'is_active' in request.POST
            development.save()
            
            # Agregar nuevas imágenes
            images = request.FILES.getlist('images')
            if images:
                current_count = development.images.count()
                for idx, image in enumerate(images):
                    DevelopmentImage.objects.create(
                        development=development,
                        image=image,
                        is_main=False,
                        order=current_count + idx
                    )
            
            messages.success(request, f'Desarrollo "{development.name}" actualizado exitosamente.')
            return redirect('developments:panel_list')
        except Exception as e:
            messages.error(request, f'Error al actualizar desarrollo: {str(e)}')
    
    context = {
        'development': development,
        'title': 'Editar Desarrollo',
    }
    
    return render(request, 'developments/panel/edit.html', context)

@login_required
@user_passes_test(is_staff_user, login_url='admin:login')
def panel_development_delete(request, pk):
    """Eliminar desarrollo"""
    development = get_object_or_404(Development, pk=pk)
    
    if request.method == 'POST':
        name = development.name
        development.delete()
        messages.success(request, f'Desarrollo "{name}" eliminado exitosamente.')
        return redirect('developments:panel_list')
    
    context = {
        'development': development,
        'title': 'Eliminar Desarrollo',
    }
    
    return render(request, 'developments/panel/delete.html', context)

@login_required
@user_passes_test(is_staff_user, login_url='admin:login')
def panel_development_images(request, pk):
    """Gestionar imágenes del desarrollo"""
    development = get_object_or_404(Development, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'upload':
            # Subir nuevas imágenes
            images = request.FILES.getlist('images')
            if images:
                current_count = development.images.count()
                has_main = development.images.filter(is_main=True).exists()
                
                for idx, image_file in enumerate(images):
                    DevelopmentImage.objects.create(
                        development=development,
                        image=image_file,
                        is_main=(not has_main and idx == 0),  # Primera imagen como principal si no hay ninguna
                        order=current_count + idx
                    )
                messages.success(request, f'{len(images)} imagen(es) agregada(s) exitosamente.')
            else:
                messages.warning(request, 'No se seleccionaron imágenes.')
        
        elif action == 'delete':
            image_id = request.POST.get('image_id')
            image = get_object_or_404(DevelopmentImage, pk=image_id, development=development)
            image.delete()
            messages.success(request, 'Imagen eliminada exitosamente.')
        
        elif action == 'set_main':
            image_id = request.POST.get('image_id')
            development.images.update(is_main=False)
            image = get_object_or_404(DevelopmentImage, pk=image_id, development=development)
            image.is_main = True
            image.save()
            messages.success(request, 'Imagen principal actualizada.')
        
        return redirect('developments:panel_images', pk=pk)
    
    context = {
        'development': development,
        'images': development.images.all().order_by('-is_main', 'order'),  # Principal primero, luego por orden
        'title': f'Imágenes de {development.name}',
    }
    
    return render(request, 'developments/panel/images.html', context)

