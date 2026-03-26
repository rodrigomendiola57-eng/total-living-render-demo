# Fase 1 - Previo a Lightsail

Esta fase deja el proyecto listo para arrancar con Docker (web + postgres) y validar flujo base antes del despliegue final.

## 1) Preparar variables

1. Copia la plantilla:
   ```powershell
   copy .env.production.example .env.production
   ```
2. Edita `.env.production` con valores reales:
   - `SECRET_KEY`
   - `POSTGRES_PASSWORD`
   - `AWS_*`
   - `APP_PORT` (si `8001` está ocupado, usa `8090` o `8002`)
   - `USE_S3`:
     - `False` para validar local sin AWS
     - `True` cuando ya tengas bucket y credenciales AWS
   - `SECURE_SSL_REDIRECT`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`:
     - `False` en pruebas locales HTTP
     - `True` en producción con HTTPS
   - `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS`
   - rutas privadas `ADMIN_URL_PATH`, `PANEL_URL_PATH`

## 2) Levantar stack local de validación

```powershell
docker compose --env-file .env.production up -d --build
```

## 3) Inicializar Django dentro del contenedor

```powershell
docker compose --env-file .env.production exec web python manage.py migrate --noinput
docker compose --env-file .env.production exec web python manage.py collectstatic --noinput
docker compose --env-file .env.production exec web python manage.py createsuperuser
```

## 4) Pruebas mínimas

- Home: http://127.0.0.1:8090/ (o el valor de `APP_PORT`)
- Contacto: http://127.0.0.1:8090/contact/ (o el valor de `APP_PORT`)
- Panel login: usa la ruta privada definida en `PANEL_URL_PATH`
- Admin login: usa la ruta privada definida en `ADMIN_URL_PATH`

## 5) Comandos útiles

```powershell
# Ver logs
docker compose logs -f web

# Parar stack
docker compose --env-file .env.production down

# Parar y borrar volúmenes de db local
docker compose --env-file .env.production down -v
```

## Notas

- Este compose está pensado para validación previa y entorno de costo bajo.
- Para producción real en dominio, se recomienda agregar Nginx + SSL (Let's Encrypt) en Lightsail.
- No subas `.env.production` al repositorio.
- Si activas `USE_S3=True`, verifica antes que el bucket exista y el IAM tenga permisos de lectura/escritura.
- El contenedor `web` monta `./media` y `./staticfiles` para no perder archivos locales al reiniciar.
- Si ya tienes imágenes históricas en `media/`, quedarán visibles en Docker con este montaje.
