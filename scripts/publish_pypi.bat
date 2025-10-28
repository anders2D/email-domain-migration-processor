@echo off
REM Script para publicar en PyPI - Windows

echo ========================================
echo   Publicacion en PyPI - Email Processor
echo ========================================
echo.

REM Verificar instalacion de herramientas
echo [1/6] Verificando herramientas...
pip show twine >nul 2>&1
if errorlevel 1 (
    echo Instalando herramientas necesarias...
    pip install --upgrade pip setuptools wheel twine build
)

REM Limpiar builds anteriores
echo [2/6] Limpiando builds anteriores...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Construir paquete
echo [3/6] Construyendo paquete...
python -m build
if errorlevel 1 (
    echo ERROR: Fallo al construir el paquete
    exit /b 1
)

REM Verificar paquete
echo [4/6] Verificando paquete...
twine check dist/*
if errorlevel 1 (
    echo ERROR: Verificacion del paquete fallo
    exit /b 1
)

REM Preguntar si subir a TestPyPI o PyPI
echo [5/6] Seleccionar destino:
echo   1. TestPyPI (pruebas)
echo   2. PyPI (produccion)
set /p choice="Ingrese opcion (1 o 2): "

if "%choice%"=="1" (
    echo Subiendo a TestPyPI...
    twine upload --repository testpypi dist/*
) else if "%choice%"=="2" (
    echo Subiendo a PyPI...
    twine upload dist/*
) else (
    echo Opcion invalida
    exit /b 1
)

echo [6/6] Publicacion completada!
echo.
echo Verificar en:
if "%choice%"=="1" (
    echo https://test.pypi.org/project/email-processor-cli/
) else (
    echo https://pypi.org/project/email-processor-cli/
)
echo.
pause
