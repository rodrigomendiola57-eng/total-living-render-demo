from django.db import models
from django.core.validators import EmailValidator


class Contact(models.Model):
    """Modelo para formularios de contacto"""
    
    # Información del contacto
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre completo del contacto'
    )
    email = models.EmailField(
        max_length=255,
        validators=[EmailValidator()],
        verbose_name='Correo Electrónico'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Teléfono',
        help_text='Número de teléfono de contacto'
    )
    
    # Mensaje
    subject = models.CharField(
        max_length=200,
        verbose_name='Asunto',
        help_text='Asunto del mensaje'
    )
    message = models.TextField(
        verbose_name='Mensaje',
        help_text='Contenido del mensaje'
    )
    
    # Relación con propiedad (opcional)
    property = models.ForeignKey(
        'properties.Property',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contacts',
        verbose_name='Propiedad',
        help_text='Propiedad relacionada (si aplica)'
    )
    
    # Estado
    is_read = models.BooleanField(
        default=False,
        verbose_name='Leído',
        help_text='Marcar como leído'
    )
    is_responded = models.BooleanField(
        default=False,
        verbose_name='Respondido',
        help_text='Marcar como respondido'
    )
    
    # Metadatos
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    responded_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Respuesta'
    )
    
    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_read']),
            models.Index(fields=['property']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.subject} ({self.created_at.strftime('%Y-%m-%d')})"
