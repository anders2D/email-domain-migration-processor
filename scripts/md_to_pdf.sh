#!/bin/bash
# Markdown to PDF Converter - Unix/Linux/macOS Script
# Usa Pandoc + LaTeX + Eisvogel template

echo "================================================================"
echo "           MARKDOWN TO PDF CONVERTER"
echo "           Pandoc + LaTeX + Eisvogel"
echo "================================================================"
echo ""

# Verificar Pandoc
if ! command -v pandoc &> /dev/null; then
    echo "[ERROR] Pandoc no está instalado o no está en PATH"
    echo ""
    echo "Instalación:"
    echo "  macOS:   brew install pandoc"
    echo "  Linux:   sudo apt install pandoc"
    echo ""
    echo "Eisvogel template:"
    echo "  https://github.com/Wandmalfarbe/pandoc-latex-template"
    exit 1
fi

echo "[OK] Pandoc detectado"
echo ""

# Obtener directorio del script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ejecutar script Python
python3 "$SCRIPT_DIR/md_to_pdf.py"

if [ $? -eq 0 ]; then
    echo ""
    echo "[OK] Conversión completada exitosamente"
else
    echo ""
    echo "[ERROR] Hubo errores durante la conversión"
    exit 1
fi
