# SCRIPT DEFINITIVO - FUERZA EL DIRECTORIO Y CONFIGURACION CORRECTA
Write-Host "========================================" -ForegroundColor Red
Write-Host "   FORZANDO CONFIGURACION CORRECTA" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""

# PASO 1: FORZAR DIRECTORIO CORRECTO
$targetDir = "C:\TOTAL LIVING"
Write-Host "1. Cambiando a directorio: $targetDir" -ForegroundColor Yellow
Set-Location $targetDir
$currentDir = Get-Location
Write-Host "   Directorio actual: $currentDir" -ForegroundColor Green

if ($currentDir.Path -ne $targetDir) {
    Write-Host "   ERROR: No se pudo cambiar al directorio correcto!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# PASO 2: LIMPIAR VARIABLES DE ENTORNO DE OTROS PROYECTOS DJANGO
Write-Host "2. Limpiando variables de entorno..." -ForegroundColor Yellow
$env:DJANGO_SETTINGS_MODULE = $null
$env:PYTHONPATH = $null
Write-Host "   Variables limpiadas" -ForegroundColor Green
Write-Host ""

# PASO 3: VERIFICAR QUE EXISTE urls.py
Write-Host "3. Verificando archivos criticos..." -ForegroundColor Yellow
$urlsFile = Join-Path $targetDir "total_living\urls.py"
if (Test-Path $urlsFile) {
    Write-Host "   OK: urls.py encontrado" -ForegroundColor Green
    $urlsContent = Get-Content $urlsFile -Raw
    if ($urlsContent -match "urlpatterns") {
        Write-Host "   OK: urlpatterns definido" -ForegroundColor Green
    } else {
        Write-Host "   ERROR: urlpatterns NO encontrado en urls.py" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "   ERROR: urls.py NO encontrado!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# PASO 4: VERIFICAR BASE DE DATOS
Write-Host "4. Verificando base de datos..." -ForegroundColor Yellow
$dbFile = Join-Path $targetDir "db.sqlite3"
if (Test-Path $dbFile) {
    Write-Host "   OK: Base de datos encontrada" -ForegroundColor Green
} else {
    Write-Host "   ADVERTENCIA: Base de datos no encontrada" -ForegroundColor Yellow
}
Write-Host ""

# PASO 5: INICIAR SERVIDOR CON CONFIGURACION EXPLICITA
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   INICIANDO SERVIDOR" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "URL: http://127.0.0.1:8080/" -ForegroundColor Green -BackgroundColor DarkGreen
Write-Host ""
Write-Host "Si ves el cohete de Django, presiona Ctrl+C y ejecuta:" -ForegroundColor Yellow
Write-Host "  python -c `"from total_living.urls import urlpatterns; print(len(urlpatterns))`"" -ForegroundColor White
Write-Host ""

# Ejecutar con settings explicito
python manage.py runserver 8080 --settings=total_living.settings.development
