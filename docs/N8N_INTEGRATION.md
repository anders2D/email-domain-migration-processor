# Guía de Integración con n8n

## 🎯 Descripción General

Esta guía explica cómo integrar el Procesador de Emails con n8n, una plataforma de automatización de flujos de trabajo. La integración permite orquestar el proceso de transformación de emails visualmente y conectarlo con otros servicios.

## 🏗️ Arquitectura

El flujo de trabajo de n8n invoca la API del Procesador de Emails (AWS Lambda) en tres pasos secuenciales:

```
Datos de Entrada → Extraer → Transformar → Generar → Salida CSV
```

Cada paso corresponde a un endpoint de la API que sigue el patrón de arquitectura hexagonal.

![Flujo de n8n](n8n_flow.png)

## 📋 Requisitos Previos

- Instancia de n8n (cloud o auto-hospedada)
- API del Procesador de Emails desplegada en AWS Lambda
- API Key para autenticación

## 🚀 Inicio Rápido

### 1. Importar Flujo de Trabajo

Importa el flujo preconfigurado desde `examples/n8n_workflow.json`:

1. Abre n8n
2. Haz clic en **Workflows** → **Import from File**
3. Selecciona `examples/n8n_workflow.json`
4. Haz clic en **Import**

### 2. Configurar Credenciales de API

Actualiza la API Key en todos los nodos HTTP Request:

1. Abre cada nodo: **1. Extract**, **2. Transform**, **3. Generate CSV**
2. Navega a la sección **Headers**
3. Actualiza el valor de `x-api-key` con tu API key
4. Actualiza la URL de la API si usas un endpoint diferente

**Obtener tu API Key:**
```bash
cd terraform
terraform output api_key
```

### 3. Probar Flujo de Trabajo

1. Haz clic en el botón **Execute Workflow**
2. Verifica los resultados de ejecución en cada nodo
3. Descarga el CSV generado desde el último nodo

## 🔧 Configuración del Flujo de Trabajo

### Nodo 1: Datos de Entrada

**Tipo:** Set Node  
**Propósito:** Definir emails de entrada y dominio objetivo

**Configuración:**
```json
{
  "emails": "[\"user1@old.com\",\"user2@old.com\"]",
  "new_domain": "company.com"
}
```

**Personalización:**
- Modifica el array `emails` con tu lista de correos
- Cambia `new_domain` a tu dominio objetivo

### Nodo 2: Extraer

**Tipo:** HTTP Request  
**Método:** POST  
**Endpoint:** `/extract`

**Encabezados:**
```
x-api-key: prod-email-processor-2024-secure-key
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "input": ["user1@old.com", "user2@old.com"],
  "input_type": "list"
}
```

**Respuesta:**
```json
{
  "emails": ["user1@old.com", "user2@old.com"],
  "count": 2,
  "source": "list"
}
```

### Nodo 3: Transformar

**Tipo:** HTTP Request  
**Método:** POST  
**Endpoint:** `/transform`

**Encabezados:**
```
x-api-key: prod-email-processor-2024-secure-key
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "emails": ["user1@old.com", "user2@old.com"],
  "new_domain": "company.com"
}
```

**Respuesta:**
```json
{
  "transformed": [
    {
      "nombre": "User1",
      "apellido": "Old",
      "correo_original": "user1@old.com",
      "correo_nuevo": "user1.old@company.com"
    }
  ],
  "count": 1,
  "errors": []
}
```

### Nodo 4: Generar CSV

**Tipo:** HTTP Request  
**Método:** POST  
**Endpoint:** `/generate`

**Encabezados:**
```
x-api-key: prod-email-processor-2024-secure-key
Content-Type: application/json
```

**Cuerpo:**
```json
{
  "transformed": [...],
  "output_type": "csv"
}
```

**Respuesta:**
```json
{
  "output": "Nombre,Apellido,Correo Ejemplo,Correo Nuevo\nUser1,Old,user1@old.com,user1.old@company.com",
  "count": 1,
  "format": "csv"
}
```

### Nodo 5: Preparar Descarga CSV

**Tipo:** Code Node  
**Propósito:** Convertir string CSV a archivo binario descargable

**Código:**
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

## 🔄 Flujos de Trabajo Avanzados

### Procesamiento Programado de Emails

Agrega un trigger **Cron** para procesar emails automáticamente:

```
Cron Trigger → Leer Archivo → Extraer → Transformar → Generar → Enviar Email
```

**Configuración Cron:**
- **Modo:** Todos los días
- **Hora:** 9:00 AM
- **Zona horaria:** Tu zona horaria

### Notificación por Email

Agrega un nodo **Email** después de la generación del CSV:

```
Generar CSV → Preparar CSV → Enviar Email (con adjunto)
```

**Configuración de Email:**
- **Para:** destinatario@empresa.com
- **Asunto:** Resultados del Procesamiento de Emails
- **Adjuntos:** Usar datos binarios del nodo anterior

### Manejo de Errores

Agrega un nodo **IF** para manejar errores:

```
Transformar → IF (verificar errores) → Enviar Email de Alerta
                                     → Continuar a Generar
```

**Condición IF:**
```javascript
{{ $json.errors.length > 0 }}
```

### Procesamiento Multi-Dominio

Procesa emails para múltiples dominios en paralelo:

```
Entrada → Dividir en Lotes → Transformar (dominio1)
                           → Transformar (dominio2)
                           → Transformar (dominio3)
        → Combinar → Generar CSV
```

## 📊 Monitoreo

### Logs de Ejecución

Ver detalles de ejecución en n8n:

1. Ve a la pestaña **Executions**
2. Haz clic en cualquier ejecución
3. Revisa la entrada/salida de cada nodo
4. Verifica mensajes de error si los hay

### Integración con CloudWatch

Monitorea invocaciones de Lambda desde n8n:

- **Grupo de Logs:** `/aws/lambda/email-processor`
- **Métricas:** Invocaciones, Errores, Duración
- **Retención:** 7 días

## 🔐 Mejores Prácticas de Seguridad

### Gestión de API Keys

**No codifiques API keys directamente en los flujos:**

1. Usa la funcionalidad **Credentials** de n8n
2. Crea un nuevo tipo de credencial: **Header Auth**
3. Establece el nombre del encabezado: `x-api-key`
4. Establece el valor del encabezado: Tu API key
5. Referencia la credencial en los nodos HTTP Request

### Variables de Entorno

Almacena datos sensibles en variables de entorno de n8n:

```bash
# archivo .env (n8n auto-hospedado)
EMAIL_PROCESSOR_API_KEY=tu-api-key
EMAIL_PROCESSOR_API_URL=https://tu-api.execute-api.us-east-1.amazonaws.com
```

**Acceso en el flujo:**
```javascript
{{ $env.EMAIL_PROCESSOR_API_KEY }}
```

### Seguridad de Red

- Usa únicamente endpoints HTTPS
- Habilita throttling en API Gateway
- Implementa lista blanca de IPs si es necesario
- Usa endpoints VPC para APIs privadas

## 🐛 Solución de Problemas

### Error: 401 Unauthorized

**Causa:** API key inválida o faltante

**Solución:**
1. Verifica la API key en los encabezados HTTP Request
2. Revisa la API key en AWS API Gateway
3. Asegúrate de que el nombre del encabezado sea exactamente `x-api-key`

### Error: 500 Internal Server Error

**Causa:** Error de ejecución de Lambda

**Solución:**
1. Revisa los logs de CloudWatch: `/aws/lambda/email-processor`
2. Verifica el formato del cuerpo de la petición
3. Prueba el endpoint con curl o Postman

### Error: Timeout

**Causa:** Arranque en frío de Lambda o dataset grande

**Solución:**
1. Aumenta el timeout de HTTP Request en n8n (por defecto: 300s)
2. Procesa emails en lotes más pequeños
3. Aumenta el timeout de Lambda en Terraform

### Salida CSV Vacía

**Causa:** Todos los emails fallaron la validación

**Solución:**
1. Revisa el array `errors` en la respuesta de Transform
2. Revisa las reglas de validación (BR-001 a BR-005)
3. Corrige el formato de los emails en los datos de entrada

## 📚 Ejemplos

### Ejemplo 1: Procesamiento Básico

**Entrada:**
```json
{
  "emails": ["john.doe@old.com", "jane.smith@old.com"],
  "new_domain": "new.com"
}
```

**Salida CSV:**
```csv
Nombre,Apellido,Correo Ejemplo,Correo Nuevo
John,Doe,john.doe@old.com,john.doe@new.com
Jane,Smith,jane.smith@old.com,jane.smith@new.com
```

### Ejemplo 2: Con Errores de Validación

**Entrada:**
```json
{
  "emails": ["valid@old.com", "invalid", "no@at@sign.com"],
  "new_domain": "new.com"
}
```

**Respuesta de Transform:**
```json
{
  "transformed": [
    {
      "nombre": "Valid",
      "apellido": "Old",
      "correo_original": "valid@old.com",
      "correo_nuevo": "valid.old@new.com"
    }
  ],
  "count": 1,
  "errors": [
    "Email 'invalid' no contiene exactamente un '@'",
    "Email 'no@at@sign.com' no contiene exactamente un '@'"
  ]
}
```

### Ejemplo 3: Procesamiento por Lotes

Procesa 1000+ emails en lotes de 100:

```
Leer Archivo → Dividir en Lotes (100) → Extraer → Transformar → Generar → Combinar Resultados
```

## 🔗 Patrones de Integración

### Patrón 1: Subir Archivo → Procesar → Descargar

```
Webhook (subir archivo) → Extraer → Transformar → Generar → Retornar CSV
```

### Patrón 2: Procesamiento por Lotes Programado

```
Cron → Leer SharePoint → Extraer → Transformar → Generar → Subir a S3
```

### Patrón 3: Procesamiento Basado en Eventos

```
SQS Trigger → Extraer → Transformar → Generar → Enviar Notificación SNS
```

### Patrón 4: Aprobación Multi-Paso

```
Extraer → Transformar → Enviar Email de Aprobación → Esperar Aprobación → Generar → Entregar
```

## 📖 Recursos Adicionales

- **Documentación de n8n:** https://docs.n8n.io
- **Plantilla de Flujo:** `examples/n8n_workflow.json`
- **Flujo Visual:** `docs/n8n/n8n_flow.png`
- **Documentación de API:** `docs/API_LAMBDA.md`
- **Guía de Despliegue:** `docs/DEPLOYMENT_GUIDE.md`

## 🆘 Soporte

Para problemas o preguntas:

1. Revisa los logs de CloudWatch para errores de Lambda
2. Revisa los logs de ejecución de n8n
3. Prueba los endpoints de la API independientemente con curl
4. Verifica la API key y las URLs de los endpoints
5. Revisa las reglas de validación en README.md
