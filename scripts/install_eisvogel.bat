@echo off
REM Instalar Eisvogel template para Pandoc (Windows)

echo ================================================================
echo           EISVOGEL TEMPLATE INSTALLER
echo ================================================================
echo.

REM Crear directorio de templates si no existe
set TEMPLATE_DIR=%APPDATA%\pandoc\templates
if not exist "%TEMPLATE_DIR%" (
    echo Creando directorio de templates: %TEMPLATE_DIR%
    mkdir "%TEMPLATE_DIR%"
)

echo Descargando Eisvogel template...
echo.

REM Descargar template usando PowerShell
powershell -Command "Invoke-WebRequest -Uri 'https://raw.githubusercontent.com/Wandmalfarbe/pandoc-latex-template/master/eisvogel.tex' -OutFile '%TEMPLATE_DIR%\eisvogel.tex'"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Eisvogel template instalado en: %TEMPLATE_DIR%\eisvogel.tex
    echo.
    echo Ahora puedes ejecutar: md_to_pdf.bat
) else (
    echo.
    echo [ERROR] No se pudo descargar el template
    echo.
    echo Descarga manual:
    echo   https://github.com/Wandmalfarbe/pandoc-latex-template
    echo   Guarda eisvogel.tex en: %TEMPLATE_DIR%
)

pause
