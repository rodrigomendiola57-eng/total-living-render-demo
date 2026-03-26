# AWS Setup Minimo (S3 + Lightsail + PostgreSQL)

Guia corta para preparar infraestructura con costo bajo.

## 1) S3 bucket para media/estaticos

1. Crear bucket (ejemplo: `totalliving-media-prod`).
2. Region sugerida: la misma donde desplegaras la app.
3. Mantener "Block Public Access" activo.
4. En Django usaremos URLs firmadas desactivadas y lectura publica solo por objetos necesarios.

## 2) IAM usuario para Django

Crear un usuario IAM con clave programatica y politica minima al bucket:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::totalliving-media-prod",
        "arn:aws:s3:::totalliving-media-prod/*"
      ]
    }
  ]
}
```

## 3) Lightsail (costo bajo)

1. Crear instancia Ubuntu (2 GB recomendado para iniciar).
2. Instalar Docker + Compose.
3. Clonar repo y copiar `.env.production`.
4. Inicialmente puedes usar PostgreSQL en el mismo `docker-compose` para costo minimo.

## 4) Variables .env en AWS (resumen)

Valores clave al pasar a AWS:

- `USE_S3=True`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_REGION_NAME`
- `SECURE_SSL_REDIRECT=True`
- `SESSION_COOKIE_SECURE=True`
- `CSRF_COOKIE_SECURE=True`
- `ALLOWED_HOSTS` y `CSRF_TRUSTED_ORIGINS` con dominio real HTTPS

## 4.1) Migrar media local a S3 (antes de activar en producción)

Si tienes archivos en `media/` (SQLite o Docker local), súbelos al bucket antes de poner `USE_S3=True`:

```bash
aws s3 sync media/ s3://TU_BUCKET/media/ --exclude "*.tmp"
```

Y luego ejecuta estáticos hacia S3 desde Django:

```bash
docker compose --env-file .env.production exec web python manage.py collectstatic --noinput
```

Verifica que una URL de imagen histórica responda `200` desde S3.

## 5) Comandos de arranque

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput
docker compose exec web python manage.py createsuperuser
```

## 6) Checklist rapido

- [ ] Sitio responde en home
- [ ] Contacto guarda registro
- [ ] Login panel/admin funciona en rutas privadas
- [ ] Subida de imagen funciona y aparece en S3
- [ ] Logs sin errores criticos
