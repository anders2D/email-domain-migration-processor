#!/usr/bin/env python3
"""
Markdown to PDF Converter
Usa Pandoc + LaTeX + Eisvogel template para generar PDFs estilizados
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Configuración de documentos a convertir
DOCUMENTS = {
    'README.md': {
        'title': 'Procesador de Correos - Arquitectura Hexagonal',
        'subtitle': 'Sistema de migración de dominios de correo electrónico',
        'author': 'Anderson Taguada',
        'output': 'README.pdf'
    },
    'docs/PDD.md': {
        'title': 'Process Definition Document (PDD)',
        'subtitle': 'Documentación del proceso de negocio',
        'author': 'Anderson Taguada',
        'output': 'docs/PDD.pdf'
    },
    'docs/DEPLOYMENT_GUIDE.md': {
        'title': 'Guía de Despliegue',
        'subtitle': 'Despliegue completo en AWS Lambda',
        'author': 'Anderson Taguada',
        'output': 'docs/DEPLOYMENT_GUIDE.pdf'
    },
    'docs/QUICK_START.md': {
        'title': 'Guía de Inicio Rápido',
        'subtitle': 'Comienza en 5 minutos',
        'author': 'Anderson Taguada',
        'output': 'docs/QUICK_START.pdf'
    }
}

def check_pandoc():
    """Verifica que Pandoc esté instalado"""
    try:
        result = subprocess.run(['pandoc', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def convert_to_pdf(input_file: str, config: dict, base_path: Path):
    """Convierte un archivo Markdown a PDF usando Pandoc + Eisvogel"""
    input_path = base_path / input_file
    output_path = base_path / config['output']
    
    if not input_path.exists():
        print(f"❌ Archivo no encontrado: {input_path}")
        return False
    
    # Crear directorio de salida si no existe
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Comando Pandoc con Eisvogel
    cmd = [
        'pandoc',
        str(input_path),
        '-o', str(output_path),
        '--from=markdown',
        '--template=eisvogel',
        '--listings',
        '--pdf-engine=xelatex',
        f'--metadata=title:{config["title"]}',
        f'--metadata=subtitle:{config["subtitle"]}',
        f'--metadata=author:{config["author"]}',
        f'--metadata=date:{datetime.now().strftime("%Y-%m-%d")}',
        '--metadata=titlepage:true',
        '--metadata=toc:true',
        '--metadata=toc-own-page:true',
        '--metadata=listings-no-page-break:true',
        '--metadata=code-block-font-size:\\small'
    ]
    
    print(f"📄 Convirtiendo: {input_file} → {config['output']}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_path)
        if result.returncode == 0:
            print(f"✅ Generado: {output_path}")
            return True
        else:
            print(f"❌ Error al convertir {input_file}:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Excepción: {e}")
        return False

def main():
    base_path = Path(__file__).parent.parent
    
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           MARKDOWN TO PDF CONVERTER                          ║")
    print("║           Pandoc + LaTeX + Eisvogel                          ║")
    print("╚══════════════════════════════════════════════════════════════╝\n")
    
    # Verificar Pandoc
    if not check_pandoc():
        print("❌ Pandoc no está instalado o no está en PATH")
        print("\nInstalación:")
        print("  Windows: choco install pandoc")
        print("  macOS:   brew install pandoc")
        print("  Linux:   sudo apt install pandoc")
        print("\nEisvogel template:")
        print("  https://github.com/Wandmalfarbe/pandoc-latex-template")
        sys.exit(1)
    
    print("✅ Pandoc detectado\n")
    
    # Convertir documentos
    success = 0
    failed = 0
    
    for input_file, config in DOCUMENTS.items():
        if convert_to_pdf(input_file, config, base_path):
            success += 1
        else:
            failed += 1
        print()
    
    # Resumen
    print("═" * 64)
    print(f"✅ Exitosos: {success}")
    print(f"❌ Fallidos:  {failed}")
    print(f"📊 Total:     {success + failed}")
    print("═" * 64)
    
    return 0 if failed == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
