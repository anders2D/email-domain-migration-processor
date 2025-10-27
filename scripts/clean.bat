@echo off
REM Script de limpieza de archivos temporales y basura
REM Uso: clean.bat

echo ========================================
echo Limpieza de archivos temporales
echo ========================================
echo.

cd /d "%~dp0.."

echo [1/3] Limpiando outputs temporales...
if exist correos_procesados.csv del /q correos_procesados.csv
if exist error_log.txt del /q error_log.txt
if exist summary.txt del /q summary.txt
if exist test_error_log.txt del /q test_error_log.txt
if exist test_output.csv del /q test_output.csv
if exist *.log del /q *.log

echo [2/3] Limpiando artefactos de Terraform...
if exist terraform\lambda_function.zip del /q terraform\lambda_function.zip

echo [3/3] Limpiando cache de Python...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
if exist *.pyc del /s /q *.pyc

echo.
echo ========================================
echo Limpieza completada
echo ========================================
