@echo off
echo ========================================
echo   TOTAL LIVING - Iniciando Servidor
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist venv\Scripts\activate.bat (
    echo Activando entorno virtual...
    call venv\Scripts\activate.bat
) else (
    echo Advertencia: No se encontro entorno virtual
)

echo.
echo Iniciando servidor en puerto 8090...
echo.
echo Accede a: http://localhost:8090
echo.
echo Presiona Ctrl+C para detener el servidor
echo ========================================
echo.

python manage.py runserver 8090
