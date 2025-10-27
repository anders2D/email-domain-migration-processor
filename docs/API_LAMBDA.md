# Lambda API Documentation

## 🌐 Base URL

```
https://{api-id}.execute-api.{region}.amazonaws.com
```

Get your API URL after deployment:
```bash
cd terraform
terraform output api_url
```

## 🔐 Authentication

All requests require API Key authentication.

**Header:**
```
x-api-key: prod-email-processor-2024-secure-key
```

**Get API Key:**
```bash
terraform output api_key
```

**Unauthorized Response (401):**
```json
{
  "error": "Unauthorized: Invalid or missing API key"
}
```

## 📡 Endpoints

### POST /extract

Extract and validate emails from different input sources.

**Request (List Input):**
```json
{
  "input_type": "list",
  "input": ["juan.perez@example.com", "maria.garcia@old.com"]
}
```

**Request (Text Input):**
```json
{
  "input_type": "text",
  "input": "juan.perez@example.com\nmaria.garcia@old.com"
}
```

**Request (File Input - Base64):**
```json
{
  "input_type": "file",
  "file_content": "anVhbi5wZXJlekBleGFtcGxlLmNvbQptYXJpYS5nYXJjaWFAb2xkLmNvbQ=="
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `input_type` | string | No | Input type: `list`, `text`, `file` (default: `list`) |
| `input` | array/string | Conditional | Emails array or text (required if not `file`) |
| `file_content` | string | Conditional | Base64 encoded file (required if `input_type=file`) |

**Success Response (200):**
```json
{
  "emails": ["juan.perez@example.com", "maria.garcia@old.com"],
  "count": 2
}
```

---

### POST /transform

Transform emails to a new domain.

**Request:**
```json
{
  "emails": ["juan.perez@example.com", "maria.garcia@old.com"],
  "new_domain": "new.com"
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `emails` | array | Yes | List of email addresses to transform |
| `new_domain` | string | Yes | Target domain (without @) |

**Success Response (200):**
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

Generate output in specified format.

**Request:**
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

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `transformed` | array | Yes | Array of transformed email objects |
| `output_type` | string | No | Output format: `inline`, `csv`, `json`, `silent` (default: `inline`) |

**Success Response (200) - Inline/JSON:**
```json
{
  "data": [{...}],
  "count": 2
}
```

**Success Response (200) - CSV:**
```json
{
  "output": "Nombre,Apellido,Correo Original,Correo Nuevo\nJuan,Perez,juan.perez@example.com,juan.perez@new.com",
  "format": "csv",
  "count": 2
}
```

**Success Response (200) - Silent:**
```json
{
  "count": 2,
  "status": "processed"
}
```

**Error Response (400):**
```json
{
  "error": "Missing required field: emails"
}
```

**Error Response (500):**
```json
{
  "error": "Internal server error: {details}"
}
```

## 🔄 Pipeline Flow

The API supports both **modular** (3 steps) and **direct** workflows:

**Modular Pipeline:**
```
1. POST /extract  → Get emails array
2. POST /transform → Transform emails
3. POST /generate → Format output
```

**Direct Workflow (deprecated):**
Use `/transform` with `input_type` for single-step processing.

## 📋 Validation Rules

Emails must pass all validation rules (BR-001 to BR-005):

| Rule | Description | Example Fail |
|------|-------------|--------------|
| BR-001 | Exactly one @ | `user@@example.com` |
| BR-002 | Exactly one dot in prefix | `user@example.com` |
| BR-003 | First name 2-50 chars | `a.perez@example.com` |
| BR-004 | Last name 2-50 chars | `juan.p@example.com` |
| BR-005 | Only letters (a-z, accents) | `juan123.perez@example.com` |

**Invalid emails are skipped and logged in CloudWatch.**

## 🔄 Transformation Rules

Valid emails are transformed (TR-001 to TR-005):

| Rule | Transformation | Example |
|------|----------------|---------|
| TR-001 | Capitalize first name | `juan` → `Juan` |
| TR-002 | Capitalize last name | `perez` → `Perez` |
| TR-003 | Lowercase email | `Juan.Perez@NEW.COM` → `juan.perez@new.com` |
| TR-004 | Preserve original domain | Stored in `correo_original` |
| TR-005 | Apply new domain | `juan.perez@new.com` |

## 📝 Examples

### cURL - Modular Pipeline (3 Steps)

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

### cURL - Extract from File (Base64)

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

### Python - Modular Pipeline

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

### Python - Extract from File

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

### JavaScript (Node.js) - Modular Pipeline

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

### PowerShell - Modular Pipeline

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

## 📊 Response Codes

| Code | Description |
|------|-------------|
| 200 | Success - Emails processed |
| 400 | Bad Request - Invalid input |
| 401 | Unauthorized - Invalid/missing API key |
| 500 | Internal Server Error |

## 📈 CloudWatch Logs

**Log Group:** `/aws/lambda/email-processor`

**Retention:** 7 days

**Logged Events:**
- API key validation (success/failure)
- Request payload
- Validation failures (BR-001 to BR-005)
- Transformation results
- Errors and exceptions

**View Logs:**
```bash
aws logs tail /aws/lambda/email-processor --follow
```

## ⚡ Performance

| Metric | Value |
|--------|-------|
| Cold start | ~2-3 seconds |
| Warm execution | ~100-300ms |
| Timeout | 30 seconds |
| Memory | 256 MB |
| Max payload | 6 MB |

## 🔒 Security

- ✅ API Key authentication required
- ✅ HTTPS only (TLS 1.2+)
- ✅ CORS disabled by default
- ✅ CloudWatch logging enabled
- ✅ IAM role with minimal permissions

## 🚀 Deployment

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for complete deployment instructions.

**Quick Deploy:**
```bash
cd terraform
build.bat  # Windows
# or
./build.sh  # Linux/Mac

terraform init
terraform apply
```

**Get Credentials:**
```bash
terraform output api_url
terraform output api_key
```

## 🧪 Testing

Test the deployed API:

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

## 📞 Support

For issues or questions:
1. Check CloudWatch logs for errors
2. Verify API key is correct
3. Validate request payload format
4. Review validation rules (BR-001 to BR-005)
