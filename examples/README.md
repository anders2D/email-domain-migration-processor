# Examples

## 📁 Available Examples

### 🔧 CLI Examples
- **cli_example.bat** - Windows command-line usage
- **cli_example.sh** - Linux/Mac command-line usage

### 🌐 API Examples
- **api_example.py** - Local API server usage
- **lambda_example.bat** - AWS Lambda API (Windows)
- **lambda_example.sh** - AWS Lambda API (Linux/Mac)

### 📚 Library Examples
- **library_example.py** - Direct Python library usage

### 🔄 Workflow Automation
- **n8n_workflow.json** - Complete n8n workflow for visual automation
  - Import into n8n platform
  - Orchestrates Extract → Transform → Generate flow
  - Includes API authentication and CSV generation
  - See [N8N_INTEGRATION.md](../docs/N8N_INTEGRATION.md) for details

### 📂 Test Files
- **file_examples/** - Sample input files for testing
  - Valid emails, invalid formats, edge cases
  - See [file_examples/README.md](file_examples/README.md)

### 🧪 Test Suite
- **tests/run_tests.py** - Automated test runner

## 🚀 Quick Start

### CLI
```bash
# Windows
cli_example.bat

# Linux/Mac
sh cli_example.sh
```

### API (Local)
```bash
python api_example.py
```

### API (Lambda)
```bash
# Windows
lambda_example.bat

# Linux/Mac
sh lambda_example.sh
```

### Library
```bash
python library_example.py
```

### n8n Workflow
1. Open n8n
2. Import `n8n_workflow.json`
3. Update API key in HTTP Request nodes
4. Execute workflow

## 📖 Documentation

- **[Quick Start Guide](../docs/QUICK_START.md)**
- **[n8n Integration](../docs/N8N_INTEGRATION.md)**
- **[API Documentation](../docs/API_LAMBDA.md)**
- **[Deployment Guide](../docs/DEPLOYMENT_GUIDE.md)**
