from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Contact
from .spam_protection import ratelimit_contact, is_honeypot_triggered
from properties.models import Property


@require_http_methods(["GET", "POST"])
@ratelimit_contact
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
        if getattr(request, 'contact_rate_limited', False):
            messages.error(
                request,
                'Has enviado demasiados mensajes en poco tiempo. Intenta nuevamente en unos minutos.',
            )
            return render(request, 'contact/contact.html', {
                'property': property_obj,
                'form_data': request.POST,
            })

        if is_honeypot_triggered(request):
            # Respuesta neutra: evita dar feedback util a bots.
            messages.success(
                request,
                '¡Gracias por tu mensaje! Nos pondremos en contacto contigo pronto.',
            )
            return redirect('contact:contact')

        # Procesar formulario
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        property_id = request.POST.get('property_id', '').strip()

        if property_id:
            try:
                property_obj = Property.objects.get(pk=property_id, status='disponible')
            except Property.DoesNotExist:
                property_obj = None
        
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
                property=property_obj if property_obj else None,
                status=Contact.STATUS_NEW,
                source='sitio_web'
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


@require_http_methods(["GET", "POST"])
@ratelimit_contact
def advisory_purchase_view(request):
    """Modulo independiente para asesoria de compra inmobiliaria."""
    if request.method == 'POST':
        if getattr(request, 'contact_rate_limited', False):
            messages.error(
                request,
                'Has enviado demasiadas solicitudes en poco tiempo. Intenta nuevamente en unos minutos.',
            )
            return render(request, 'contact/advisory_purchase.html', {
                'form_data': request.POST,
            })

        if is_honeypot_triggered(request):
            messages.success(
                request,
                '¡Gracias por tu solicitud! Un asesor de compra te contactara pronto.',
            )
            return redirect('contact:advisory_purchase')

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        property_type = request.POST.get('property_type', '').strip()
        budget = request.POST.get('budget', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not city:
            messages.error(request, 'Por favor completa los campos requeridos para la asesoria de compra.')
            return render(request, 'contact/advisory_purchase.html', {
                'form_data': request.POST,
            })

        composed_message = (
            f"Ciudad o zona de interes: {city}\n"
            f"Tipo de propiedad: {property_type or 'Sin especificar'}\n"
            f"Presupuesto estimado: {budget or 'Sin especificar'}\n\n"
            f"Detalle del cliente:\n{message or 'Sin comentarios adicionales.'}"
        )

        try:
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone if phone else '',
                subject='Asesoria de compra inmobiliaria',
                message=composed_message,
                status=Contact.STATUS_NEW,
                source='asesoria_compra'
            )

            messages.success(
                request,
                '¡Solicitud enviada! Te contactaremos para iniciar tu asesoria de compra.',
            )
            return redirect('contact:advisory_purchase')
        except Exception:
            messages.error(request, 'Hubo un error al enviar tu solicitud. Intenta nuevamente.')

    return render(request, 'contact/advisory_purchase.html')


@require_http_methods(["GET", "POST"])
@ratelimit_contact
def advisory_sale_view(request):
    """Modulo independiente para captar propietarios que quieren vender/anunciar."""
    if request.method == 'POST':
        if getattr(request, 'contact_rate_limited', False):
            messages.error(
                request,
                'Has enviado demasiadas solicitudes en poco tiempo. Intenta nuevamente en unos minutos.',
            )
            return render(request, 'contact/advisory_sale.html', {
                'form_data': request.POST,
            })

        if is_honeypot_triggered(request):
            messages.success(
                request,
                '¡Gracias por tu solicitud! Un asesor de venta te contactara pronto.',
            )
            return redirect('contact:advisory_sale')

        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        city = request.POST.get('city', '').strip()
        property_type = request.POST.get('property_type', '').strip()
        estimated_price = request.POST.get('estimated_price', '').strip()
        sale_urgency = request.POST.get('sale_urgency', '').strip()
        exclusive_interest = request.POST.get('exclusive_interest', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not city:
            messages.error(request, 'Por favor completa los campos requeridos para la asesoria de venta.')
            return render(request, 'contact/advisory_sale.html', {
                'form_data': request.POST,
            })

        composed_message = (
            f"Ciudad o zona del inmueble: {city}\n"
            f"Tipo de propiedad: {property_type or 'Sin especificar'}\n"
            f"Valor estimado: {estimated_price or 'Sin especificar'}\n"
            f"Urgencia de venta: {sale_urgency or 'Sin especificar'}\n"
            f"Interes en exclusiva: {exclusive_interest or 'Sin especificar'}\n\n"
            f"Detalle del propietario:\n{message or 'Sin comentarios adicionales.'}"
        )

        try:
            Contact.objects.create(
                name=name,
                email=email,
                phone=phone if phone else '',
                subject='Asesoria de venta inmobiliaria',
                message=composed_message,
                status=Contact.STATUS_NEW,
                source='asesoria_venta'
            )

            messages.success(
                request,
                '¡Solicitud enviada! Te contactaremos para ayudarte a vender tu propiedad.',
            )
            return redirect('contact:advisory_sale')
        except Exception:
            messages.error(request, 'Hubo un error al enviar tu solicitud. Intenta nuevamente.')

    return render(request, 'contact/advisory_sale.html')
