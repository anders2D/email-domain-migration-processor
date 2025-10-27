# 📋 Cheatsheet - Referencia Rápida

## 🎯 Comandos Esenciales

### CLI

```bash
# Sintaxis básica
python main_cli.py --input-type <TYPE> --input <DATA> --new-domain <DOMAIN> --output-type <TYPE> [--output <FILE>]

# Archivo → CSV
python main_cli.py --input-type file --input emails.txt --new-domain company.com --output-type csv --output result.csv

# Lista → Inline
python main_cli.py --input-type list --input "a@x.com,b@y.com" --new-domain new.com --output-type inline

# Texto → JSON
python main_cli.py --input-type text --input "a@x.com\nb@y.com" --new-domain new.com --output-type json --output result.json

# Modo silencioso
python main_cli.py --input-type file --input emails.txt --new-domain company.com --output-type silent
```

### API Local

```bash
# Iniciar servidor
python main_api.py

# Extract
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"input_type":"list","input":["user@old.com"]}'

# Transform
curl -X POST http://localhost:5000/transform \
  -H "Content-Type: application/json" \
  -d '{"emails":["user@old.com"],"new_domain":"new.com"}'

# Generate
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"transformed":[{"transformed":"user@new.com","valid":true}],"output_type":"inline"}'
```

### Lambda (AWS)

```bash
# Construir
cd terraform && ./build.sh

# Desplegar
terraform init && terraform apply

# Obtener API Key
terraform output api_key

# Usar
curl -X POST $API_URL/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"emails":["user@old.com"],"new_domain":"new.com"}'

# Destruir
terraform destroy
```

### Librería Python

```python
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary

# Extract
emails = EmailProcessingLibrary.extract(["user@old.com"], "list")

# Transform
transformed = EmailProcessingLibrary.transform(emails, "new.com")

# Generate
result = EmailProcessingLibrary.generate(transformed, "inline")

# Validate
is_valid = EmailProcessingLibrary.validate("user@domain.com")
```

---

## 📊 Parámetros

### Input Types

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| `file` | Archivo de texto | `emails.txt` |
| `list` | Lista de correos | `["a@x.com", "b@y.com"]` |
| `text` | Texto con saltos de línea | `"a@x.com\nb@y.com"` |

### Output Types

| Tipo | Descripción | Requiere archivo | Retorna |
|------|-------------|------------------|---------|
| `csv` | Archivo CSV | Sí | Contador |
| `json` | Archivo JSON | Sí | Contador |
| `inline` | Salida directa | No | Lista/Array |
| `silent` | Sin salida | No | Contador |

---

## 🔍 Reglas de Validación

### Business Rules (BR)

| ID | Regla | Ejemplo Válido | Ejemplo Inválido |
|----|-------|----------------|------------------|
| BR-001 | Exactamente un @ | `user@domain.com` | `user@@domain.com` |
| BR-002 | Exactamente un . antes de @ | `user.name@domain.com` | `username@domain.com` |
| BR-003 | Nombre 2-50 caracteres | `juan.perez@x.com` | `a.perez@x.com` |
| BR-004 | Apellido 2-50 caracteres | `juan.perez@x.com` | `juan.p@x.com` |
| BR-005 | Solo letras (a-z, A-Z, acentos) | `josé.garcía@x.com` | `juan123.perez@x.com` |

### Transformation Rules (TR)

| ID | Regla | Input | Output |
|----|-------|-------|--------|
| TR-001 | Capitalizar nombre | `juan` | `Juan` |
| TR-002 | Capitalizar apellido | `perez` | `Perez` |
| TR-003 | Minúsculas en email | `Juan.Perez@NEW.COM` | `juan.perez@new.com` |
| TR-004 | Preservar dominio original | `juan.perez@example.com` | `@example.com` |
| TR-005 | Aplicar nuevo dominio | `Juan + Perez + @new.com` | `juan.perez@new.com` |

---

## 🌐 Endpoints API

### Local (http://localhost:5000)

| Método | Endpoint | Body | Response |
|--------|----------|------|----------|
| POST | `/extract` | `{"input_type":"list","input":["email"]}` | `{"emails":[],"count":N}` |
| POST | `/transform` | `{"emails":[],"new_domain":"x.com"}` | `{"transformed":[],"valid":N,"total":N}` |
| POST | `/generate` | `{"transformed":[],"output_type":"inline"}` | `{"emails":[],"count":N}` |

### Lambda (https://xxx.execute-api.region.amazonaws.com)

Mismos endpoints + header `x-api-key: <API_KEY>`

---

## 📁 Archivos Generados

| Archivo | Descripción | Formato |
|---------|-------------|---------|
| `result.csv` | Correos transformados | CSV |
| `result.json` | Correos transformados | JSON |
| `error_log.txt` | Errores de validación | Texto |
| `summary.txt` | Resumen de ejecución | Texto |
| `email_processor_YYYYMMDD.log` | Log detallado | Texto |

---

## 🔧 Terraform

```bash
# Inicializar
terraform init

# Ver plan
terraform plan

# Aplicar cambios
terraform apply

# Ver outputs
terraform output

# Obtener valor específico
terraform output -raw api_key

# Destruir todo
terraform destroy

# Ver estado
terraform state list

# Formatear código
terraform fmt

# Validar sintaxis
terraform validate
```

---

## 📊 AWS CLI

```bash
# Ver logs Lambda
aws logs tail /aws/lambda/email-processor --follow

# Ver logs API Gateway
aws logs tail /aws/apigateway/email-processor --follow

# Invocar Lambda directamente
aws lambda invoke \
  --function-name email-processor \
  --payload '{"body":"{\"emails\":[\"user@old.com\"],\"new_domain\":\"new.com\"}"}' \
  response.json

# Ver métricas
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=email-processor \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-12-31T23:59:59Z \
  --period 3600 \
  --statistics Sum

# Listar funciones
aws lambda list-functions

# Ver configuración
aws lambda get-function --function-name email-processor
```

---

## 🐍 Python Snippets

### Validación Manual

```python
from src.shared.validation_adapter import RegexEmailValidator

validator = RegexEmailValidator()

# Validar formato
is_valid = validator.is_valid("juan.perez@example.com")  # True

# Validar y parsear
nombre, apellido = validator.validate_and_parse("juan.perez@example.com")
# nombre = "juan", apellido = "perez"

# Validar dominio
is_valid = validator.validate_domain("company.com")  # True
```

### Crear Email Entity

```python
from src.features.email_processing.domain.email import Email

email = Email.create(
    nombre="Juan",
    apellido="Perez",
    correo_original="juan.perez@old.com",
    nuevo_dominio="new.com"
)

print(email.nombre)           # Juan
print(email.apellido)         # Perez
print(email.correo_original)  # juan.perez@old.com
print(email.correo_nuevo)     # juan.perez@new.com
print(str(email))             # juan.perez@new.com
```

### Usar Service Directamente

```python
from src.features.email_processing.domain.email_service import EmailProcessingService
from src.shared.validation_adapter import RegexEmailValidator
from src.shared.logging_adapter import PythonLogger

validator = RegexEmailValidator()
logger = PythonLogger("custom")
service = EmailProcessingService(validator, logger)

result = service.transform_emails(
    ["juan.perez@old.com", "ana.garcia@old.com"],
    "company.com"
)

print(f"Processed: {result['processed']}/{result['total']}")
print(f"Success rate: {result['success_rate']:.1f}%")

for email in result['emails']:
    print(f"{email.correo_original} → {email.correo_nuevo}")

for error in result['error_details']:
    print(f"Error: {error['email']} - {error['error']}")
```

---

## 🔐 Seguridad

### API Key (Lambda)

```bash
# Default
x-api-key: prod-email-processor-2024-secure-key

# Cambiar en main.tf
environment {
  variables = {
    API_KEY = "tu-nueva-api-key-segura"
  }
}

# Obtener después de deploy
terraform output -raw api_key
```

### Variables de Entorno

```bash
# Linux/Mac
export NEW_DOMAIN="company.com"
export API_KEY="secret-key"

# Windows (CMD)
set NEW_DOMAIN=company.com
set API_KEY=secret-key

# Windows (PowerShell)
$env:NEW_DOMAIN="company.com"
$env:API_KEY="secret-key"
```

---

## 📈 Performance

### Métricas Esperadas

| Métrica | Valor |
|---------|-------|
| Velocidad | ~0.1 seg/email |
| Tasa de éxito | 90-95% |
| Errores de validación | 5-10% |
| Capacidad diaria | 10,000+ emails |

### Optimización

```python
# Procesar en lotes
batch_size = 100
for i in range(0, len(emails), batch_size):
    batch = emails[i:i+batch_size]
    result = service.transform_emails(batch, new_domain)
```

---

## 🧪 Testing

### Casos de Prueba

```bash
# Válidos
juan.perez@example.com
maría.garcía@test.com
josé.lópez@domain.com

# Inválidos
invalid@email@com          # BR-001: Múltiples @
noname@domain.com          # BR-002: Sin punto antes de @
a.b@domain.com             # BR-003: Nombre muy corto
juan.p@domain.com          # BR-004: Apellido muy corto
juan123.perez@domain.com   # BR-005: Números no permitidos
```

### Ejecutar Tests

```bash
# Tests de ejemplo
python examples/tests/run_tests.py

# Test completo
python examples/test_complete_flow.py

# Test API
python test_api.py
```

---

## 🐛 Debug

### Logs Detallados

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Ver Stack Trace

```bash
python main_cli.py ... 2>&1 | tee debug.log
```

### Verificar Estructura

```bash
# Windows
dir /s /b src

# Linux/Mac
find src -type f
```

---

## 🔄 Actualización

### Actualizar Código Local

```bash
git pull origin main
pip install -r requirements.txt
```

### Actualizar Lambda

```bash
cd terraform
./build.sh
terraform apply
```

### Rollback

```bash
git checkout <commit-hash>
cd terraform
./build.sh
terraform apply
```

---

## 📞 Soporte

### Verificar Versión

```bash
python --version
pip list | grep flask
terraform --version
aws --version
```

### Limpiar Cache

```bash
# Python
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

# Terraform
rm -rf .terraform terraform.tfstate*
```

### Reiniciar Todo

```bash
# Detener procesos
pkill -f main_api.py

# Limpiar archivos
rm -f *.csv *.json *.txt *.log

# Reconstruir
cd terraform
terraform destroy
./build.sh
terraform apply
```

---

## 📚 Enlaces Rápidos

- [Guía Completa](DEPLOYMENT_GUIDE.md)
- [Inicio Rápido](QUICK_START.md)
- [PDD](pdd/PDD.md)
- [SDD](sdd/SDD.md)
- [README](../README.md)
- [Ejemplos](../examples/)

---

**Tip:** Guarda este archivo como favorito para consulta rápida.
