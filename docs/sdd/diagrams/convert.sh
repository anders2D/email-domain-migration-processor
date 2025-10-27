#!/bin/bash

# Script para convertir diagramas Mermaid a SVG
# Requiere: npm install -g @mermaid-js/mermaid-cli

echo "🎨 Convirtiendo diagramas Mermaid a SVG..."

# Verificar si mmdc está instalado
if ! command -v mmdc &> /dev/null; then
    echo "❌ Error: mermaid-cli no está instalado"
    echo "Instalar con: npm install -g @mermaid-js/mermaid-cli"
    exit 1
fi

# Convertir cada archivo .mmd a .svg
for file in *.mmd; do
    if [ -f "$file" ]; then
        output="${file%.mmd}.svg"
        echo "  📄 $file → $output"
        mmdc -i "$file" -o "$output" -t neutral -b transparent
    fi
done

echo "✅ Conversión completada"
