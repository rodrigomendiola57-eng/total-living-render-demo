from django.db import models
from django.utils import timezone

class Development(models.Model):
    OPERATION_CHOICES = [
        ('venta', 'Venta'),
        ('renta', 'Renta'),
        ('venta_renta', 'Venta y Renta'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nombre del Desarrollo")
    description = models.TextField(verbose_name="Descripción")
    location = models.CharField(max_length=200, verbose_name="Ubicación")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    state = models.CharField(max_length=100, verbose_name="Estado")
    google_maps_url = models.URLField(max_length=500, blank=True, verbose_name="URL de Google Maps")
    operation_type = models.CharField(max_length=20, choices=OPERATION_CHOICES, default='venta', verbose_name="Tipo de Operación")
    total_units = models.IntegerField(verbose_name="Total de Unidades", default=0)
    available_units = models.IntegerField(verbose_name="Unidades Disponibles", default=0)
    price_from = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Precio Desde")
    delivery_date = models.DateField(verbose_name="Fecha de Entrega", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    is_featured = models.BooleanField(default=False, verbose_name="Destacado")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha de Creación")
    
    class Meta:
        verbose_name = "Desarrollo"
        verbose_name_plural = "Desarrollos"
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return self.name
    
    def get_operation_type_display_custom(self):
        return dict(self.OPERATION_CHOICES).get(self.operation_type, '')
    
    def get_main_image(self):
        """Obtener la imagen principal del desarrollo"""
        return self.images.filter(is_main=True).first() or self.images.first()

class DevelopmentImage(models.Model):
    development = models.ForeignKey(Development, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='developments/', verbose_name="Imagen")
    is_main = models.BooleanField(default=False, verbose_name="Imagen Principal")
    order = models.IntegerField(default=0, verbose_name="Orden")
    
    class Meta:
        verbose_name = "Imagen de Desarrollo"
        verbose_name_plural = "Imágenes de Desarrollo"
        ordering = ['-is_main', 'order']  # Principal primero, luego por orden
    
    def __str__(self):
        return f"Imagen de {self.development.name}"
