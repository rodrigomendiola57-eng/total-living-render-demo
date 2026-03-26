# Pre-Deploy Checklist (Total Living)

Checklist corta y practica para desplegar de forma segura.

## 1) Variables de entorno (obligatorio)

- [ ] `SECRET_KEY` real (no default).
- [ ] `DJANGO_SETTINGS_MODULE=total_living.settings.production`.
- [ ] `ALLOWED_HOSTS` con dominio(s) real(es).
- [ ] `CSRF_TRUSTED_ORIGINS` con `https://...`.
- [ ] `DATABASE_URL` a PostgreSQL (RDS recomendado).
- [ ] Variables AWS S3 (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`) si static/media van a S3.
- [ ] `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS` y settings de cookie seguras confirmados en producción.
- [ ] (Opcional recomendado) Ajustar:
  - [ ] `PANEL_LOGIN_RATELIMIT_IP`
  - [ ] `PANEL_LOGIN_RATELIMIT_USERNAME`
  - [ ] `CONTACT_FORM_RATELIMIT_IP`

## 2) Verificaciones previas de Django

- [ ] Instalar deps: `python -m pip install -r requirements.txt`
- [ ] Verificar deploy: `python manage.py check --deploy`
- [ ] Verificar migraciones pendientes: `python manage.py makemigrations --check --dry-run`
- [ ] Aplicar migraciones: `python manage.py migrate --noinput`

## 3) Archivos estáticos y media

- [ ] Ejecutar `python manage.py collectstatic --noinput`.
- [ ] Comprobar que CSS/JS cargan en dominio final.
- [ ] Comprobar que una imagen nueva de propiedad se sube y se sirve correctamente.

## 4) Pruebas funcionales mínimas

- [ ] Home carga sin errores.
- [ ] Formulario de contacto guarda un registro.
- [ ] Anti-spam contacto:
  - [ ] Honeypot: enviar con `website` lleno no crea error visible.
  - [ ] Rate limit: tras varios envíos muestra bloqueo temporal.
- [ ] Panel login:
  - [ ] Login staff correcto.
  - [ ] Intentos fallidos reiterados se limitan.

## 5) Seguridad operativa mínima

- [ ] HTTPS activo en dominio.
- [ ] Credenciales de BD y AWS no expuestas en logs.
- [ ] `.env` no versionado en git.
- [ ] Usuario admin con contraseña fuerte.
- [ ] Backups de BD habilitados (snapshot/retención).

## 6) Comando de arranque (ejemplo)

```
gunicorn --bind 0.0.0.0:8000 total_living.wsgi:application
```

## 7) Smoke test final (post-deploy)

- [ ] Respuesta `200` en `/`.
- [ ] Respuesta `200` en `/contact/`.
- [ ] Respuesta `302/200` esperada en `/panel/login/`.
- [ ] Sin errores críticos en logs durante primeros minutos.

