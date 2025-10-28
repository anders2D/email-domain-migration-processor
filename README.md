# Procesador de Correos - Arquitectura Hexagonal

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/email-processor-cli.svg)](https://pypi.org/project/email-processor-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple.svg)](https://www.terraform.io/)

> Sistema de migración de dominios de correo electrónico con arquitectura hexagonal, multi-interfaz (CLI, API, Librería) y despliegue en AWS Lambda.

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-principios-de-arquitectura)
- [Lógica de Negocio](#-lógica-de-negocio)
- [Instalación](#-instalación)
- [Inicio Rápido](#-inicio-rápido)
- [Documentación](#-documentación)
- [Seguridad](#-seguridad)
- [Despliegue](#-despliegue)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

## ✨ Características

- ✅ **Arquitectura Hexagonal** - Núcleo de negocio aislado de infraestructura
- ✅ **Multi-interfaz** - CLI, API REST (local + Lambda), Librería Python
- ✅ **Sin Estado** - Stateless, escalable horizontalmente
- ✅ **Validación Robusta** - 5 reglas de negocio (BR-001 a BR-005)
- ✅ **Transformación Inteligente** - 5 reglas de transformación (TR-001 a TR-005)
- ✅ **E/S Flexible** - Múltiples formatos de entrada/salida (CSV, JSON, inline)
- ✅ **Seguridad** - Autenticación con API Key en Lambda
- ✅ **IaC** - Infraestructura como código con Terraform
- ✅ **Logging** - CloudWatch logs con retención configurable
- ✅ **Documentación Completa** - PDD, diagramas Mermaid, guías de uso

## 🎯 Principios de Arquitectura

- ✅ **Sin Estado**: Sin estado entre peticiones
- ✅ **Modular**: Patrón Extraer → Transformar → Generar
- ✅ **Hexagonal**: Núcleo aislado de la infraestructura
- ✅ **Multi-interfaz**: CLI, API (Local + Lambda), Librería
- ✅ **E/S Flexible**: Múltiples tipos de entrada/salida

## 💼 Lógica de Negocio

### Flujo Principal

El sistema procesa direcciones de correo electrónico extrayendo información de usuario y migrándolas a un nuevo dominio:

1. **Extraer**: Leer correos de varias fuentes (archivo, lista, texto)
2. **Validar**: Aplicar reglas de negocio BR-001 a BR-005
3. **Transformar**: Aplicar reglas de transformación TR-001 a TR-005
4. **Generar**: Producir resultados en formato CSV, JSON o en línea

### Reglas de Validación (BR)

| ID | Regla | Condición | Acción si Falla |
|----|-------|-----------|------------------|
| BR-001 | Exactamente un @ | `email.count('@') == 1` | Registrar y omitir |
| BR-002 | Exactamente un punto en prefijo | `prefix.count('.') == 1` | Registrar y omitir |
| BR-003 | Nombre 2-50 caracteres | `2 ≤ len(nombre) ≤ 50` | Registrar y omitir |
| BR-004 | Apellido 2-50 caracteres | `2 ≤ len(apellido) ≤ 50` | Registrar y omitir |
| BR-005 | Solo letras (a-z, A-Z, acentuadas) | `nombre.isalpha()` | Registrar y omitir |

**Nota:** Todas las validaciones se ejecutan secuencialmente. Si alguna falla, el correo se registra y se omite.

### Reglas de Transformación (TR)

| ID | Regla | Entrada Ejemplo | Salida Ejemplo |
|----|-------|-----------------|----------------|
| TR-001 | Capitalizar nombre | juan | Juan |
| TR-002 | Capitalizar apellido | perez | Perez |
| TR-003 | Minúsculas en correo | Juan.Perez@NEW.COM | juan.perez@new.com |
| TR-004 | Preservar dominio original | juan.perez@example.com | @example.com |
| TR-005 | Aplicar nuevo dominio | Juan + Perez + @new.com | juan.perez@new.com |

**Nota:** Las transformaciones solo se aplican a correos que pasaron todas las validaciones.

### Entidad de Dominio (Email)

**Propiedades:**
- `nombre`: Nombre (capitalizado)
- `apellido`: Apellido (capitalizado)
- `correo_original`: Dirección de correo original
- `correo_nuevo`: Nuevo correo con dominio destino

**Comportamiento:**
- Capitaliza nombres automáticamente
- Convierte correos a minúsculas automáticamente
- Genera nuevo correo: `nombre.apellido@nuevo_dominio`

### Métricas del Proceso

| Métrica | Valor |
|---------|-------|
| Velocidad de procesamiento | ~0.1 seg/correo |
| Tasa de éxito | 90-95% |
| Errores de validación | 5-10% |
| Capacidad | 10,000+ correos/día (automatizado) |

## 🏗️ Estructura

```
src/features/email_processing/
├── domain/              # Lógica de Negocio Principal
│   ├── email.py        # Entidad
│   └── ports.py        # Interfaces
├── adapters/
│   ├── input/          # Adaptadores Primarios
│   │   ├── cli_adapter.py
│   │   ├── api_adapter.py
│   │   └── library_adapter.py
│   └── output/         # Adaptadores Secundarios
│       ├── file_adapter.py
│       ├── csv_adapter.py
│       └── json_adapter.py
└── shared/             # Validación y Logging
```

## 📦 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- AWS CLI (solo para despliegue en Lambda)
- Terraform 1.0+ (solo para despliegue en Lambda)

### Opción 1: Desde PyPI (Recomendado)

```bash
pip install email-processor-cli
```

### Opción 2: Desde Código Fuente

```bash
# Clonar repositorio
git clone https://github.com/anders2d/hiperautomatization.git
cd hiperautomatization

# Instalar dependencias
pip install -r requirements.txt

# Verificar instalación
python main_cli.py --help
```

## 🚀 Inicio Rápido

### CLI

**Instalado desde PyPI:**
```bash
email-processor --input-type list --input "user@old.com" --new-domain new.com --output-type inline
```

**Desde código fuente:**
```bash
python main_cli.py --input-type list --input "user@old.com" --new-domain new.com --output-type inline
```

### 🎬 Demos en Acción

<details>
<summary><b>Demo Básico - Procesamiento Inline</b></summary>
<br>
<img src="demos/demo_basic.svg" alt="Demo Básico">
</details>

<details>
<summary><b>Validación de Errores - Reglas de Negocio</b></summary>
<br>
<img src="demos/demo_validation.svg" alt="Demo Validación">
</details>

<details>
<summary><b>Salida CSV - Formato Estructurado</b></summary>
<br>
<img src="demos/demo_csv.svg" alt="Demo CSV">
</details>

**Ver más demos:** [demos/README.md](demos/README.md)

### API (Local)
```bash
# Iniciar servidor
python main_api.py

# Probar
python test_api.py
```

### API (AWS Lambda)
```bash
cd terraform
build.bat  # o ./build.sh
terraform apply

# Obtener API Key
terraform output api_key
```

**Autenticación:** Todas las peticiones a la API Lambda requieren el header `x-api-key`.

```bash
# Ejemplo con API Key
curl -X POST https://your-api.execute-api.us-east-1.amazonaws.com/transform \
  -H "Content-Type: application/json" \
  -H "x-api-key: prod-email-processor-2024-secure-key" \
  -d '{"emails":["user@old.com"],"new_domain":"new.com"}'
```

### Librería
```python
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary

emails = EmailProcessingLibrary.extract(['user@old.com'], 'list')
transformed = EmailProcessingLibrary.transform(emails, 'new.com')
result = EmailProcessingLibrary.generate(transformed, 'inline')
```

## 📋 Tipos de Entrada
- **file**: Leer desde ruta de archivo
- **list**: Array de correos
- **text**: Texto separado por líneas

## 📋 Tipos de Salida
- **csv**: Guardar en archivo CSV (predeterminado)
- **json**: Guardar en archivo JSON
- **inline**: Retornar/imprimir directamente
- **silent**: Procesar sin salida (solo logs)

## 🔐 Seguridad

### Autenticación con API Key

La API Lambda usa autenticación con API Key:

- **Header:** `x-api-key`
- **Clave por defecto:** `prod-email-processor-2024-secure-key`
- **Variable de entorno:** `API_KEY` en Lambda
- **Respuesta en caso de fallo:** `401 Unauthorized`

**Obtener API Key después del despliegue:**
```bash
cd terraform
terraform output api_key
```

**Probar autenticación:**
```bash
# Sin API Key (falla)
curl -X POST $API_URL/transform -d '{}'
# Respuesta: {"error": "Unauthorized: Invalid or missing API key"}

# Con API Key (éxito)
curl -X POST $API_URL/transform -H "x-api-key: YOUR_KEY" -d '{}'
```

## 📚 Ejemplos

Ver carpeta [examples/](examples/) para ejemplos completos:

- **[API Local](examples/api_local_example.py)** - Uso de API Flask local
- **[API Lambda](examples/api_lambda_example.sh)** - Llamadas a API en AWS con autenticación
- **[Librería Python](examples/library_example.py)** - Integración como librería
- **[CLI Windows](examples/cli_example.bat)** - Scripts batch para Windows
- **[CLI Linux/Mac](examples/cli_example.sh)** - Scripts shell para Unix
- **[n8n Workflow](examples/n8n_workflow.json)** - Flujo de automatización n8n

## 📦 Publicación en PyPI

### 🎉 Paquete Publicado

Este proyecto está disponible en PyPI:

- **Nombre:** `email-processor-cli`
- **Última versión:** `2025.10.27.183827`
- **URL:** https://pypi.org/project/email-processor-cli/

### 🚀 Publicar Nueva Versión

**Publicación automática con timestamp:**

```bash
# Windows
scripts\publish_timestamp.bat

# Linux/Mac
chmod +x scripts/publish_timestamp.sh
./scripts/publish_timestamp.sh
```

El script:
- Genera versión automática: `YYYY.MM.DD.HHMMSS`
- Actualiza archivos de configuración
- Construye el paquete
- Publica en PyPI o TestPyPI

**Formato de versión:**
- `2025.01.27.143052` - 27 enero 2025, 14:30:52
- `2025.02.15.091523` - 15 febrero 2025, 09:15:23

### 📚 Guías de Publicación

- **[docs/PYPI_DEPLOYMENT.md](docs/PYPI_DEPLOYMENT.md)** - Documentación completa
- **[PYPI_COMMANDS.md](PYPI_COMMANDS.md)** - Referencia rápida de comandos

## 🧪 Pruebas

```bash
# Pruebas de API local
python test_api.py

# Pruebas de CLI
python main_cli.py --input-type list --input "test@example.com" --new-domain new.com --output-type inline

# Pruebas de librería
python examples/library_example.py
```

## 📖 Documentación

### 🚀 Guías de Usuario

| Documento | Descripción | Audiencia |
|-----------|-------------|----------|
| **[Inicio Rápido](docs/QUICK_START.md)** | Comienza en 5 minutos | Todos |
| **[Guía de Despliegue](docs/DEPLOYMENT_GUIDE.md)** | Despliegue completo en AWS | DevOps |
| **[Hoja de Referencia](docs/CHEATSHEET.md)** | Comandos y configuraciones | Desarrolladores |
| **[Integración n8n](docs/N8N_INTEGRATION.md)** | Automatización con n8n | Automatización |
| **[Publicación PyPI](docs/PYPI_DEPLOYMENT.md)** | Publicar paquete en PyPI | Mantenedores |
| **[Comandos PyPI](PYPI_COMMANDS.md)** | Referencia rápida de comandos | Desarrolladores |

### 📋 Documentación de Procesos (PDD)

**[Process Definition Document](docs/pdd/PDD.md)** - Documentación completa del proceso de negocio:

| Sección | Contenido | Propósito |
|---------|-----------|----------|
| **Proceso AS-IS** | Proceso manual actual | Entender estado actual |
| **Reglas de Negocio** | BR-001 a BR-005, TR-001 a TR-005 | Validación y transformación |
| **Análisis de Automatización** | Viabilidad y mapeo tecnológico | Justificar automatización |
| **Visión TO-BE** | Proceso automatizado | Diseñar solución |
| **Evaluación de Riesgos** | Riesgos y mitigación | Gestión de riesgos |
| **Roadmap** | Plan de 6 meses | Implementación gradual |

### 📊 Diagramas de Procesos

**[docs/pdd/diagrams/](docs/pdd/diagrams/)** - Documentación visual de procesos:

| Diagrama | Descripción | Sección |
|----------|-------------|----------|
| `macroproceso.mmd` | Contexto organizacional (upstream/downstream) | 1.1 |
| `swimlanes.mmd` | Secuencia de interacción de actores | 1.1 |
| `alcance.mmd` | Visualización de alcance (dentro/fuera) | 1.2 |
| `entradas-salidas.mmd` | Flujo de datos entrada/salida | 1.3-1.4 |
| `flujo-detallado.mmd` | Flujo manual AS-IS detallado | 1.8 |
| `heatmap-automatizacion.mmd` | Mapa de calor de viabilidad de automatización | 4.2 |
| `proceso-tobe.mmd` | Proceso automatizado TO-BE | 5.1 |
| `roadmap-transicion.mmd` | Gantt de transición de 6 meses | 5.3 |

## 🚢 Despliegue

### Despliegue Local

```bash
# API Local
python main_api.py
# Servidor en http://localhost:5000

# CLI
python main_cli.py --input-type file --input sample_emails.txt --new-domain new.com
```

### Despliegue en AWS Lambda

Ver **[terraform/README.md](terraform/README.md)** para instrucciones completas.

```bash
cd terraform

# Windows
build.bat

# Linux/Mac
./build.sh

# Desplegar infraestructura
terraform init
terraform plan
terraform apply

# Obtener API Key
terraform output api_key
```

### Monitoreo y Logs

**CloudWatch Logs:**

| Recurso | Log Group | Retención |
|---------|-----------|----------|
| Lambda Function | `/aws/lambda/email-processor` | 7 días |
| API Gateway | `/aws/apigateway/email-processor` | 7 días |

**Métricas incluidas:**
- Request/response completos
- Errores y excepciones
- Fallos de validación (BR-001 a BR-005)
- Validación de API key
- Tiempos de ejecución

## 👤 Autor

**Anderson Taguada**

- GitHub: [@anders2d](https://github.com/anders2d)
- Email: ferchoafta@gmail.com