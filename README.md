# Total Living - Sistema Web Inmobiliaria

Sistema web completo para gestión de propiedades inmobiliarias.

## Tecnologías

- Python 3.11+
- Django 4.2
- PostgreSQL
- AWS (RDS, S3, Elastic Beanstalk)

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
```

2. Activar entorno virtual:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
copy .env.example .env
# Editar .env con tus configuraciones
```

5. Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Ejecutar servidor de desarrollo:
```bash
# Puerto 8090 (recomendado si 8000 está ocupado)
python manage.py runserver 8090

# O usar el script
.\runserver.ps1  # PowerShell
# o
runserver.bat    # CMD
```

## Estructura del Proyecto

- `total_living/` - Configuración principal del proyecto
- `properties/` - App de propiedades
- `accounts/` - App de usuarios
- `contact/` - App de contacto
- `search/` - App de búsqueda

## Fases del Proyecto

### Fase 1: ✅ Estructura Base
- Configuración inicial del proyecto
- Settings modular (development, staging, production)
- Apps básicas creadas

### Fase 2: Funcionalidades Core (Próximo)
- Modelos de datos
- CRUD de propiedades
- Sistema de búsqueda
- Frontend base

### Fase 3: Preparación AWS
- Configuración para producción
- Dockerización
- Optimizaciones
