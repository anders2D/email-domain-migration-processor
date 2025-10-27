#!/bin/bash
# Script de limpieza de archivos temporales y basura
# Uso: sh clean.sh

echo "========================================"
echo "Limpieza de archivos temporales"
echo "========================================"
echo ""

cd "$(dirname "$0")/.."

echo "[1/3] Limpiando outputs temporales..."
rm -f correos_procesados.csv error_log.txt summary.txt test_error_log.txt test_output.csv *.log

echo "[2/3] Limpiando artefactos de Terraform..."
rm -f terraform/lambda_function.zip

echo "[3/3] Limpiando cache de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null

echo ""
echo "========================================"
echo "Limpieza completada"
echo "========================================"
