from django.contrib import admin
from .models import Development, DevelopmentImage

class DevelopmentImageInline(admin.TabularInline):
    model = DevelopmentImage
    extra = 1

@admin.register(Development)
class DevelopmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'total_units', 'available_units', 'price_from', 'is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured', 'city', 'state']
    search_fields = ['name', 'location', 'city']
    inlines = [DevelopmentImageInline]
    
@admin.register(DevelopmentImage)
class DevelopmentImageAdmin(admin.ModelAdmin):
    list_display = ['development', 'is_main', 'order']
    list_filter = ['is_main', 'development']
