# Ejemplos

## 📁 Ejemplos Disponibles

### 🔧 Ejemplos CLI
- **cli_example.bat** - Uso desde línea de comandos en Windows
- **cli_example.sh** - Uso desde línea de comandos en Linux/Mac

### 🌐 Ejemplos API
- **api_example.py** - Uso del servidor API local
- **lambda_example.bat** - API de AWS Lambda (Windows)
- **lambda_example.sh** - API de AWS Lambda (Linux/Mac)

### 📚 Ejemplos de Librería
- **library_example.py** - Uso directo de la librería Python

### 🔄 Automatización de Flujos de Trabajo
- **n8n_workflow.json** - Flujo completo de n8n para automatización visual
  - Importar en la plataforma n8n
  - Orquesta el flujo Extraer → Transformar → Generar
  - Incluye autenticación de API y generación de CSV
  - Ver [N8N_INTEGRATION.md](../docs/N8N_INTEGRATION.md) para detalles

### 📂 Archivos de Prueba
- **file_examples/** - Archivos de entrada de ejemplo para pruebas
  - Emails válidos, formatos inválidos, casos extremos
  - Ver [file_examples/README.md](file_examples/README.md)

### 🧪 Suite de Pruebas
- **tests/run_tests.py** - Ejecutor de pruebas automatizadas

## 🚀 Inicio Rápido

### CLI (PyPI - Recomendado)
```bash
# Instalar
pip install email-processor-cli

# Usar
email-processor --input-type list --input "user@old.com" --new-domain new.com --output-type inline
```

### CLI (Código Fuente)
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

### Librería
```bash
python library_example.py
```

### Flujo de Trabajo n8n
1. Abre n8n
2. Importa `n8n_workflow.json`
3. Actualiza la API key en los nodos HTTP Request
4. Ejecuta el flujo de trabajo

## 📖 Documentación

- **[Guía de Inicio Rápido](../docs/QUICK_START.md)**
- **[Integración con n8n](../docs/N8N_INTEGRATION.md)**
- **[Documentación de API](../docs/API_LAMBDA.md)**
- **[Guía de Despliegue](../docs/DEPLOYMENT_GUIDE.md)**
