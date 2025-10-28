# 📦 Guía de Publicación en PyPI

## 🎯 Requisitos Previos

1. **Cuenta en PyPI**
   - Crear cuenta en [PyPI](https://pypi.org/account/register/)
   - Crear cuenta en [TestPyPI](https://test.pypi.org/account/register/) (opcional, para pruebas)

2. **Generar API Token**
   - Ir a [PyPI Account Settings](https://pypi.org/manage/account/)
   - Crear API token con scope "Entire account" o específico del proyecto
   - Guardar el token (comienza con `pypi-`)

3. **Instalar herramientas**
   ```bash
   pip install --upgrade pip setuptools wheel twine build
   ```

## 🚀 Pasos para Publicar

### 1. Actualizar Versión

Editar `setup.py` y `pyproject.toml`:
```python
version="1.0.0"  # Incrementar según semantic versioning
```

### 2. Limpiar Builds Anteriores

**Windows:**
```cmd
rmdir /s /q build dist *.egg-info
```

**Linux/Mac:**
```bash
rm -rf build dist *.egg-info
```

### 3. Construir el Paquete

```bash
python -m build
```

Esto genera:
- `dist/email-processor-cli-1.0.0.tar.gz` (source distribution)
- `dist/email_processor_cli-1.0.0-py3-none-any.whl` (wheel)

### 4. Verificar el Paquete

```bash
twine check dist/*
```

### 5. Probar en TestPyPI (Opcional)

```bash
twine upload --repository testpypi dist/*
```

Instalar desde TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ email-processor-cli
```

### 6. Publicar en PyPI

```bash
twine upload dist/*
```

Ingresar credenciales:
- **Username:** `__token__`
- **Password:** Tu API token (incluyendo el prefijo `pypi-`)

### 7. Verificar Publicación

Visitar: https://pypi.org/project/email-processor-cli/

## 📥 Instalación del Paquete

Una vez publicado, los usuarios pueden instalar con:

```bash
pip install email-processor-cli
```

## 🔧 Uso del CLI

Después de instalar, el comando estará disponible globalmente:

```bash
email-processor --input-type list --input "user@old.com" --new-domain new.com --output-type inline
```

## 🔄 Actualizar Versión

Para publicar una nueva versión:

1. Actualizar versión en `setup.py` y `pyproject.toml`
2. Limpiar builds anteriores
3. Construir nuevo paquete
4. Subir a PyPI

```bash
# Ejemplo: actualizar de 1.0.0 a 1.0.1
python -m build
twine upload dist/*
```

## 🔐 Configuración de Credenciales

### Opción 1: Variables de Entorno

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=pypi-your-token-here
twine upload dist/*
```

### Opción 2: Archivo .pypirc

Crear `~/.pypirc` (Linux/Mac) o `%USERPROFILE%\.pypirc` (Windows):

```ini
[distutils]
index-servers =
    pypi

[pypi]
username = __token__
password = pypi-your-token-here
```

**⚠️ IMPORTANTE:** Nunca commitear `.pypirc` con tokens reales al repositorio.

## 📋 Checklist Pre-Publicación

- [ ] Versión actualizada en `setup.py` y `pyproject.toml`
- [ ] README.md actualizado con ejemplos de uso
- [ ] LICENSE incluido
- [ ] Tests ejecutados exitosamente
- [ ] Builds anteriores limpiados
- [ ] Paquete construido con `python -m build`
- [ ] Paquete verificado con `twine check dist/*`
- [ ] (Opcional) Probado en TestPyPI
- [ ] API token de PyPI configurado
- [ ] Publicado con `twine upload dist/*`

## 🐛 Solución de Problemas

### Error: "File already exists"

El paquete con esa versión ya existe en PyPI. Incrementar versión y reconstruir.

### Error: "Invalid or non-existent authentication"

Verificar que el token sea correcto y comience con `pypi-`.

### Error: "Package name already taken"

Cambiar el nombre en `setup.py` y `pyproject.toml` a uno único.

### Paquete no se instala correctamente

Verificar que `MANIFEST.in` incluya todos los archivos necesarios.

## 📚 Referencias

- [PyPI Official Guide](https://packaging.python.org/tutorials/packaging-projects/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [Semantic Versioning](https://semver.org/)
