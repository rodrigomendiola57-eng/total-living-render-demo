# Script PowerShell para iniciar el servidor desde el directorio correcto
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  INICIANDO SERVIDOR TOTAL LIVING" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Cambiar al directorio del proyecto (FORZAR)
$projectDir = "C:\TOTAL LIVING"
if (-not (Test-Path $projectDir)) {
    Write-Host "ERROR: No se encontro el directorio $projectDir" -ForegroundColor Red
    pause
    exit 1
}

# Forzar cambio de directorio
Set-Location $projectDir
$currentDir = Get-Location
Write-Host "Directorio actual: $currentDir" -ForegroundColor Cyan

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "manage.py")) {
    Write-Host "ERROR: No se encontro manage.py" -ForegroundColor Red
    Write-Host "Asegurate de que el proyecto este en C:\TOTAL LIVING" -ForegroundColor Red
    pause
    exit 1
}

# Verificar base de datos
Write-Host "Verificando base de datos..." -ForegroundColor Yellow
python verificar_db.py
Write-Host ""

# Mostrar información
Write-Host "Base de datos: C:\TOTAL LIVING\db.sqlite3" -ForegroundColor Green
Write-Host ""

# Iniciar servidor
Write-Host "Iniciando servidor en http://127.0.0.1:8090" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Write-Host ""
python manage.py runserver 8090
