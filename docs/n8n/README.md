# Guía de Integración con n8n

## 🎯 Descripción General

Integración del Procesador de Emails con n8n para orquestar el proceso de transformación de emails visualmente.

## 🏗️ Arquitectura

El flujo invoca la API del Procesador de Emails (AWS Lambda) en tres pasos:

```
Datos de Entrada → Extraer → Transformar → Generar → Salida CSV
```

![Flujo de Trabajo n8n](n8n_flow.png)

## 📋 Requisitos Previos

- Instancia de n8n (cloud o auto-hospedada)
- API del Procesador de Emails desplegada en AWS Lambda
- API Key para autenticación

## 🚀 Inicio Rápido

### 1. Importar Flujo de Trabajo

1. Abre n8n
2. **Workflows** → **Import from File**
3. Selecciona `examples/n8n_workflow.json`
4. Haz clic en **Import**

### 2. Configurar API Key

Actualiza la API Key en todos los nodos HTTP Request:

1. Abre cada nodo: **1. Extract**, **2. Transform**, **3. Generate CSV**
2. Sección **Headers**
3. Actualiza `x-api-key` con tu API key
4. Actualiza la URL si usas un endpoint diferente

**Obtener API Key:**
```bash
cd terraform
terraform output api_key
```

### 3. Probar Flujo

1. Clic en **Execute Workflow**
2. Verifica resultados en cada nodo
3. Descarga el CSV generado

## 🔧 Configuración de Nodos

### Nodo 1: Datos de Entrada

**Tipo:** Set Node

```json
{
  "emails": "[\"user1@old.com\",\"user2@old.com\"]",
  "new_domain": "company.com"
}
```

### Nodo 2: Extraer

**Endpoint:** `/extract`  
**Método:** POST

```json
{
  "input": ["user1@old.com", "user2@old.com"],
  "input_type": "list"
}
```

### Nodo 3: Transformar

**Endpoint:** `/transform`  
**Método:** POST

```json
{
  "emails": ["user1@old.com", "user2@old.com"],
  "new_domain": "company.com"
}
```

### Nodo 4: Generar CSV

**Endpoint:** `/generate`  
**Método:** POST

```json
{
  "transformed": [...],
  "output_type": "csv"
}
```

### Nodo 5: Preparar Descarga CSV

**Tipo:** Code Node

```javascript
const item = $input.first().json;
const csvContent = item.output || '';
const fileName = 'emails_transformed_' + new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5) + '.csv';

return [{
  json: {
    fileName: fileName,
    csvContent: csvContent,
    count: item.count || 0,
    format: item.format || 'csv'
  },
  binary: {
    data: {
      data: Buffer.from(csvContent, 'utf-8').toString('base64'),
      mimeType: 'text/csv',
      fileName: fileName
    }
  }
}];
```

## 🔄 Flujos Avanzados

### Procesamiento Programado

```
Cron Trigger → Leer Archivo → Extraer → Transformar → Generar → Enviar Email
```

**Configuración Cron:**
- **Modo:** Todos los días
- **Hora:** 9:00 AM

### Notificación por Email

```
Generar CSV → Preparar CSV → Enviar Email (con adjunto)
```

### Manejo de Errores

```
Transformar → IF (verificar errores) → Enviar Alerta
                                     → Continuar
```

**Condición:**
```javascript
{{ $json.errors.length > 0 }}
```

### Procesamiento Multi-Dominio

```
Entrada → Dividir → Transformar (dominio1)
                  → Transformar (dominio2)
                  → Transformar (dominio3)
        → Combinar → Generar CSV
```

## 🔐 Mejores Prácticas

### Gestión de API Keys

**Usa Credentials de n8n:**

1. Crea credencial: **Header Auth**
2. Nombre del encabezado: `x-api-key`
3. Valor: Tu API key
4. Referencia en nodos HTTP Request

### Variables de Entorno

```bash
# .env (n8n auto-hospedado)
EMAIL_PROCESSOR_API_KEY=tu-api-key
EMAIL_PROCESSOR_API_URL=https://tu-api.execute-api.us-east-1.amazonaws.com
```

**Acceso:**
```javascript
{{ $env.EMAIL_PROCESSOR_API_KEY }}
```

## 🐛 Solución de Problemas

### Error: 401 Unauthorized

**Solución:**
1. Verifica API key en encabezados
2. Revisa API key en AWS API Gateway
3. Nombre del encabezado: `x-api-key`

### Error: 500 Internal Server Error

**Solución:**
1. Revisa logs: `/aws/lambda/email-processor`
2. Verifica formato del cuerpo
3. Prueba con curl o Postman

### Error: Timeout

**Solución:**
1. Aumenta timeout en n8n (default: 300s)
2. Procesa en lotes más pequeños
3. Aumenta timeout de Lambda

### Salida CSV Vacía

**Solución:**
1. Revisa array `errors` en Transform
2. Verifica reglas de validación (BR-001 a BR-005)
3. Corrige formato de emails

## 📚 Ejemplos

### Ejemplo 1: Procesamiento Básico

**Entrada:**
```json
{
  "emails": ["john.doe@old.com", "jane.smith@old.com"],
  "new_domain": "new.com"
}
```

**Salida:**
```csv
Nombre,Apellido,Correo Ejemplo,Correo Nuevo
John,Doe,john.doe@old.com,john.doe@new.com
Jane,Smith,jane.smith@old.com,jane.smith@new.com
```

### Ejemplo 2: Con Errores

**Entrada:**
```json
{
  "emails": ["valid@old.com", "invalid", "no@at@sign.com"],
  "new_domain": "new.com"
}
```

**Respuesta:**
```json
{
  "transformed": [{...}],
  "count": 1,
  "errors": [
    "Email 'invalid' no contiene exactamente un '@'",
    "Email 'no@at@sign.com' no contiene exactamente un '@'"
  ]
}
```

## 🔗 Patrones de Integración

### Patrón 1: Subir → Procesar → Descargar

```
Webhook (subir) → Extraer → Transformar → Generar → Retornar CSV
```

### Patrón 2: Procesamiento Programado

```
Cron → Leer SharePoint → Extraer → Transformar → Generar → Subir a S3
```

### Patrón 3: Basado en Eventos

```
SQS Trigger → Extraer → Transformar → Generar → SNS Notificación
```

### Patrón 4: Aprobación Multi-Paso

```
Extraer → Transformar → Email Aprobación → Esperar → Generar → Entregar
```

## 📖 Recursos

- **JSON del Flujo:** `examples/n8n_workflow.json`
- **Documentación de n8n:** https://docs.n8n.io
- **Documentación de API:** `docs/API_LAMBDA.md`
- **Guía de Despliegue:** `docs/DEPLOYMENT_GUIDE.md`
