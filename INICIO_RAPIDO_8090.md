# 🚀 INICIO RÁPIDO - PUERTO 8090

## ⚡ COMANDO RÁPIDO

```powershell
cd "C:\TOTAL LIVING"
python manage.py runserver 8090
```

Luego abre: **http://127.0.0.1:8090/**

---

## 📋 PASOS COMPLETOS

### 1. Cambiar al directorio
```powershell
cd "C:\TOTAL LIVING"
```

### 2. Limpiar caché (opcional)
```powershell
Get-ChildItem -Path "." -Include __pycache__ -Recurse -Directory | Remove-Item -Recurse -Force
```

### 3. Verificar configuración
```powershell
python manage.py check
```

### 4. Iniciar servidor
```powershell
python manage.py runserver 8090
```

---

## 🌐 ACCEDER AL SITIO

Una vez que el servidor esté corriendo:
- **URL:** http://127.0.0.1:8090/
- **Admin:** http://127.0.0.1:8090/admin/

---

## ✅ VERIFICACIÓN

Si ves:
- ✅ Tu sitio web con navbar → **TODO ESTÁ BIEN**
- ❌ Cohete de Django → El servidor está corriendo desde otro directorio
- ❌ Error 404 → Hay un problema con las URLs

---

## 🔧 SCRIPTS DISPONIBLES

### PowerShell:
```powershell
.\runserver.ps1
.\iniciar_servidor.ps1
.\SOLUCION_FINAL_COHETE.ps1
```

### Batch:
```cmd
runserver.bat
iniciar_servidor.bat
SOLUCION_FINAL_COHETE.bat
```

---

## 📝 NOTA IMPORTANTE

**Este proyecto usa el puerto 8090**

**SIEMPRE ejecuta desde `C:\TOTAL LIVING`**
