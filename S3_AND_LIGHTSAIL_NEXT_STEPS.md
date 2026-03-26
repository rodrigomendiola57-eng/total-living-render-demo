# Conectar S3 y preparar Lightsail (pasos rápidos)

## A) Conectar S3 en local Docker
1. Copia plantilla:
   ```powershell
   copy .env.production.example .env.production
   ```
2. Edita `.env.production`:
   - `USE_S3=True`
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`
   - Mantén `SERVE_LOCAL_MEDIA=True` solo para pruebas de transición.
3. Reinicia stack:
   ```powershell
   docker compose --env-file .env.production up -d --build
   ```
4. Verifica subida nueva de imagen desde panel.

## B) Migrar media histórica a S3
- Prueba en seco:
  ```powershell
  .\scripts\s3_media_sync.ps1 -BucketName "TU_BUCKET" -DryRun
  ```
- Ejecuta real:
  ```powershell
  .\scripts\s3_media_sync.ps1 -BucketName "TU_BUCKET"
  ```

## C) Preflight para Lightsail
- [ ] Docker y Compose instalados
- [ ] `.env.production` listo con valores reales
- [ ] `USE_S3=True`
- [ ] `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`
- [ ] `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` con dominio real
- [ ] `docker compose up -d --build`
- [ ] `migrate`, `collectstatic`, `createsuperuser`
- [ ] Smoke test completo (home, panel, contacto, imágenes)
