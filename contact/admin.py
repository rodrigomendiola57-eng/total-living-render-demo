from django.contrib import admin
from django.utils.html import format_html
from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Administración de contactos"""
    
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'subject',
        'property_link',
        'is_read',
        'is_responded',
        'created_at'
    ]
    
    list_filter = [
        'is_read',
        'is_responded',
        'created_at',
        'property'
    ]
    
    search_fields = [
        'name',
        'email',
        'phone',
        'subject',
        'message',
        'property__title'
    ]
    
    readonly_fields = [
        'name',
        'email',
        'phone',
        'subject',
        'message',
        'property',
        'created_at',
        'responded_at'
    ]
    
    fieldsets = (
        ('Información del Contacto', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Mensaje', {
            'fields': ('subject', 'message')
        }),
        ('Propiedad Relacionada', {
            'fields': ('property',)
        }),
        ('Estado', {
            'fields': ('is_read', 'is_responded')
        }),
        ('Fechas', {
            'fields': ('created_at', 'responded_at'),
            'classes': ('collapse',)
        }),
    )
    
    list_editable = ['is_read', 'is_responded']
    
    date_hierarchy = 'created_at'
    
    list_per_page = 25
    
    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_responded']
    
    def property_link(self, obj):
        """Mostrar enlace a la propiedad"""
        if obj.property:
            return format_html(
                '<a href="/admin/properties/property/{}/change/">{}</a>',
                obj.property.id,
                obj.property.title
            )
        return "-"
    property_link.short_description = 'Propiedad'
    
    def mark_as_read(self, request, queryset):
        """Marcar contactos como leídos"""
        queryset.update(is_read=True)
        self.message_user(request, f'{queryset.count()} contactos marcados como leídos.')
    mark_as_read.short_description = 'Marcar como leído'
    
    def mark_as_unread(self, request, queryset):
        """Marcar contactos como no leídos"""
        queryset.update(is_read=False)
        self.message_user(request, f'{queryset.count()} contactos marcados como no leídos.')
    mark_as_unread.short_description = 'Marcar como no leído'
    
    def mark_as_responded(self, request, queryset):
        """Marcar contactos como respondidos"""
        from django.utils import timezone
        queryset.update(is_responded=True, responded_at=timezone.now())
        self.message_user(request, f'{queryset.count()} contactos marcados como respondidos.')
    mark_as_responded.short_description = 'Marcar como respondido'
