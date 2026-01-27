from django import forms
from .models import Property, PropertyImage, PropertyFeature


class PropertyForm(forms.ModelForm):
    """Formulario para crear/editar propiedades"""
    
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'operation_type', 'status',
            'price', 'currency', 'address', 'city', 'state', 'zip_code', 'country',
            'latitude', 'longitude', 'bedrooms', 'bathrooms', 'parking_spaces',
            'area', 'construction_area', 'lot_area', 'floors', 'year_built',
            'is_featured', 'is_new', 'published_at'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Casa moderna en zona residencial'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descripción detallada de la propiedad...'
            }),
            'property_type': forms.Select(attrs={'class': 'form-select'}),
            'operation_type': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'currency': forms.TextInput(attrs={
                'class': 'form-control',
                'maxlength': '3',
                'placeholder': 'MXN'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Calle y número'
            }),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001'
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'parking_spaces': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'construction_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'lot_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            }),
            'floors': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
            'year_built': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1900',
                'max': '2100'
            }),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'published_at': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }
        help_texts = {
            'latitude': 'Coordenada GPS (opcional)',
            'longitude': 'Coordenada GPS (opcional)',
        }


class PropertyImageForm(forms.ModelForm):
    """Formulario para agregar imágenes a una propiedad"""
    
    class Meta:
        model = PropertyImage
        fields = ['image', 'is_main', 'alt_text', 'order']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_main': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'alt_text': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción de la imagen'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
        }
