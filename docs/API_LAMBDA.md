# Documentación API Lambda

## 🌐 URL Base

```
https://{api-id}.execute-api.{region}.amazonaws.com
```

Obtén tu URL de API después del despliegue:
```bash
cd terraform
terraform output api_url
```

## 🔐 Autenticación

Todas las peticiones requieren autenticación con API Key.

**Header:**
```
x-api-key: prod-email-processor-2024-secure-key
```

**Obtener API Key:**
```bash
terraform output api_key
```

**Respuesta No Autorizada (401):**
```json
{
  "error": "Unauthorized: Invalid or missing API key"
}
```

## 📡 Endpoints

### POST /extract

Extrae y valida correos de diferentes fuentes de entrada.

**Petición (Entrada de Lista):**
```json
{
  "input_type": "list",
  "input": ["juan.perez@example.com", "maria.garcia@old.com"]
}
```

**Petición (Entrada de Texto):**
```json
{
  "input_type": "text",
  "input": "juan.perez@example.com\nmaria.garcia@old.com"
}
```

**Petición (Entrada de Archivo - Base64):**
```json
{
  "input_type": "file",
  "file_content": "anVhbi5wZXJlekBleGFtcGxlLmNvbQptYXJpYS5nYXJjaWFAb2xkLmNvbQ=="
}
```

**Parámetros:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| `input_type` | string | No | Tipo de entrada: `list`, `text`, `file` (predeterminado: `list`) |
| `input` | array/string | Condicional | Array de correos o texto (requerido si no es `file`) |
| `file_content` | string | Condicional | Archivo codificado en Base64 (requerido si `input_type=file`) |

**Respuesta Exitosa (200):**
```json
{
  "emails": ["juan.perez@example.com", "maria.garcia@old.com"],
  "count": 2
}
```

---

### POST /transform

Transforma correos a un nuevo dominio.

**Petición:**
```json
{
  "emails": ["juan.perez@example.com", "maria.garcia@old.com"],
  "new_domain": "new.com"
}
```

**Parámetros:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| `emails` | array | Sí | Lista de direcciones de correo a transformar |
| `new_domain` | string | Sí | Dominio destino (sin @) |

**Respuesta Exitosa (200):**
```json
{
  "transformed": [
    {
      "nombre": "Juan",
      "apellido": "Perez",
      "correo_original": "juan.perez@example.com",
      "correo_nuevo": "juan.perez@new.com",
      "valid": true
    },
    {
      "nombre": "Maria",
      "apellido": "Garcia",
      "correo_original": "maria.garcia@old.com",
      "correo_nuevo": "maria.garcia@new.com",
      "valid": true
    }
  ],
  "valid": 2,
  "total": 2
}
```

---

### POST /generate

Genera salida en el formato especificado.

**Petición:**
```json
{
  "transformed": [
    {
      "nombre": "Juan",
      "apellido": "Perez",
      "correo_original": "juan.perez@example.com",
      "correo_nuevo": "juan.perez@new.com",
      "valid": true
    }
  ],
  "output_type": "csv"
}
```

**Parámetros:**
| Campo | Tipo | Requerido | Descripción |
|-------|------|----------|-------------|
| `transformed` | array | Sí | Array de objetos de correo transformados |
| `output_type` | string | No | Formato de salida: `inline`, `csv`, `json`, `silent` (predeterminado: `inline`) |

**Respuesta Exitosa (200) - Inline/JSON:**
```json
{
  "data": [{...}],
  "count": 2
}
```

**Respuesta Exitosa (200) - CSV:**
```json
{
  "output": "Nombre,Apellido,Correo Original,Correo Nuevo\nJuan,Perez,juan.perez@example.com,juan.perez@new.com",
  "format": "csv",
  "count": 2
}
```

**Respuesta Exitosa (200) - Silent:**
```json
{
  "count": 2,
  "status": "processed"
}
```

**Respuesta de Error (400):**
```json
{
  "error": "Missing required field: emails"
}
```

**Respuesta de Error (500):**
```json
{
  "error": "Internal server error: {details}"
}
```

## 🔄 Flujo del Pipeline

La API soporta flujos de trabajo **modulares** (3 pasos) y **directos**:

**Pipeline Modular:**
```
1. POST /extract  → Obtener array de correos
2. POST /transform → Transformar correos
3. POST /generate → Formatear salida
```

**Flujo Directo (obsoleto):**
Usa `/transform` con `input_type` para procesamiento de un solo paso.

## 📋 Reglas de Validación

Los correos deben pasar todas las reglas de validación (BR-001 a BR-005):

| Regla | Descripción | Ejemplo de Fallo |
|-------|-------------|--------------|
| BR-001 | Exactamente un @ | `user@@example.com` |
| BR-002 | Exactamente un punto en prefijo | `user@example.com` |
| BR-003 | Nombre 2-50 caracteres | `a.perez@example.com` |
| BR-004 | Apellido 2-50 caracteres | `juan.p@example.com` |
| BR-005 | Solo letras (a-z, acentos) | `juan123.perez@example.com` |

**Los correos inválidos se omiten y se registran en CloudWatch.**

## 🔄 Reglas de Transformación

Los correos válidos se transforman (TR-001 a TR-005):

| Regla | Transformación | Ejemplo |
|-------|----------------|---------|
| TR-001 | Capitalizar nombre | `juan` → `Juan` |
| TR-002 | Capitalizar apellido | `perez` → `Perez` |
| TR-003 | Minúsculas en correo | `Juan.Perez@NEW.COM` → `juan.perez@new.com` |
| TR-004 | Preservar dominio original | Almacenado en `correo_original` |
| TR-005 | Aplicar nuevo dominio | `juan.perez@new.com` |

## 📝 Ejemplos

### cURL - Pipeline Modular (3 Pasos)

```bash
API_URL="https://your-api.execute-api.us-east-1.amazonaws.com"
API_KEY="prod-email-processor-2024-secure-key"

# Step 1: Extract
EMAILS=$(curl -s -X POST $API_URL/extract \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"input_type":"list","input":["juan.perez@example.com","maria.garcia@old.com"]}' \
  | jq -r '.emails')

# Step 2: Transform
TRANSFORMED=$(curl -s -X POST $API_URL/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"emails\":$EMAILS,\"new_domain\":\"new.com\"}" \
  | jq -r '.transformed')

# Step 3: Generate
curl -X POST $API_URL/generate \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"transformed\":$TRANSFORMED,\"output_type\":\"csv\"}"
```

### cURL - Extraer desde Archivo (Base64)

```bash
# Encode file to base64
FILE_CONTENT=$(base64 -w 0 examples/file_examples/sample_emails.txt)

curl -X POST https://your-api.execute-api.us-east-1.amazonaws.com/extract \
  -H "Content-Type: application/json" \
  -H "x-api-key: prod-email-processor-2024-secure-key" \
  -d "{
    \"input_type\": \"file\",
    \"file_content\": \"$FILE_CONTENT\"
  }"
```

### Python - Pipeline Modular

```python
import requests

base_url = "https://your-api.execute-api.us-east-1.amazonaws.com"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "prod-email-processor-2024-secure-key"
}

# Step 1: Extract
extract_response = requests.post(
    f"{base_url}/extract",
    json={"input_type": "list", "input": ["juan.perez@example.com"]},
    headers=headers
)
emails = extract_response.json()['emails']

# Step 2: Transform
transform_response = requests.post(
    f"{base_url}/transform",
    json={"emails": emails, "new_domain": "new.com"},
    headers=headers
)
transformed = transform_response.json()['transformed']

# Step 3: Generate
generate_response = requests.post(
    f"{base_url}/generate",
    json={"transformed": transformed, "output_type": "csv"},
    headers=headers
)
print(generate_response.json()['output'])
```

### Python - Extraer desde Archivo

```python
import requests
import base64

url = "https://your-api.execute-api.us-east-1.amazonaws.com/extract"
headers = {
    "Content-Type": "application/json",
    "x-api-key": "prod-email-processor-2024-secure-key"
}

# Read and encode file
with open('examples/file_examples/sample_emails.txt', 'rb') as f:
    file_content = base64.b64encode(f.read()).decode('utf-8')

payload = {
    "input_type": "file",
    "file_content": file_content
}

response = requests.post(url, json=payload, headers=headers)
print(response.json()['emails'])
```

### JavaScript (Node.js) - Pipeline Modular

```javascript
const axios = require('axios');

const baseUrl = 'https://your-api.execute-api.us-east-1.amazonaws.com';
const headers = {
  'Content-Type': 'application/json',
  'x-api-key': 'prod-email-processor-2024-secure-key'
};

async function processEmails() {
  // Step 1: Extract
  const extractRes = await axios.post(`${baseUrl}/extract`, 
    { input_type: 'list', input: ['juan.perez@example.com'] },
    { headers }
  );
  
  // Step 2: Transform
  const transformRes = await axios.post(`${baseUrl}/transform`,
    { emails: extractRes.data.emails, new_domain: 'new.com' },
    { headers }
  );
  
  // Step 3: Generate
  const generateRes = await axios.post(`${baseUrl}/generate`,
    { transformed: transformRes.data.transformed, output_type: 'csv' },
    { headers }
  );
  
  console.log(generateRes.data.output);
}

processEmails();
```

### PowerShell - Pipeline Modular

```powershell
$baseUrl = "https://your-api.execute-api.us-east-1.amazonaws.com"
$headers = @{
    "Content-Type" = "application/json"
    "x-api-key" = "prod-email-processor-2024-secure-key"
}

# Step 1: Extract
$extractBody = @{
    input_type = "list"
    input = @("juan.perez@example.com")
} | ConvertTo-Json

$extractRes = Invoke-RestMethod -Uri "$baseUrl/extract" `
    -Method Post -Headers $headers -Body $extractBody

# Step 2: Transform
$transformBody = @{
    emails = $extractRes.emails
    new_domain = "new.com"
} | ConvertTo-Json

$transformRes = Invoke-RestMethod -Uri "$baseUrl/transform" `
    -Method Post -Headers $headers -Body $transformBody

# Step 3: Generate
$generateBody = @{
    transformed = $transformRes.transformed
    output_type = "csv"
} | ConvertTo-Json -Depth 10

$generateRes = Invoke-RestMethod -Uri "$baseUrl/generate" `
    -Method Post -Headers $headers -Body $generateBody

Write-Output $generateRes.output
```

## 📊 Códigos de Respuesta

| Código | Descripción |
|--------|-------------|
| 200 | Éxito - Correos procesados |
| 400 | Petición Incorrecta - Entrada inválida |
| 401 | No Autorizado - API key inválida/faltante |
| 500 | Error Interno del Servidor |

## 📈 Logs de CloudWatch

**Grupo de Logs:** `/aws/lambda/email-processor`

**Retención:** 7 días

**Eventos Registrados:**
- Validación de API key (éxito/fallo)
- Payload de petición
- Fallos de validación (BR-001 a BR-005)
- Resultados de transformación
- Errores y excepciones

**Ver Logs:**
```bash
aws logs tail /aws/lambda/email-processor --follow
```

## ⚡ Rendimiento

| Métrica | Valor |
|---------|-------|
| Arranque en frío | ~2-3 segundos |
| Ejecución en caliente | ~100-300ms |
| Timeout | 30 segundos |
| Memoria | 256 MB |
| Payload máximo | 6 MB |

## 🔒 Seguridad

- ✅ Autenticación con API Key requerida
- ✅ Solo HTTPS (TLS 1.2+)
- ✅ CORS deshabilitado por defecto
- ✅ Logging de CloudWatch habilitado
- ✅ Rol IAM con permisos mínimos

## 🚀 Despliegue

Ver [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) para instrucciones completas de despliegue.

**Despliegue Rápido:**
```bash
cd terraform
build.bat  # Windows
# or
./build.sh  # Linux/Mac

terraform init
terraform apply
```

**Obtener Credenciales:**
```bash
terraform output api_url
terraform output api_key
```

## 🧪 Pruebas

Probar la API desplegada:

```bash
# Get API details
cd terraform
API_URL=$(terraform output -raw api_url)
API_KEY=$(terraform output -raw api_key)

# Test request
curl -X POST $API_URL/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"emails":["test@example.com"],"new_domain":"new.com"}'
```

## 📞 Soporte

Para problemas o preguntas:
1. Revisar logs de CloudWatch para errores
2. Verificar que la API key sea correcta
3. Validar formato del payload de petición
4. Revisar reglas de validación (BR-001 a BR-005)
