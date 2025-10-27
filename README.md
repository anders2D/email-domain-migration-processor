# Procesador de Correos - Arquitectura Hexagonal

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

## 🚀 Inicio Rápido

### CLI
```bash
python main_cli.py --input-type list --input "user@old.com" --new-domain new.com --output-type inline
```

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

Ver carpeta [examples/](examples/) para ejemplos completos de uso:
- Ejemplos de API (local + Lambda con API Key)
- Ejemplos de librería
- Ejemplos de CLI (Windows + Linux/Mac)

## 🧪 Pruebas

```bash
python test_api.py
```

## 📖 Documentación

### 🚀 Primeros Pasos

- **[Guía de Inicio Rápido](docs/QUICK_START.md)** - Comienza a usar en 5 minutos con ejemplos prácticos
- **[Guía de Despliegue](docs/DEPLOYMENT_GUIDE.md)** - Documentación completa de despliegue y uso
- **[Hoja de Referencia](docs/CHEATSHEET.md)** - Referencia rápida de comandos y configuraciones
- **[Integración n8n](docs/N8N_INTEGRATION.md)** - Automatización de flujos con plataforma n8n

### 📋 Documentación de Procesos

**[docs/pdd/PDD.md](docs/pdd/PDD.md)** - Documentación completa del proceso de negocio:

- 📄 **Proceso AS-IS:** Descripción del proceso manual con actores, pasos y métricas
- 📊 **Reglas de Negocio:** Validación (BR-001 a BR-005) y reglas de transformación (TR-001 a TR-005)
- 🤖 **Análisis de Automatización:** Viabilidad de automatización 100% con mapeo de tecnologías
- 🚀 **Visión TO-BE:** Diseño del proceso automatizado y comparación de beneficios
- ⚠️ **Evaluación de Riesgos:** Riesgos operacionales, de seguridad y cumplimiento con estrategias de mitigación
- 📅 **Hoja de Ruta de Transición:** Plan de implementación de 6 meses

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

**Generar Diagramas:**
```bash
cd docs/pdd/diagrams
sh convert.sh
```

**Requisitos:**
```bash
npm install -g @mermaid-js/mermaid-cli
```

## 🚢 Despliegue

Ver [terraform/README.md](terraform/README.md) para instrucciones de despliegue en AWS.

### Logs de CloudWatch

Los logs se guardan automáticamente en CloudWatch:

- **Logs de Lambda:** `/aws/lambda/email-processor`
- **Logs de API Gateway:** `/aws/apigateway/email-processor`
- **Retención:** 7 días
- **Incluye:** Request/response, errores, fallos de validación, validación de API key