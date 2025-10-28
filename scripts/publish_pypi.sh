#!/bin/bash
# Script para publicar en PyPI - Linux/Mac

echo "========================================"
echo "  Publicacion en PyPI - Email Processor"
echo "========================================"
echo ""

# Verificar instalacion de herramientas
echo "[1/6] Verificando herramientas..."
if ! pip show twine &> /dev/null; then
    echo "Instalando herramientas necesarias..."
    pip install --upgrade pip setuptools wheel twine build
fi

# Limpiar builds anteriores
echo "[2/6] Limpiando builds anteriores..."
rm -rf build dist *.egg-info

# Construir paquete
echo "[3/6] Construyendo paquete..."
python -m build
if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al construir el paquete"
    exit 1
fi

# Verificar paquete
echo "[4/6] Verificando paquete..."
twine check dist/*
if [ $? -ne 0 ]; then
    echo "ERROR: Verificacion del paquete fallo"
    exit 1
fi

# Preguntar si subir a TestPyPI o PyPI
echo "[5/6] Seleccionar destino:"
echo "  1. TestPyPI (pruebas)"
echo "  2. PyPI (produccion)"
read -p "Ingrese opcion (1 o 2): " choice

if [ "$choice" == "1" ]; then
    echo "Subiendo a TestPyPI..."
    twine upload --repository testpypi dist/*
elif [ "$choice" == "2" ]; then
    echo "Subiendo a PyPI..."
    twine upload dist/*
else
    echo "Opcion invalida"
    exit 1
fi

echo "[6/6] Publicacion completada!"
echo ""
echo "Verificar en:"
if [ "$choice" == "1" ]; then
    echo "https://test.pypi.org/project/email-processor-cli/"
else
    echo "https://pypi.org/project/email-processor-cli/"
fi
echo ""
