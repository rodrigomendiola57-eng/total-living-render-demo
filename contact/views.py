from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Contact
from properties.models import Property


@require_http_methods(["GET", "POST"])
def contact_view(request):
    """Vista para formulario de contacto"""
    property_id = request.GET.get('property', None)
    property_obj = None
    
    if property_id:
        try:
            property_obj = Property.objects.get(pk=property_id, status='disponible')
        except Property.DoesNotExist:
            pass
    
    if request.method == 'POST':
        # Procesar formulario
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        property_id = request.POST.get('property_id', '')
        
        # Validación básica
        if not name or not email or not message:
            messages.error(request, 'Por favor completa todos los campos requeridos.')
            return render(request, 'contact/contact.html', {
                'property': property_obj,
                'form_data': request.POST
            })
        
        # Crear contacto
        try:
            contact = Contact.objects.create(
                name=name,
                email=email,
                phone=phone if phone else '',
                subject=subject if subject else 'Consulta desde sitio web',
                message=message,
                property=property_obj if property_obj else None
            )
            
            messages.success(
                request, 
                '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.'
            )
            return redirect('contact:contact')
        except Exception as e:
            messages.error(request, 'Hubo un error al enviar tu mensaje. Por favor intenta de nuevo.')
    
    return render(request, 'contact/contact.html', {
        'property': property_obj
    })
