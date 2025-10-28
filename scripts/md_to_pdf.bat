@echo off
REM Markdown to PDF Converter - Windows Batch Script
REM Usa Pandoc + LaTeX + Eisvogel template

echo ================================================================
echo           MARKDOWN TO PDF CONVERTER
echo           Pandoc + LaTeX + Eisvogel
echo ================================================================
echo.

REM Verificar Pandoc
where pandoc >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Pandoc no esta instalado o no esta en PATH
    echo.
    echo Instalacion:
    echo   choco install pandoc
    echo   choco install miktex
    echo.
    echo Eisvogel template:
    echo   https://github.com/Wandmalfarbe/pandoc-latex-template
    exit /b 1
)

echo [OK] Pandoc detectado
echo.

REM Ejecutar script Python
python "%~dp0md_to_pdf.py"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [OK] Conversion completada exitosamente
) else (
    echo.
    echo [ERROR] Hubo errores durante la conversion
)

pause
