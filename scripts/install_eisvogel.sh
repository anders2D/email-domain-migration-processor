#!/bin/bash
# Instalar Eisvogel template para Pandoc (Unix/Linux/macOS)

echo "================================================================"
echo "           EISVOGEL TEMPLATE INSTALLER"
echo "================================================================"
echo ""

# Determinar directorio de templates según el sistema
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    TEMPLATE_DIR="$HOME/.pandoc/templates"
else
    # Linux
    TEMPLATE_DIR="$HOME/.local/share/pandoc/templates"
fi

# Crear directorio si no existe
if [ ! -d "$TEMPLATE_DIR" ]; then
    echo "Creando directorio de templates: $TEMPLATE_DIR"
    mkdir -p "$TEMPLATE_DIR"
fi

echo "Descargando Eisvogel template..."
echo ""

# Descargar template
curl -o "$TEMPLATE_DIR/eisvogel.tex" \
    https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.tex

if [ $? -eq 0 ]; then
    echo ""
    echo "[OK] Eisvogel template instalado en: $TEMPLATE_DIR/eisvogel.tex"
    echo ""
    echo "Ahora puedes ejecutar: ./md_to_pdf.sh"
else
    echo ""
    echo "[ERROR] No se pudo descargar el template"
    echo ""
    echo "Descarga manual:"
    echo "  https://github.com/Wandmalfarbe/pandoc-latex-template"
    echo "  Guarda eisvogel.tex en: $TEMPLATE_DIR"
    exit 1
fi
