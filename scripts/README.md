# Scripts de Utilidad

## 🧹 Limpieza

### clean.bat / clean.sh

Script de limpieza de archivos temporales y basura del proyecto.

**Windows:**
```bash
scripts\clean.bat
```

**Linux/Mac:**
```bash
sh scripts/clean.sh
```

**Archivos que elimina:**
1. Outputs temporales: correos_procesados.csv, error_log.txt, summary.txt, *.log
2. Artefactos Terraform: lambda_function.zip
3. Cache Python: __pycache__/, *.pyc

## 📦 PyPI

### test_local_install.bat / test_local_install.sh

Prueba la instalación del paquete localmente antes de publicar en PyPI.

**Windows:**
```bash
scripts\test_local_install.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/test_local_install.sh
./scripts/test_local_install.sh
```

**Qué hace:**
1. Limpia builds anteriores
2. Construye el paquete
3. Crea entorno virtual temporal
4. Instala el paquete localmente
5. Prueba el comando `email-processor`
6. Limpia el entorno de prueba

### publish_pypi.bat / publish_pypi.sh

Publica el paquete en PyPI o TestPyPI con versión manual.

**Windows:**
```bash
scripts\publish_pypi.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/publish_pypi.sh
./scripts/publish_pypi.sh
```

**Requisitos previos:**
- Cuenta en PyPI creada
- API token generado
- Archivo `~/.pypirc` configurado

**Qué hace:**
1. Verifica herramientas necesarias
2. Limpia builds anteriores
3. Construye el paquete
4. Verifica el paquete
5. Pregunta si subir a TestPyPI o PyPI
6. Sube el paquete

### publish_timestamp.bat / publish_timestamp.sh (Recomendado)

Publica el paquete con versión automática basada en timestamp.

**Windows:**
```bash
scripts\publish_timestamp.bat
```

**Linux/Mac:**
```bash
chmod +x scripts/publish_timestamp.sh
./scripts/publish_timestamp.sh
```

**Formato de versión:** `YYYY.MM.DD.HHMMSS`
- Ejemplo: `2025.01.27.143052`

**Ventajas:**
- ✅ Versión única automática
- ✅ No hay conflictos de versión
- ✅ Trazabilidad por fecha/hora
- ✅ No requiere editar archivos manualmente

**Qué hace:**
1. Genera versión con timestamp actual
2. Actualiza `setup.py` y `pyproject.toml` automáticamente
3. Limpia builds anteriores
4. Construye el paquete
5. Verifica el paquete
6. Pregunta si subir a TestPyPI o PyPI
7. Sube el paquete

**Ver documentación completa:**
- [PYPI_DEPLOYMENT.md](../docs/PYPI_DEPLOYMENT.md)
- [PYPI_QUICKSTART.md](../docs/PYPI_QUICKSTART.md)
- [PYPI_SETUP_SUMMARY.md](../PYPI_SETUP_SUMMARY.md)
