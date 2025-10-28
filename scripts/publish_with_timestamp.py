#!/usr/bin/env python3
"""
Script para publicar en PyPI con versión basada en timestamp
Formato: YYYY.MM.DD.HHMMSS
Ejemplo: 2025.01.27.143052
"""
import os
import sys
import subprocess
from datetime import datetime
import re

def update_version_in_file(filepath, new_version):
    """Actualiza la versión en un archivo"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar version="X.X.X" o version = "X.X.X"
    content = re.sub(
        r'version\s*=\s*["\'][\d.]+["\']',
        f'version="{new_version}"',
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"OK Actualizado {os.path.basename(filepath)}")

def run_command(cmd, cwd=None):
    """Ejecuta un comando y retorna el resultado"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: {result.stderr}")
        sys.exit(1)
    return result.stdout

def main():
    # Obtener directorio raíz del proyecto
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    
    # Generar versión con timestamp
    now = datetime.now()
    version = now.strftime("%Y.%m.%d.%H%M%S")
    
    print("=" * 50)
    print("  Publicacion en PyPI con Timestamp")
    print("=" * 50)
    print(f"\nNueva version: {version}\n")
    
    # Actualizar versión en archivos
    print("[1/6] Actualizando versión...")
    setup_py = os.path.join(project_dir, "setup.py")
    
    update_version_in_file(setup_py, version)
    
    # Limpiar builds anteriores
    print("\n[2/6] Limpiando builds anteriores...")
    for dir_name in ["build", "dist"]:
        dir_path = os.path.join(project_dir, dir_name)
        if os.path.exists(dir_path):
            if sys.platform == "win32":
                run_command(f'rmdir /s /q "{dir_path}"', cwd=project_dir)
            else:
                run_command(f'rm -rf "{dir_path}"', cwd=project_dir)
    
    # Limpiar .egg-info
    for item in os.listdir(project_dir):
        if item.endswith(".egg-info"):
            item_path = os.path.join(project_dir, item)
            if sys.platform == "win32":
                run_command(f'rmdir /s /q "{item_path}"', cwd=project_dir)
            else:
                run_command(f'rm -rf "{item_path}"', cwd=project_dir)
    
    print("OK Limpieza completada")
    
    # Construir paquete
    print("\n[3/6] Construyendo paquete...")
    run_command("python -m build", cwd=project_dir)
    print("OK Paquete construido")
    
    # Verificar paquete
    print("\n[4/6] Verificando paquete...")
    print("OK Omitiendo verificacion (publicando directamente)")
    
    # Preguntar destino
    print("\n[5/6] Seleccionar destino:")
    print("  1. TestPyPI (pruebas)")
    print("  2. PyPI (producción)")
    choice = input("Ingrese opción (1 o 2): ").strip()
    
    # Publicar
    print("\n[6/6] Publicando...")
    if choice == "1":
        print("Subiendo a TestPyPI...")
        run_command("twine upload --repository testpypi dist/*", cwd=project_dir)
        print(f"\nOK Publicado en TestPyPI!")
        print(f"   https://test.pypi.org/project/email-processor-cli/{version}/")
    elif choice == "2":
        print("Subiendo a PyPI...")
        run_command("twine upload dist/*", cwd=project_dir)
        print(f"\nOK Publicado en PyPI!")
        print(f"   https://pypi.org/project/email-processor-cli/{version}/")
    else:
        print("ERROR Opcion invalida")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("  Publicacion completada!")
    print("=" * 50)
    print(f"\nVersion publicada: {version}")
    print("\nInstalar con:")
    print("  pip install email-processor-cli")
    print("\nUsar con:")
    print("  email-processor --help")

if __name__ == "__main__":
    main()
