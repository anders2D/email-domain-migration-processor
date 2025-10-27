# Email Processor - Hexagonal Architecture

## 🎯 Architecture Principles

- ✅ **Stateless**: No state between requests
- ✅ **Modular**: Extract → Transform → Generate pattern
- ✅ **Hexagonal**: Core isolated from infrastructure
- ✅ **Multi-interface**: CLI, API (Local + Lambda), Library
- ✅ **Flexible I/O**: Multiple input/output types

## 💼 Business Logic

### Core Workflow

The system processes email addresses by extracting user information and migrating them to a new domain:

1. **Extract**: Read emails from various sources (file, list, text)
2. **Validate**: Apply business rules BR-001 to BR-005
3. **Transform**: Apply transformation rules TR-001 to TR-005
4. **Output**: Generate results in CSV, JSON, or inline format

### Validation Rules (BR)

| ID | Rule | Condition | Action if Fails |
|----|------|-----------|------------------|
| BR-001 | Exactly one @ | `email.count('@') == 1` | Log and skip |
| BR-002 | Exactly one dot in prefix | `prefix.count('.') == 1` | Log and skip |
| BR-003 | First name 2-50 characters | `2 ≤ len(nombre) ≤ 50` | Log and skip |
| BR-004 | Last name 2-50 characters | `2 ≤ len(apellido) ≤ 50` | Log and skip |
| BR-005 | Only letters (a-z, A-Z, accented) | `nombre.isalpha()` | Log and skip |

**Note:** All validations execute sequentially. If any fails, the email is logged and skipped.

### Transformation Rules (TR)

| ID | Rule | Example Input | Example Output |
|----|------|---------------|----------------|
| TR-001 | Capitalize first name | juan | Juan |
| TR-002 | Capitalize last name | perez | Perez |
| TR-003 | Lowercase email | Juan.Perez@NEW.COM | juan.perez@new.com |
| TR-004 | Preserve original domain | juan.perez@example.com | @example.com |
| TR-005 | Apply new domain | Juan + Perez + @new.com | juan.perez@new.com |

**Note:** Transformations only apply to emails that passed all validations.

### Domain Entity (Email)

**Properties:**
- `nombre`: First name (capitalized)
- `apellido`: Last name (capitalized)
- `correo_original`: Original email address
- `correo_nuevo`: New email with target domain

**Behavior:**
- Automatically capitalizes names
- Automatically lowercases email addresses
- Generates new email: `nombre.apellido@new_domain`

### Process Metrics

| Metric | Value |
|--------|-------|
| Processing speed | ~0.1 sec/email |
| Success rate | 90-95% |
| Validation errors | 5-10% |
| Capacity | 10,000+ emails/day (automated) |

## 🏗️ Structure

```
src/features/email_processing/
├── domain/              # Core Business Logic
│   ├── email.py        # Entity
│   └── ports.py        # Interfaces
├── adapters/
│   ├── input/          # Primary Adapters
│   │   ├── cli_adapter.py
│   │   ├── api_adapter.py
│   │   └── library_adapter.py
│   └── output/         # Secondary Adapters
│       ├── file_adapter.py
│       ├── csv_adapter.py
│       └── json_adapter.py
└── shared/             # Validation & Logging
```

## 🚀 Quick Start

### CLI
```bash
python main_cli.py --input-type list --input "user@old.com" --new-domain new.com --output-type inline
```

### API (Local)
```bash
# Start server
python main_api.py

# Test
python test_api.py
```

### API (AWS Lambda)
```bash
cd terraform
build.bat  # or ./build.sh
terraform apply

# Get API Key
terraform output api_key
```

**Authentication:** All Lambda API requests require `x-api-key` header.

```bash
# Example with API Key
curl -X POST https://your-api.execute-api.us-east-1.amazonaws.com/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: prod-email-processor-2024-secure-key" \
  -d '{"emails":["user@old.com"],"new_domain":"new.com"}'
```

### Library
```python
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary

emails = EmailProcessingLibrary.extract(['user@old.com'], 'list')
transformed = EmailProcessingLibrary.transform(emails, 'new.com')
result = EmailProcessingLibrary.generate(transformed, 'inline')
```

## 📋 Input Types
- **file**: Read from file path
- **list**: Array of emails
- **text**: Newline-separated text

## 📋 Output Types
- **csv**: Save to CSV file (default)
- **json**: Save to JSON file
- **inline**: Return/print directly
- **silent**: Process without output (logs only)

## 🔐 Security

### API Key Authentication

The Lambda API uses hardcoded API Key authentication:

- **Header:** `x-api-key`
- **Default Key:** `prod-email-processor-2024-secure-key`
- **Environment Variable:** `API_KEY` in Lambda
- **Response on failure:** `401 Unauthorized`

**Get API Key after deployment:**
```bash
cd terraform
terraform output api_key
```

**Test authentication:**
```bash
# Without API Key (fails)
curl -X POST $API_URL/transform -d '{}'
# Response: {"error": "Unauthorized: Invalid or missing API key"}

# With API Key (succeeds)
curl -X POST $API_URL/transform -H "x-api-key: YOUR_KEY" -d '{}'
```

## 📚 Examples

See [examples/](examples/) folder for comprehensive usage examples:
- API examples (local + Lambda with API Key)
- Library examples
- CLI examples (Windows + Linux/Mac)

## 🧪 Testing

```bash
python test_api.py
```

## 📖 Documentation

### 🚀 Getting Started

- **[Quick Start Guide](docs/QUICK_START.md)** - Start using in 5 minutes with practical examples
- **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)** - Complete deployment and usage documentation
- **[Cheatsheet](docs/CHEATSHEET.md)** - Quick reference for commands and configurations
- **[n8n Integration](docs/N8N_INTEGRATION.md)** - Workflow automation with n8n platform

### 📋 Process Documentation

**[docs/pdd/PDD.md](docs/pdd/PDD.md)** - Complete business process documentation:

- 📄 **AS-IS Process:** Manual process description with actors, steps, and metrics
- 📊 **Business Rules:** Validation (BR-001 to BR-005) and transformation rules (TR-001 to TR-005)
- 🤖 **Automation Analysis:** 100% automation feasibility with technology mapping
- 🚀 **TO-BE Vision:** Automated process design and benefits comparison
- ⚠️ **Risk Assessment:** Operational, security, and compliance risks with mitigation strategies
- 📅 **Transition Roadmap:** 6-month implementation plan

### 📊 Process Diagrams

**[docs/pdd/diagrams/](docs/pdd/diagrams/)** - Visual process documentation:

| Diagram | Description | Section |
|---------|-------------|----------|
| `macroproceso.mmd` | Organizational context (upstream/downstream) | 1.1 |
| `swimlanes.mmd` | Actor interaction sequence | 1.1 |
| `alcance.mmd` | Scope visualization (in/out) | 1.2 |
| `entradas-salidas.mmd` | Input/output data flow | 1.3-1.4 |
| `flujo-detallado.mmd` | Detailed AS-IS manual flow | 1.8 |
| `heatmap-automatizacion.mmd` | Automation feasibility heatmap | 4.2 |
| `proceso-tobe.mmd` | TO-BE automated process | 5.1 |
| `roadmap-transicion.mmd` | 6-month transition Gantt | 5.3 |

**Generate Diagrams:**
```bash
cd docs/pdd/diagrams
sh convert.sh
```

**Requirements:**
```bash
npm install -g @mermaid-js/mermaid-cli
```

## 🚢 Deployment

See [terraform/README.md](terraform/README.md) for AWS deployment instructions.

### CloudWatch Logs

Logs are automatically saved to CloudWatch:

- **Lambda logs:** `/aws/lambda/email-processor`
- **API Gateway logs:** `/aws/apigateway/email-processor`
- **Retention:** 7 days
- **Includes:** Request/response, errors, validation failures, API key validation