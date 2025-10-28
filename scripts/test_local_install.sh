#!/bin/bash
# Script para probar instalacion local antes de publicar en PyPI

echo "========================================"
echo "  Prueba de Instalacion Local"
echo "========================================"
echo ""

# Limpiar builds anteriores
echo "[1/5] Limpiando builds anteriores..."
rm -rf build dist *.egg-info

# Construir paquete
echo "[2/5] Construyendo paquete..."
python -m build
if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al construir el paquete"
    exit 1
fi

# Crear entorno virtual temporal
echo "[3/5] Creando entorno virtual temporal..."
rm -rf test_venv
python -m venv test_venv
source test_venv/bin/activate

# Instalar paquete localmente
echo "[4/5] Instalando paquete localmente..."
pip install dist/*.whl
if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al instalar el paquete"
    deactivate
    exit 1
fi

# Probar comando
echo "[5/5] Probando comando..."
echo ""
echo "Ejecutando: email-processor --help"
echo ""
email-processor --help
echo ""
echo "Ejecutando: email-processor --input-type list --input \"test@old.com\" --new-domain new.com --output-type inline"
echo ""
email-processor --input-type list --input "test@old.com" --new-domain new.com --output-type inline

# Limpiar
echo ""
echo "Limpiando entorno de prueba..."
deactivate
rm -rf test_venv

echo ""
echo "========================================"
echo "  Prueba completada exitosamente!"
echo "========================================"
echo ""
echo "Si todo funciono correctamente, puedes publicar en PyPI con:"
echo "  cd scripts"
echo "  ./publish_pypi.sh"
echo ""
