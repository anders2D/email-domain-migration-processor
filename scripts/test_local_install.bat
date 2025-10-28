@echo off
REM Script para probar instalacion local antes de publicar en PyPI

echo ========================================
echo   Prueba de Instalacion Local
echo ========================================
echo.

REM Limpiar builds anteriores
echo [1/5] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Construir paquete
echo [2/5] Construyendo paquete...
python -m build
if errorlevel 1 (
    echo ERROR: Fallo al construir el paquete
    exit /b 1
)

REM Crear entorno virtual temporal
echo [3/5] Creando entorno virtual temporal...
if exist test_venv rmdir /s /q test_venv
python -m venv test_venv
call test_venv\Scripts\activate.bat

REM Instalar paquete localmente
echo [4/5] Instalando paquete localmente...
pip install dist\*.whl
if errorlevel 1 (
    echo ERROR: Fallo al instalar el paquete
    deactivate
    exit /b 1
)

REM Probar comando
echo [5/5] Probando comando...
echo.
echo Ejecutando: email-processor --help
echo.
email-processor --help
echo.
echo Ejecutando: email-processor --input-type list --input "test@old.com" --new-domain new.com --output-type inline
echo.
email-processor --input-type list --input "test@old.com" --new-domain new.com --output-type inline

REM Limpiar
echo.
echo Limpiando entorno de prueba...
deactivate
rmdir /s /q test_venv

echo.
echo ========================================
echo   Prueba completada exitosamente!
echo ========================================
echo.
echo Si todo funciono correctamente, puedes publicar en PyPI con:
echo   cd scripts
echo   publish_pypi.bat
echo.
pause
