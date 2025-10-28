# 🚀 Guía de Despliegue y Uso

## 📋 Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Instalación Local](#instalación-local)
3. [Uso CLI](#uso-cli)
4. [Uso API Local](#uso-api-local)
5. [Uso como Librería](#uso-como-librería)
6. [Despliegue AWS Lambda](#despliegue-aws-lambda)
7. [Monitoreo y Logs](#monitoreo-y-logs)
8. [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos Previos

### Software Requerido

```bash
# Python 3.11+
python --version

# pip (gestor de paquetes)
pip --version

# Git (opcional)
git --version
```

### Dependencias Python

```bash
# Instalar dependencias
pip install -r requirements.txt

# O manualmente
pip install flask requests
```

### Para Despliegue AWS

```bash
# Terraform 1.0+
terraform --version

# AWS CLI configurado
aws --version
aws configure
```

---

## 🔧 Instalación Local

### 1. Clonar o Descargar el Proyecto

```bash
# Opción 1: Clonar con Git
git clone <repository-url>
cd hiperautomatization

# Opción 2: Descargar ZIP y extraer
cd hiperautomatization
```

### 2. Verificar Estructura

```
hiperautomatization/
├── src/                    # Código fuente
├── examples/               # Ejemplos de uso
├── terraform/              # Infraestructura AWS
├── main_cli.py            # Interfaz CLI
├── main_api.py            # Interfaz API
└── README.md
```

### 3. Probar Instalación

```bash
# Verificar CLI
python main_cli.py --help

# Verificar API
python main_api.py
# Ctrl+C para detener
```

---

## 💻 Uso CLI

### Sintaxis General

```bash
# Opción 1: Usando PyPI (recomendado)
email-processor \
  --input-type <file|list|text> \
  --input <datos> \
  --new-domain <dominio> \
  --output-type <csv|json|inline|silent> \
  --output <archivo>

# Opción 2: Usando código fuente
python main_cli.py \
  --input-type <file|list|text> \
  --input <datos> \
  --new-domain <dominio> \
  --output-type <csv|json|inline|silent> \
  --output <archivo>
```

### Parámetros

| Parámetro | Valores | Descripción | Requerido |
|-----------|---------|-------------|-----------|
| `--input-type` | file, list, text | Tipo de entrada | Sí |
| `--input` | string | Datos de entrada | Sí |
| `--new-domain` | string | Dominio destino | Sí |
| `--output-type` | csv, json, inline, silent | Formato de salida | No (default: csv) |
| `--output` | string | Archivo de salida | Sí (para csv/json) |

### Ejemplos Prácticos

#### 1. Procesar Archivo a CSV

```bash
# PyPI
email-processor \
  --input-type file \
  --input examples/file_examples/sample_emails.txt \
  --new-domain company.com \
  --output-type csv \
  --output result.csv

# Código fuente
python main_cli.py \
  --input-type file \
  --input examples/file_examples/sample_emails.txt \
  --new-domain company.com \
  --output-type csv \
  --output result.csv
```

**Salida:**
```
[OK] Processed 10/10 emails
[OK] Error log: error_log.txt
[OK] Summary: summary.txt
```

#### 2. Procesar Lista a JSON

```bash
# PyPI
email-processor \
  --input-type list \
  --input "juan.perez@old.com,ana.garcia@old.com" \
  --new-domain newcompany.com \
  --output-type json \
  --output result.json

# Código fuente
python main_cli.py \
  --input-type list \
  --input "juan.perez@old.com,ana.garcia@old.com" \
  --new-domain newcompany.com \
  --output-type json \
  --output result.json
```

#### 3. Procesar Texto a Inline (sin archivo)

```bash
# PyPI
email-processor \
  --input-type text \
  --input "user@old.com
admin@old.com" \
  --new-domain company.com \
  --output-type inline

# Código fuente
python main_cli.py \
  --input-type text \
  --input "user@old.com
admin@old.com" \
  --new-domain company.com \
  --output-type inline
```

**Salida:**
```
user@company.com
admin@company.com
```

#### 4. Modo Silencioso (solo logs)

```bash
# PyPI
email-processor \
  --input-type file \
  --input emails.txt \
  --new-domain company.com \
  --output-type silent

# Código fuente
python main_cli.py \
  --input-type file \
  --input emails.txt \
  --new-domain company.com \
  --output-type silent
```

### Windows (PowerShell)

```powershell
# PyPI
email-processor `
  --input-type file `
  --input examples\file_examples\sample_emails.txt `
  --new-domain company.com `
  --output-type csv `
  --output result.csv

# Código fuente
python main_cli.py `
  --input-type file `
  --input examples\file_examples\sample_emails.txt `
  --new-domain company.com `
  --output-type csv `
  --output result.csv
```

### Archivos Generados

| Archivo | Descripción |
|---------|-------------|
| `result.csv` | Correos transformados |
| `error_log.txt` | Errores de validación |
| `summary.txt` | Resumen de ejecución |

---

## 🌐 Uso API Local

### 1. Iniciar Servidor

```bash
python main_api.py
```

**Salida:**
```
=== Email Processing API - Modular & Stateless ===
Server: http://localhost:5000

Endpoints:
  POST /extract    - Extract emails from source
  POST /transform  - Transform emails with new domain
  POST /generate   - Generate output in format

Test: python test_api.py
```

### 2. Endpoints Disponibles

#### POST /extract

Extrae correos de diferentes fuentes.

**Request:**
```bash
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "list",
    "input": ["user@old.com", "admin@old.com"]
  }'
```

**Response:**
```json
{
  "emails": ["user@old.com", "admin@old.com"],
  "count": 2
}
```

**Tipos de Input:**

```json
// Desde archivo
{
  "input_type": "file",
  "input": "path/to/emails.txt"
}

// Desde lista
{
  "input_type": "list",
  "input": ["email1@old.com", "email2@old.com"]
}

// Desde texto
{
  "input_type": "text",
  "input": "email1@old.com\nemail2@old.com"
}
```

#### POST /transform

Transforma correos con nuevo dominio.

**Request:**
```bash
curl -X POST http://localhost:5000/transform \
  -H "Content-Type: application/json" \
  -d '{
    "emails": ["juan.perez@old.com", "ana.garcia@old.com"],
    "new_domain": "company.com"
  }'
```

**Response:**
```json
{
  "transformed": [
    {
      "original": "juan.perez@old.com",
      "transformed": "juan.perez@company.com",
      "valid": true
    },
    {
      "original": "ana.garcia@old.com",
      "transformed": "ana.garcia@company.com",
      "valid": true
    }
  ],
  "valid": 2,
  "total": 2
}
```

#### POST /generate

Genera salida en formato especificado.

**Request:**
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "transformed": [
      {"transformed": "user@new.com", "valid": true}
    ],
    "output_type": "inline"
  }'
```

**Response:**
```json
{
  "emails": ["user@new.com"],
  "count": 1
}
```

**Tipos de Output:**

| Tipo | Descripción | Requiere `output_file` |
|------|-------------|------------------------|
| `inline` | Retorna array JSON | No |
| `csv` | Guarda en CSV | Sí |
| `json` | Guarda en JSON | Sí |
| `silent` | Solo contador | No |

### 3. Pipeline Completo

```bash
# 1. Extract
EMAILS=$(curl -s -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"input_type":"list","input":["user@old.com"]}' \
  | jq -r '.emails')

# 2. Transform
TRANSFORMED=$(curl -s -X POST http://localhost:5000/transform \
  -H "Content-Type: application/json" \
  -d "{\"emails\":$EMAILS,\"new_domain\":\"new.com\"}" \
  | jq -r '.transformed')

# 3. Generate
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d "{\"transformed\":$TRANSFORMED,\"output_type\":\"inline\"}"
```

### 4. Ejemplos con Python

```python
import requests

BASE_URL = "http://localhost:5000"

# Extract
response = requests.post(f"{BASE_URL}/extract", json={
    "input_type": "list",
    "input": ["user@old.com", "admin@old.com"]
})
emails = response.json()["emails"]

# Transform
response = requests.post(f"{BASE_URL}/transform", json={
    "emails": emails,
    "new_domain": "company.com"
})
transformed = response.json()["transformed"]

# Generate
response = requests.post(f"{BASE_URL}/generate", json={
    "transformed": transformed,
    "output_type": "inline"
})
result = response.json()["emails"]
print(result)
```

---

## 📚 Uso como Librería

### Importar Módulo

```python
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary
```

### Métodos Disponibles

#### 1. extract(input_data, input_type)

```python
# Desde archivo
emails = EmailProcessingLibrary.extract("emails.txt", "file")

# Desde lista
emails = EmailProcessingLibrary.extract(["user@old.com"], "list")

# Desde texto
emails = EmailProcessingLibrary.extract("user@old.com\nadmin@old.com", "text")
```

#### 2. transform(emails, new_domain)

```python
emails = ["juan.perez@old.com", "ana.garcia@old.com"]
transformed = EmailProcessingLibrary.transform(emails, "company.com")

# Resultado:
# [
#   {"original": "juan.perez@old.com", "transformed": "juan.perez@company.com", "valid": True},
#   {"original": "ana.garcia@old.com", "transformed": "ana.garcia@company.com", "valid": True}
# ]
```

#### 3. generate(transformed, output_type, output_file=None)

```python
# Inline (retorna lista)
emails = EmailProcessingLibrary.generate(transformed, "inline")

# CSV (guarda archivo)
count = EmailProcessingLibrary.generate(transformed, "csv", "output.csv")

# JSON (guarda archivo)
count = EmailProcessingLibrary.generate(transformed, "json", "output.json")

# Silent (solo contador)
count = EmailProcessingLibrary.generate(transformed, "silent")
```

#### 4. validate(email)

```python
is_valid = EmailProcessingLibrary.validate("juan.perez@example.com")
# True

is_valid = EmailProcessingLibrary.validate("invalid_email")
# False
```

### Ejemplo Completo

```python
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary

# Pipeline completo
emails = EmailProcessingLibrary.extract(["juan.perez@old.com"], "list")
transformed = EmailProcessingLibrary.transform(emails, "company.com")
result = EmailProcessingLibrary.generate(transformed, "inline")

print(result)
# ['juan.perez@company.com']
```

---

## ☁️ Despliegue AWS Lambda

### Arquitectura

```
Cliente → API Gateway → Lambda Function → CloudWatch Logs
          (x-api-key)   (Python 3.11)     (7 días)
```

### Recursos Creados

| Recurso | Nombre | Descripción |
|---------|--------|-------------|
| Lambda | `email-processor` | Función Python 3.11 |
| API Gateway | `email-processor-api` | HTTP API |
| IAM Role | `email-processor-role` | Permisos Lambda |
| CloudWatch | `/aws/lambda/email-processor` | Logs Lambda |
| CloudWatch | `/aws/apigateway/email-processor` | Logs API Gateway |

### Paso 1: Construir Paquete

#### Windows

```bash
cd terraform
build.bat
```

**Contenido de build.bat:**
```batch
@echo off
echo Building Lambda deployment package...

rmdir /s /q lambda_package 2>nul
mkdir lambda_package

xcopy /s /e /i ..\src lambda_package\src
copy lambda_handler.py lambda_package\

cd lambda_package
powershell Compress-Archive -Path * -DestinationPath ..\lambda_function.zip -Force
cd ..

rmdir /s /q lambda_package

echo Lambda package created: lambda_function.zip
```

#### Linux/Mac

```bash
cd terraform
chmod +x build.sh
./build.sh
```

**Verificar:**
```bash
ls -lh lambda_function.zip
# Debe existir y pesar ~50KB
```

### Paso 2: Configurar AWS

```bash
# Configurar credenciales
aws configure

# Verificar perfil
aws sts get-caller-identity --profile kubernates
```

**Editar variables (opcional):**

`terraform/main.tf`:
```hcl
variable "aws_profile" {
  default = "kubernates"  # Cambiar perfil
}

variable "aws_region" {
  default = "us-east-1"   # Cambiar región
}
```

### Paso 3: Desplegar con Terraform

```bash
cd terraform

# Inicializar
terraform init

# Revisar plan
terraform plan

# Aplicar cambios
terraform apply
# Escribir: yes
```

**Salida esperada:**
```
Apply complete! Resources: 12 added, 0 changed, 0 destroyed.

Outputs:

api_endpoint = "https://abc123.execute-api.us-east-1.amazonaws.com"
api_key = <sensitive>
extract_url = "https://abc123.execute-api.us-east-1.amazonaws.com/extract"
transform_url = "https://abc123.execute-api.us-east-1.amazonaws.com/transform"
generate_url = "https://abc123.execute-api.us-east-1.amazonaws.com/generate"
lambda_function_name = "email-processor"
region = "us-east-1"
```

### Paso 4: Obtener API Key

```bash
terraform output api_key
# prod-email-processor-2024-secure-key
```

### Paso 5: Probar Endpoints

#### Sin API Key (Falla)

```bash
curl -X POST https://abc123.execute-api.us-east-1.amazonaws.com/transform \
  -H "Content-Type: application/json" \
  -d '{"emails":["user@old.com"],"new_domain":"new.com"}'
```

**Response:**
```json
{
  "error": "Unauthorized: Invalid or missing API key"
}
```

#### Con API Key (Éxito)

```bash
API_KEY=$(cd terraform && terraform output -raw api_key)
API_URL=$(cd terraform && terraform output -raw api_endpoint)

curl -X POST $API_URL/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{
    "emails": ["juan.perez@old.com"],
    "new_domain": "company.com"
  }'
```

**Response:**
```json
{
  "transformed": [
    {
      "Nombre": "Juan",
      "Apellido": "Perez",
      "Correo Ejemplo": "juan.perez@old.com",
      "Correo Nuevo": "juan.perez@company.com",
      "valid": true
    }
  ],
  "valid": 1,
  "total": 1
}
```

### Paso 6: Usar en Producción

#### Bash Script

```bash
#!/bin/bash
API_KEY="prod-email-processor-2024-secure-key"
API_URL="https://abc123.execute-api.us-east-1.amazonaws.com"

curl -X POST $API_URL/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{
    "emails": ["user@old.com"],
    "new_domain": "company.com"
  }'
```

#### Python

```python
import requests

API_KEY = "prod-email-processor-2024-secure-key"
API_URL = "https://abc123.execute-api.us-east-1.amazonaws.com"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

response = requests.post(
    f"{API_URL}/transform",
    headers=headers,
    json={
        "emails": ["juan.perez@old.com"],
        "new_domain": "company.com"
    }
)

print(response.json())
```

#### PowerShell

```powershell
$API_KEY = "prod-email-processor-2024-secure-key"
$API_URL = "https://abc123.execute-api.us-east-1.amazonaws.com"

$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = $API_KEY
}

$body = @{
    emails = @("user@old.com")
    new_domain = "company.com"
} | ConvertTo-Json

Invoke-RestMethod -Uri "$API_URL/transform" -Method Post -Headers $headers -Body $body
```

### Paso 7: Actualizar Lambda

```bash
# Modificar código
# Reconstruir paquete
cd terraform
build.sh  # o build.bat

# Redesplegar
terraform apply
```

### Paso 8: Destruir Infraestructura

```bash
cd terraform
terraform destroy
# Escribir: yes
```

**Advertencia:** Esto eliminará todos los recursos de AWS.

---

## 📊 Monitoreo y Logs

### CloudWatch Logs

#### Ver Logs Lambda

```bash
# AWS CLI
aws logs tail /aws/lambda/email-processor --follow

# Consola AWS
https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logsV2:log-groups/log-group/$252Faws$252Flambda$252Femail-processor
```

#### Ver Logs API Gateway

```bash
aws logs tail /aws/apigateway/email-processor --follow
```

### Logs Locales

#### CLI

```bash
# Logs en consola (PyPI)
email-processor --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv

# Logs en consola (código fuente)
python main_cli.py --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv

# Archivos generados:
# - error_log.txt: Errores de validación
# - summary.txt: Resumen de ejecución
# - email_processor_YYYYMMDD.log: Log detallado
```

#### API

```bash
# Logs en consola
python main_api.py

# Ver en tiempo real:
# 2025-10-27 10:30:15 - INFO - Extracting emails from list
# 2025-10-27 10:30:15 - INFO - Extracted 2 emails
# 2025-10-27 10:30:16 - INFO - Transforming 2 emails to domain company.com
```

### Métricas

#### Lambda

```bash
# Invocaciones
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=email-processor \
  --start-time 2025-10-27T00:00:00Z \
  --end-time 2025-10-27T23:59:59Z \
  --period 3600 \
  --statistics Sum

# Errores
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=email-processor \
  --start-time 2025-10-27T00:00:00Z \
  --end-time 2025-10-27T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

#### API Gateway

```bash
# Requests
aws cloudwatch get-metric-statistics \
  --namespace AWS/ApiGateway \
  --metric-name Count \
  --dimensions Name=ApiId,Value=<api-id> \
  --start-time 2025-10-27T00:00:00Z \
  --end-time 2025-10-27T23:59:59Z \
  --period 3600 \
  --statistics Sum
```

---

## 🔧 Troubleshooting

### Problemas Comunes

#### 1. "Module not found"

**Error:**
```
ModuleNotFoundError: No module named 'src'
```

**Solución:**
```bash
# Verificar estructura
ls src/

# Ejecutar desde raíz del proyecto
cd hiperautomatization
python main_cli.py --help
```

#### 2. "Invalid input_type"

**Error:**
```
ValueError: Invalid input_type: fil
```

**Solución:**
```bash
# Valores válidos: file, list, text
python main_cli.py --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv
```

#### 3. "output_file required for csv"

**Error:**
```
ValueError: output_file required for csv
```

**Solución:**
```bash
# Agregar --output para csv/json
python main_cli.py --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv
```

#### 4. API no responde

**Error:**
```
requests.exceptions.ConnectionError
```

**Solución:**
```bash
# Iniciar servidor
python main_api.py

# En otra terminal
curl http://localhost:5000/extract
```

#### 5. Lambda "Unauthorized"

**Error:**
```json
{"error": "Unauthorized: Invalid or missing API key"}
```

**Solución:**
```bash
# Obtener API Key
cd terraform
terraform output api_key

# Usar en header
curl -H "x-api-key: <API_KEY>" ...
```

#### 6. Terraform "No such file"

**Error:**
```
Error: no such file or directory: lambda_function.zip
```

**Solución:**
```bash
# Construir paquete primero
cd terraform
./build.sh  # o build.bat

# Luego aplicar
terraform apply
```

#### 7. AWS Credentials

**Error:**
```
Error: No valid credential sources found
```

**Solución:**
```bash
# Configurar AWS CLI
aws configure

# Verificar
aws sts get-caller-identity
```

#### 8. Validación falla

**Error:**
```
BR-001: Email must contain exactly one @
```

**Causa:** Email no cumple reglas de negocio.

**Solución:** Revisar formato:
- Exactamente un `@`
- Exactamente un `.` antes del `@`
- Nombre y apellido entre 2-50 caracteres
- Solo letras (a-z, A-Z, SIN acentos)

### Logs de Debug

#### Habilitar logs detallados

```python
# En main_cli.py o main_api.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Ver stack trace completo

```bash
# CLI (PyPI)
email-processor ... 2>&1 | tee debug.log

# CLI (código fuente)
python main_cli.py ... 2>&1 | tee debug.log

# API
python main_api.py 2>&1 | tee api_debug.log
```

### Contacto Soporte

Para problemas no resueltos:

1. Revisar logs: `error_log.txt`, `summary.txt`
2. Verificar versión Python: `python --version`
3. Verificar dependencias: `pip list`
4. Consultar documentación: `README.md`, `docs/pdd/PDD.md`

---

## 📚 Referencias

- [README.md](../README.md) - Documentación principal
- [QUICK_START.md](QUICK_START.md) - Guía rápida de inicio
- [CHEATSHEET.md](CHEATSHEET.md) - Referencia rápida
- [PDD.md](pdd/PDD.md) - Definición del proceso
- [SDD.md](sdd/SDD.md) - Diseño técnico
- [examples/](../examples/) - Ejemplos de uso
- [terraform/README.md](../terraform/README.md) - Infraestructura AWS

---

## 📝 Notas de Versión

### v1.0.0 (2025-10-27)

**Características:**
- ✅ CLI, API Local, Lambda y Librería Python
- ✅ Validación completa (BR-001 a BR-005)
- ✅ Transformación automática (TR-001 a TR-005)
- ✅ Múltiples formatos de entrada/salida
- ✅ Autenticación con API Key
- ✅ Logs en CloudWatch
- ✅ Documentación completa en español

**Requisitos:**
- Python 3.11+
- Flask 3.0.0
- Requests 2.31.0
- Terraform 1.0+ (para AWS)

---

**Última actualización:** 2025-10-27  
**Versión:** 1.0.0  
**Licencia:** MIT  
**Mantenedor:** Equipo de Desarrollo
