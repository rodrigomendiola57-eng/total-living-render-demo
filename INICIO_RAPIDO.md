# 🚀 INICIO RÁPIDO - SOLUCIÓN DEFINITIVA

## ⚠️ PROBLEMA

Ves el cohete de Django o error 404 porque el servidor no está cargando las URLs correctamente.

## ✅ SOLUCIÓN EN 3 PASOS

### PASO 1: Limpiar Caché

```powershell
cd "C:\TOTAL LIVING"
Get-ChildItem -Path "." -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

### PASO 2: Verificar que todo está bien

```powershell
python manage.py check
# Debe mostrar: System check identified no issues
```

### PASO 3: Iniciar el servidor

```powershell
python manage.py runserver 8080
```

**IMPORTANTE:** Asegúrate de que el servidor muestre:
```
Starting development server at http://127.0.0.1:8080/
```

**NO deberías ver errores** al iniciar.

## 🌐 ACCEDER AL SITIO

1. **Abre tu navegador**
2. **Ve a:** http://127.0.0.1:8080/
3. **Deberías ver:** Tu sitio web con navbar, hero section, etc.

## 🔍 VERIFICACIÓN

Si accedes a http://127.0.0.1:8080/ y ves:
- ✅ Tu sitio web → **TODO ESTÁ BIEN**
- ❌ Cohete de Django → El servidor está corriendo desde otro proyecto
- ❌ Error 404 → Hay un problema con las URLs

## 📝 NOTA CRÍTICA

**SIEMPRE inicia el servidor desde `C:\TOTAL LIVING`**

NUNCA desde:
- ❌ `C:\Users\rodri`
- ❌ Cualquier otro lugar

---

**Ejecuta los 3 pasos en orden y el problema se resolverá.**
