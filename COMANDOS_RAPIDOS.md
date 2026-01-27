# 🚀 COMANDOS RÁPIDOS - SOLUCIÓN COHETE DJANGO

## ⚡ OPCIÓN 1: Script Automático (RECOMENDADO)

### PowerShell:
```powershell
cd "C:\TOTAL LIVING"
.\SOLUCION_FINAL_COHETE.ps1
```

### CMD/Batch:
```cmd
cd "C:\TOTAL LIVING"
SOLUCION_FINAL_COHETE.bat
```

---

## ⚡ OPCIÓN 2: Comandos Manuales

### Paso 1: Cambiar al directorio
```powershell
cd "C:\TOTAL LIVING"
```

### Paso 2: Limpiar caché
```powershell
Get-ChildItem -Path "." -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

### Paso 3: Verificar configuración
```powershell
python manage.py check
```

### Paso 4: Verificar URLs
```powershell
python -c "import sys; sys.path.insert(0, '.'); import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'total_living.settings.development'); import django; django.setup(); from total_living.urls import urlpatterns; print('urlpatterns count:', len(urlpatterns)); print('First 3 patterns:', [str(p.pattern) for p in urlpatterns[:3]])"
```

### Paso 5: Iniciar servidor
```powershell
python manage.py runserver 8090
```

---

## 🌐 ACCEDER AL SITIO

Una vez que el servidor esté corriendo:
1. Abre tu navegador
2. Ve a: **http://127.0.0.1:8090/**
3. Deberías ver tu sitio web (NO el cohete)

---

## ✅ VERIFICACIÓN

Si ves:
- ✅ Tu sitio web con navbar → **TODO ESTÁ BIEN**
- ❌ Cohete de Django → El servidor está corriendo desde otro directorio
- ❌ Error 404 → Hay un problema con las URLs

---

## 🔧 SI AÚN VES EL COHETE

1. **Mata TODOS los procesos de Python:**
   ```powershell
   Get-Process python | Stop-Process -Force
   ```

2. **Espera 5 segundos**

3. **Ejecuta el script de nuevo:**
   ```powershell
   .\SOLUCION_FINAL_COHETE.ps1
   ```

---

## 📝 NOTA IMPORTANTE

**SIEMPRE ejecuta desde `C:\TOTAL LIVING`**

NUNCA desde:
- ❌ `C:\Users\rodri`
- ❌ Cualquier otro lugar
