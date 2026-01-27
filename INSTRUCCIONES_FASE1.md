# ✅ FASE 1 COMPLETADA - Instrucciones de Configuración

## 📋 Resumen de lo Creado

✅ Estructura completa del proyecto Django
✅ Configuración modular de settings (development, staging, production)
✅ 4 Apps creadas: properties, accounts, contact, search
✅ URLs y views básicas configuradas
✅ Archivos de configuración (.gitignore, requirements.txt, README.md)
✅ Preparado para AWS (configuración de producción lista)

## 🚀 Próximos Pasos para Comenzar

### 1. Instalar Dependencias

```powershell
# Activar entorno virtual (si no está activo)
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

```powershell
# Generar archivo .env con SECRET_KEY automática
python setup_env.py
```

O crea manualmente el archivo `.env` copiando `.env.example` y generando una SECRET_KEY con:
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3. Ejecutar Migraciones

```powershell
python manage.py migrate
```

### 4. Crear Superusuario (Opcional)

```powershell
python manage.py createsuperuser
```

### 5. Ejecutar Servidor de Desarrollo

**Opción 1: Usar el script (puerto 8080)**
```powershell
# Windows PowerShell
.\runserver.ps1

# O Windows CMD
runserver.bat
```

**Opción 2: Especificar puerto manualmente**
```powershell
# Puerto 8080 (recomendado)
python manage.py runserver 8080

# O cualquier otro puerto (ej: 3000, 5000, 9000)
python manage.py runserver 3000
```

Abre tu navegador en: http://127.0.0.1:8080/

## 📁 Estructura del Proyecto

```
TOTAL LIVING/
├── .gitignore
├── requirements.txt
├── README.md
├── setup_env.py
├── manage.py
├── total_living/          # Configuración principal
│   ├── settings/          # Settings modular
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── staging.py
│   │   └── production.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── properties/            # App de propiedades
├── accounts/              # App de usuarios
├── contact/               # App de contacto
├── search/                # App de búsqueda
├── static/                # Archivos estáticos
├── media/                 # Archivos de medios
└── templates/             # Plantillas HTML
```

## 🔧 Configuración por Entornos

### Desarrollo (Actual)
- Base de datos: SQLite
- DEBUG: True
- Archivos estáticos: WhiteNoise
- Email: Consola

### Producción (AWS)
- Base de datos: PostgreSQL (RDS)
- DEBUG: False
- Archivos estáticos/media: S3
- Seguridad: HTTPS, cookies seguras
- Email: SMTP configurado

## ⚠️ Notas Importantes

1. **SECRET_KEY**: Nunca compartas tu archivo `.env` - está en `.gitignore`
2. **Base de Datos**: En desarrollo usa SQLite. Para producción necesitarás PostgreSQL
3. **Dependencias de Producción**: Las dependencias de AWS están comentadas en `requirements.txt`. Descoméntalas cuando vayas a producción
4. **Settings**: El proyecto detecta automáticamente el entorno según la variable `ENVIRONMENT` en `.env`

## 🎯 Próxima Fase

**Fase 2: Funcionalidades Core**
- Modelos de datos (Property, PropertyImage, etc.)
- CRUD completo de propiedades
- Sistema de búsqueda avanzada
- Frontend con templates

## 🐛 Solución de Problemas

### Error: "No module named 'decouple'"
```powershell
pip install python-decouple
```

### Error: "SECRET_KEY not found"
Ejecuta: `python setup_env.py` para crear el archivo `.env`

### Error al ejecutar migraciones
Asegúrate de que todas las apps estén en `INSTALLED_APPS` en `settings/base.py`

---

**¡Fase 1 completada exitosamente! 🎉**
