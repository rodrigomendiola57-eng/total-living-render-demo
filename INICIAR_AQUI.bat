@echo off
echo ========================================
echo    TOTAL LIVING - INICIO FORZADO
echo ========================================
echo.

cd /d "C:\TOTAL LIVING"
echo Directorio: %CD%
echo.

echo Iniciando servidor en puerto 8080...
echo URL: http://127.0.0.1:8080/
echo.

python manage.py runserver 8080 --settings=total_living.settings.development

pause
