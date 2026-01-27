# Script PowerShell para iniciar el servidor de desarrollo en puerto 8090
Write-Host "Iniciando servidor Django en http://127.0.0.1:8090" -ForegroundColor Green
python manage.py runserver 8090
