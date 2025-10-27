@echo off
REM Script para convertir diagramas Mermaid a SVG en Windows
REM Requiere: npm install -g @mermaid-js/mermaid-cli

echo Convirtiendo diagramas Mermaid a SVG...

REM Verificar si mmdc esta instalado
where mmdc >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: mermaid-cli no esta instalado
    echo Instalar con: npm install -g @mermaid-js/mermaid-cli
    exit /b 1
)

REM Convertir cada archivo .mmd a .svg
for %%f in (*.mmd) do (
    echo   %%f -^> %%~nf.svg
    mmdc -i "%%f" -o "%%~nf.svg" -t neutral -b transparent
)

echo Conversion completada
