# 🚨 INSTRUCCIONES URGENTES - SOLUCIONAR ERROR

## ⚠️ PROBLEMA IDENTIFICADO

El servidor está corriendo desde `C:\Users\rodri` en lugar de `C:\TOTAL LIVING`, por eso busca la base de datos incorrecta.

## ✅ SOLUCIÓN INMEDIATA (3 PASOS)

### PASO 1: DETENER EL SERVIDOR ACTUAL

1. Ve a la terminal donde está corriendo el servidor
2. Presiona `Ctrl + C` para detenerlo
3. **ESPERA** hasta que veas el prompt de nuevo

### PASO 2: ABRIR NUEVA TERMINAL POWERSHELL

1. Cierra la terminal actual completamente
2. Abre una **NUEVA** terminal PowerShell
3. **NO** uses la terminal anterior

### PASO 3: EJECUTAR ESTOS COMANDOS (COPIA Y PEGA)

```powershell
# Ir al directorio correcto
cd "C:\TOTAL LIVING"

# Verificar que estás en el lugar correcto
Get-Location
# Debe mostrar: C:\TOTAL LIVING

# Verificar que existe manage.py
Test-Path "manage.py"
# Debe mostrar: True

# Iniciar el servidor
python manage.py runserver 8080
```

## ✅ ALTERNATIVA: USAR EL SCRIPT

Si prefieres, usa el script que creamos:

```powershell
cd "C:\TOTAL LIVING"
.\iniciar_servidor.ps1
```

## 🔍 VERIFICACIÓN

Después de iniciar el servidor, deberías ver algo como:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 06, 2026 - 00:XX:XX
Django version 5.2.7, using settings 'total_living.settings.development'
Starting development server at http://127.0.0.1:8080/
Quit the server with CTRL-BREAK.
```

## 🌐 ACCEDER AL ADMIN

1. Abre tu navegador
2. Ve a: **http://127.0.0.1:8080/admin/**
3. Usa estas credenciales:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

## ❌ SI SIGUE SALIENDO EL ERROR

Si después de seguir estos pasos sigue saliendo el error:

1. **Detén el servidor** (Ctrl+C)
2. **Ejecuta este comando:**
   ```powershell
   cd "C:\TOTAL LIVING"
   python fix_database.py
   ```
3. **Luego inicia el servidor de nuevo:**
   ```powershell
   python manage.py runserver 8080
   ```

## 🔑 PUNTOS CLAVE

- ✅ **SIEMPRE** inicia el servidor desde `C:\TOTAL LIVING`
- ✅ **NUNCA** desde `C:\Users\rodri` o cualquier otro lugar
- ✅ **SIEMPRE** verifica con `Get-Location` antes de iniciar
- ✅ Usa el script `iniciar_servidor.ps1` para evitar errores

---

**¡Sigue estos pasos exactamente y el problema se resolverá!**
