# Roles del stack (pre-deploy y producción)

## Aplicación y contenedores
- `Django`: lógica de negocio, panel, API web y templates.
- `Gunicorn`: servidor WSGI que ejecuta Django en producción.
- `Dockerfile`: define cómo construir la imagen de la app.
- `docker-compose.yml`: orquesta servicios (`web` y `db`) en local/predeploy.

## Datos y archivos
- `PostgreSQL` (servicio `db`): base de datos principal (ya no SQLite en runtime Docker).
- `S3`: almacenamiento de media/estáticos para producción cuando `USE_S3=True`.
- `Whitenoise`: sirve estáticos en modo sin S3 (predeploy local o fallback).

## Seguridad y configuración
- `.env.production`: configuración sensible (NO subir a git).
- `.env.production.example`: plantilla compartible sin secretos.
- `production.py`: activa seguridad, SSL/cookies seguras, y switch de S3.
- `IAM`: permisos mínimos para que Django suba/lea archivos en S3.

## Infraestructura AWS
- `Lightsail`: servidor económico para correr Docker Compose.
- `Nginx + Let's Encrypt` (siguiente fase): proxy HTTPS y certificados.

## Flujo recomendado
1. Local predeploy: `USE_S3=False` + Docker + validación funcional.
2. Conectar S3 en local: `USE_S3=True`, credenciales IAM, pruebas de subida.
3. Migrar `media/` existente a S3 con `aws s3 sync`.
4. Subir a Lightsail y repetir smoke tests.
