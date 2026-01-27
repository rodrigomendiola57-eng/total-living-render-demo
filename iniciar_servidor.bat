@echo off
REM Script para iniciar el servidor desde el directorio correcto
echo ========================================
echo   INICIANDO SERVIDOR TOTAL LIVING
echo ========================================
echo.

REM Cambiar al directorio del proyecto
cd /d "C:\TOTAL LIVING"

REM Verificar que estamos en el directorio correcto
if not exist "manage.py" (
    echo ERROR: No se encontro manage.py
    echo Asegurate de que el proyecto este en C:\TOTAL LIVING
    pause
    exit /b 1
)

REM Verificar base de datos
echo Verificando base de datos...
python verificar_db.py
echo.

REM Iniciar servidor
echo Iniciando servidor en http://127.0.0.1:8090
echo Presiona Ctrl+C para detener el servidor
echo.
python manage.py runserver 8090
