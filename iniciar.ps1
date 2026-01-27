# Script mejorado para iniciar el servidor de Django
# Verifica que todo esté configurado correctamente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   TOTAL LIVING - INICIO DEL SERVIDOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del proyecto
Set-Location "C:\TOTAL LIVING"

# Verificar propiedades en la base de datos
Write-Host "Verificando base de datos..." -ForegroundColor Yellow
$propCount = python -c "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'total_living.settings.development'); import django; django.setup(); from properties.models import Property; print(Property.objects.count())"

if ($propCount -eq "0") {
    Write-Host "No hay propiedades en la base de datos." -ForegroundColor Red
    Write-Host "Creando propiedades de demostracion..." -ForegroundColor Yellow
    python crear_propiedades_demo.py
    Write-Host ""
} else {
    Write-Host "Base de datos OK: $propCount propiedades encontradas" -ForegroundColor Green
    Write-Host ""
}

# Iniciar servidor
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INICIANDO SERVIDOR..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tu sitio estara disponible en:" -ForegroundColor Green
Write-Host "  http://127.0.0.1:8080/" -ForegroundColor White -BackgroundColor DarkGreen
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 8080
