from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.conf import settings
from .image_security import validate_image_upload, optimize_image_for_storage


class PropertyType(models.TextChoices):
    """Tipos de propiedades disponibles"""
    CASA = 'casa', 'Casa'
    DEPARTAMENTO = 'departamento', 'Departamento'
    TERRENO = 'terreno', 'Terreno'
    LOCAL = 'local', 'Local Comercial'
    OFICINA = 'oficina', 'Oficina'
    BODEGA = 'bodega', 'Bodega'
    RANCHO = 'rancho', 'Rancho'
    OTRO = 'otro', 'Otro'


class PropertyStatus(models.TextChoices):
    """Estados de la propiedad"""
    DISPONIBLE = 'disponible', 'Disponible'
    VENDIDA = 'vendida', 'Vendida'
    RENTADA = 'rentada', 'Rentada'
    RESERVADA = 'reservada', 'Reservada'
    NO_DISPONIBLE = 'no_disponible', 'No Disponible'


class PropertyProcess(models.TextChoices):
    """Proceso/Etapa de la propiedad en el sistema inmobiliario"""
    EN_BUSQUEDA = 'en_busqueda', 'En Búsqueda'
    EN_NEGOCIACION = 'en_negociacion', 'En Negociación'
    EN_PROCESO_LEGAL = 'en_proceso_legal', 'En Proceso Legal'
    EN_ESCRITURACION = 'en_escrituracion', 'En Escrituración'
    CERRADO = 'cerrado', 'Cerrado'
    CANCELADO = 'cancelado', 'Cancelado'
    NO_APLICA = 'no_aplica', 'No Aplica'


class PropertyOperation(models.TextChoices):
    """Tipo de operación"""
    VENTA = 'venta', 'Venta'
    RENTA = 'renta', 'Renta'
    VENTA_RENTA = 'venta_renta', 'Venta o Renta'


class Property(models.Model):
    """Modelo principal para propiedades inmobiliarias"""
    FINANCING_BANK = 'credito_bancario'
    FINANCING_INFONAVIT = 'infonavit'
    FINANCING_FOVISSSTE = 'fovissste'
    FINANCING_COFINAVIT = 'cofinavit'
    FINANCING_APOYO_INFONAVIT = 'apoyo_infonavit'
    FINANCING_INFONAVIT_TOTAL = 'infonavit_total'
    FINANCING_FOVISSSTE_PARA_TODOS = 'fovissste_para_todos'
    FINANCING_ISSFAM = 'issfam'
    FINANCING_COOPERATIVE = 'cooperativa_caja_popular'
    FINANCING_SOFOM = 'sofom'
    FINANCING_LEASE_OPTION = 'arrendamiento_opcion_compra'
    FINANCING_OWNER_DIRECT = 'financiamiento_directo_propietario'
    FINANCING_CHOICES = [
        (FINANCING_BANK, 'Crédito hipotecario bancario'),
        (FINANCING_INFONAVIT, 'INFONAVIT'),
        (FINANCING_FOVISSSTE, 'FOVISSSTE'),
        (FINANCING_COFINAVIT, 'COFINAVIT'),
        (FINANCING_APOYO_INFONAVIT, 'Apoyo Infonavit'),
        (FINANCING_INFONAVIT_TOTAL, 'Infonavit Total'),
        (FINANCING_FOVISSSTE_PARA_TODOS, 'FOVISSSTE para Todos'),
        (FINANCING_ISSFAM, 'ISSFAM'),
        (FINANCING_COOPERATIVE, 'Cooperativa / Caja Popular'),
        (FINANCING_SOFOM, 'SOFOM / financiera no bancaria'),
        (FINANCING_LEASE_OPTION, 'Arrendamiento con opción a compra'),
        (FINANCING_OWNER_DIRECT, 'Financiamiento directo con propietario'),
    ]
    
    # Información básica
    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título descriptivo de la propiedad'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        blank=True,
        verbose_name='Slug',
        help_text='URL amigable (se genera automáticamente)'
    )
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada de la propiedad'
    )
    
    # Tipo y operación
    property_type = models.CharField(
        max_length=20,
        choices=PropertyType.choices,
        default=PropertyType.CASA,
        verbose_name='Tipo de Propiedad'
    )
    operation_type = models.CharField(
        max_length=20,
        choices=PropertyOperation.choices,
        default=PropertyOperation.VENTA,
        verbose_name='Tipo de Operación'
    )
    status = models.CharField(
        max_length=20,
        choices=PropertyStatus.choices,
        default=PropertyStatus.DISPONIBLE,
        verbose_name='Estado'
    )
    process = models.CharField(
        max_length=30,
        choices=PropertyProcess.choices,
        default=PropertyProcess.EN_BUSQUEDA,
        verbose_name='Proceso/Etapa',
        help_text='Etapa actual en el proceso de venta/renta'
    )
    
    # Precio
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Precio',
        help_text='Precio en moneda local'
    )
    currency = models.CharField(
        max_length=3,
        default='MXN',
        verbose_name='Moneda',
        help_text='Código de moneda (MXN, USD, etc.)'
    )
    
    # Ubicación
    address = models.CharField(
        max_length=255,
        verbose_name='Dirección'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Ciudad'
    )
    region = models.ForeignKey(
        'regions.Region',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='properties',
        verbose_name='Región'
    )
    state = models.CharField(
        max_length=100,
        verbose_name='Estado/Provincia'
    )
    zip_code = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Código Postal'
    )
    country = models.CharField(
        max_length=100,
        default='México',
        verbose_name='País'
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Latitud',
        help_text='Coordenada GPS'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name='Longitud',
        help_text='Coordenada GPS'
    )
    google_maps_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name='URL Google Maps',
        help_text='Link de Google Maps de la ubicación'
    )
    
    # Características físicas
    bedrooms = models.PositiveIntegerField(
        default=0,
        verbose_name='Recámaras',
        help_text='Número de recámaras'
    )
    bathrooms = models.PositiveIntegerField(
        default=0,
        verbose_name='Baños',
        help_text='Número de baños'
    )
    half_bathrooms = models.PositiveIntegerField(
        default=0,
        verbose_name='Medios Baños',
        help_text='Número de medios baños'
    )
    parking_spaces = models.PositiveIntegerField(
        default=0,
        verbose_name='Estacionamientos',
        help_text='Número de espacios de estacionamiento'
    )
    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Área (m²)',
        help_text='Área total en metros cuadrados'
    )
    construction_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Área de Construcción (m²)',
        help_text='Área construida en metros cuadrados'
    )
    lot_area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        verbose_name='Área de Terreno (m²)',
        help_text='Área del terreno en metros cuadrados'
    )
    floors = models.PositiveIntegerField(
        default=1,
        verbose_name='Niveles',
        help_text='Número de pisos o niveles'
    )
    year_built = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Año de Construcción'
    )
    front_measure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Medida Frente (m)'
    )
    back_measure = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Medida Fondo (m)'
    )
    rooms = models.PositiveIntegerField(
        default=0,
        verbose_name='Ambientes'
    )
    maintenance_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Cuota de Mantenimiento'
    )
    
    # Distribución
    has_sala = models.BooleanField(default=False, verbose_name='Sala')
    has_comedor = models.BooleanField(default=False, verbose_name='Comedor')
    has_cocina = models.BooleanField(default=False, verbose_name='Cocina Integral')
    has_estudio = models.BooleanField(default=False, verbose_name='Estudio')
    has_despensa = models.BooleanField(default=False, verbose_name='Despensa')
    has_cuarto_tv = models.BooleanField(default=False, verbose_name='Cuarto TV')
    has_gimnasio = models.BooleanField(default=False, verbose_name='Gimnasio')
    has_balcon = models.BooleanField(default=False, verbose_name='Balcón')
    has_jardin = models.BooleanField(default=False, verbose_name='Jardín')
    has_patio = models.BooleanField(default=False, verbose_name='Patio')
    has_roof_garden = models.BooleanField(default=False, verbose_name='Roof Garden')
    has_area_lavado = models.BooleanField(default=False, verbose_name='Área de Lavado')
    has_bodega = models.BooleanField(default=False, verbose_name='Bodega')
    
    # Amenidades
    amenity_salon = models.BooleanField(default=False, verbose_name='Salón de Usos Múltiples')
    amenity_vigilancia = models.BooleanField(default=False, verbose_name='Vigilancia 24/7')
    amenity_acceso = models.BooleanField(default=False, verbose_name='Acceso Controlado')
    amenity_areas_verdes = models.BooleanField(default=False, verbose_name='Áreas Verdes')
    amenity_juegos = models.BooleanField(default=False, verbose_name='Juegos Infantiles')
    amenity_gimnasio = models.BooleanField(default=False, verbose_name='Gimnasio')
    amenity_alberca = models.BooleanField(default=False, verbose_name='Alberca')
    amenity_cancha_futbol = models.BooleanField(default=False, verbose_name='Cancha de Fútbol')
    amenity_cancha_tenis = models.BooleanField(default=False, verbose_name='Cancha de Tenis')
    amenity_cancha_basket = models.BooleanField(default=False, verbose_name='Cancha de Basketball')
    amenity_asadores = models.BooleanField(default=False, verbose_name='Zona de Asadores')
    amenity_pet_friendly = models.BooleanField(default=False, verbose_name='Pet Friendly')
    
    # Servicios
    service_agua = models.BooleanField(default=False, verbose_name='Agua')
    service_drenaje = models.BooleanField(default=False, verbose_name='Drenaje')
    service_luz = models.BooleanField(default=False, verbose_name='Luz')
    service_gas = models.BooleanField(default=False, verbose_name='Gas Estacionario')
    service_internet = models.BooleanField(default=False, verbose_name='Internet')
    service_fibra = models.BooleanField(default=False, verbose_name='Fibra Óptica')
    service_cable = models.BooleanField(default=False, verbose_name='TV Cable')
    service_telefono = models.BooleanField(default=False, verbose_name='Línea Telefónica')
    service_cisterna = models.BooleanField(default=False, verbose_name='Cisterna')
    service_hidroneumatico = models.BooleanField(default=False, verbose_name='Hidroneumático')
    service_aire = models.BooleanField(default=False, verbose_name='Aire Acondicionado')
    service_boiler = models.BooleanField(default=False, verbose_name='Boiler')

    # Gestión comercial interna (solo panel/admin)
    is_advisor_exclusive = models.BooleanField(
        default=False,
        verbose_name='Exclusiva de asesor',
        help_text='Solo visible para administración/panel interno'
    )
    exclusive_advisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='exclusive_properties',
        verbose_name='Asesor responsable de la exclusiva'
    )
    financing_options = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Opciones de financiamiento',
        help_text='Solo visible para administración/panel interno'
    )
    
    # Información adicional
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destacada',
        help_text='Mostrar en la página principal'
    )
    is_new = models.BooleanField(
        default=False,
        verbose_name='Nueva',
        help_text='Marcar como propiedad nueva'
    )
    
    # Metadatos
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Publicación'
    )
    
    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['property_type']),
            models.Index(fields=['operation_type']),
            models.Index(fields=['city']),
            models.Index(fields=['is_featured']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.city}"
    
    def save(self, *args, **kwargs):
        """Generar slug automáticamente si no existe"""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """URL absoluta para la propiedad"""
        return reverse('properties:detail', kwargs={'pk': self.pk})
    
    def get_main_image(self):
        """Obtener la imagen principal de la propiedad"""
        prefetched = getattr(self, '_prefetched_objects_cache', {}).get('images')
        if prefetched is not None:
            for image in prefetched:
                if image.is_main:
                    return image
            return prefetched[0] if prefetched else None
        return self.images.filter(is_main=True).first() or self.images.first()
    
    def get_price_display(self):
        """Formatear el precio para mostrar"""
        return f"${self.price:,.2f} {self.currency}"

    def get_financing_options_display(self):
        labels = dict(self.FINANCING_CHOICES)
        return [labels.get(code, code) for code in (self.financing_options or [])]


class PropertyImage(models.Model):
    """Modelo para imágenes de propiedades"""
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Propiedad'
    )
    image = models.ImageField(
        upload_to='properties/',
        verbose_name='Imagen',
        help_text='Imagen de la propiedad'
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name='Imagen Principal',
        help_text='Marcar como imagen principal'
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name='Texto Alternativo',
        help_text='Descripción de la imagen para accesibilidad'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    
    class Meta:
        verbose_name = 'Imagen de Propiedad'
        verbose_name_plural = 'Imágenes de Propiedades'
        ordering = ['is_main', 'order', '-created_at']
    
    def __str__(self):
        return f"Imagen de {self.property.title}"

    def save(self, *args, **kwargs):
        if self.image:
            validate_image_upload(self.image)
            self.image = optimize_image_for_storage(self.image, max_width=1920)

        if self.is_main and self.property_id:
            PropertyImage.objects.filter(
                property_id=self.property_id,
                is_main=True,
            ).exclude(pk=self.pk).update(is_main=False)

        super().save(*args, **kwargs)


class CarouselSlide(models.Model):
    """Modelo para gestionar slides del carrusel principal"""
    
    title = models.CharField(
        max_length=200,
        verbose_name='Título',
        help_text='Título del slide'
    )
    subtitle = models.CharField(
        max_length=300,
        blank=True,
        verbose_name='Subtítulo',
        help_text='Subtítulo o descripción breve'
    )
    image = models.ImageField(
        upload_to='carousel/',
        verbose_name='Imagen',
        help_text='Imagen del slide (recomendado: 1920x1080px)'
    )
    link_url = models.URLField(
        blank=True,
        null=True,
        verbose_name='URL de Enlace',
        help_text='URL a la que redirigir al hacer clic (opcional)'
    )
    link_text = models.CharField(
        max_length=100,
        blank=True,
        default='Ver Más',
        verbose_name='Texto del Botón',
        help_text='Texto del botón de acción'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo',
        help_text='Mostrar este slide en el carrusel'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Orden',
        help_text='Orden de visualización (menor número = primero)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de Actualización'
    )
    
    class Meta:
        verbose_name = 'Slide del Carrusel'
        verbose_name_plural = 'Slides del Carrusel'
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return f"{self.title} ({'Activo' if self.is_active else 'Inactivo'})"
    
    def save(self, *args, **kwargs):
        """Optimizar imagen antes de guardar."""
        if self.image:
            validate_image_upload(self.image)
            self.image = optimize_image_for_storage(self.image, max_width=1920)

        super().save(*args, **kwargs)


class PropertyFeature(models.Model):
    """Modelo para características adicionales de propiedades"""
    
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nombre',
        help_text='Nombre de la característica (ej: Piscina, Jardín, etc.)'
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Icono',
        help_text='Clase de icono (FontAwesome, Material Icons, etc.)'
    )
    
    class Meta:
        verbose_name = 'Característica'
        verbose_name_plural = 'Características'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class PropertyFeatureRelation(models.Model):
    """Relación entre propiedades y características"""
    
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='features',
        verbose_name='Propiedad'
    )
    feature = models.ForeignKey(
        PropertyFeature,
        on_delete=models.CASCADE,
        verbose_name='Característica'
    )
    
    class Meta:
        verbose_name = 'Característica de Propiedad'
        verbose_name_plural = 'Características de Propiedades'
        unique_together = ['property', 'feature']
    
    def __str__(self):
        return f"{self.property.title} - {self.feature.name}"
