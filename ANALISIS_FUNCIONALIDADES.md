# Análisis de Funcionalidades - CLI vs Librería vs API

## 📊 Resumen Ejecutivo

| Característica | CLI | Librería | API Local | API Lambda |
|----------------|-----|----------|-----------|------------|
| **Tipos de entrada** | ✅ file, list, text | ✅ file, list, text | ✅ file, list, text | ⚠️ list, text, file* |
| **Tipos de salida** | ✅ csv, json, inline, silent | ✅ csv, json, inline, silent | ✅ csv, json, inline, silent | ✅ csv, json, inline, silent |
| **Archivos de entrada** | ✅ Ruta local | ✅ Ruta local | ✅ Ruta local | ⚠️ Base64 |
| **Archivos de salida** | ✅ Guarda en disco | ✅ Guarda en disco | ⚠️ No guarda | ⚠️ Retorna string |
| **Error logging** | ✅ error_log.txt | ❌ No | ❌ No | ❌ No |
| **Summary report** | ✅ summary.txt | ❌ No | ❌ No | ❌ No |
| **Validación BR-001 a BR-005** | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| **Transformación TR-001 a TR-005** | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Sí |
| **Autenticación** | ❌ No | ❌ No | ❌ No | ✅ API Key |

**Leyenda:**
- ✅ Funcionalidad completa
- ⚠️ Funcionalidad parcial o con limitaciones
- ❌ No disponible

---

## 🔍 Análisis Detallado

### 1. Tipos de Entrada (Input Types)

#### ✅ CLI - COMPLETO
```bash
# file - Lee desde archivo local
--input-type file --input sample_emails.txt

# list - Lista separada por comas
--input-type list --input "juan.perez@old.com,maria.garcia@old.com"

# text - Texto con saltos de línea
--input-type text --input "juan.perez@old.com\nmaria.garcia@old.com"
```

**Implementación:** `cli_adapter.py` líneas 60-72
```python
if input_type == 'file':
    emails = FileEmailRepository().read(input_data)
elif input_type == 'list':
    emails = input_data.split(',') if isinstance(input_data, str) else input_data
elif input_type == 'text':
    emails = [e.strip() for e in input_data.split('\n') if e.strip()]
```

#### ✅ Librería - COMPLETO
```python
# file
emails = EmailProcessingLibrary.extract('sample_emails.txt', 'file')

# list
emails = EmailProcessingLibrary.extract(['juan.perez@old.com'], 'list')

# text
emails = EmailProcessingLibrary.extract("juan.perez@old.com\nmaria.garcia@old.com", 'text')
```

**Implementación:** `library_adapter.py` líneas 24-40

#### ✅ API Local - COMPLETO
```bash
# file
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"input_type":"file","input":"sample_emails.txt"}'

# list
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"input_type":"list","input":["juan.perez@old.com"]}'

# text
curl -X POST http://localhost:5000/extract \
  -H "Content-Type: application/json" \
  -d '{"input_type":"text","input":"juan.perez@old.com\nmaria.garcia@old.com"}'
```

**Implementación:** `api_adapter.py` líneas 32-48

#### ⚠️ API Lambda - PARCIAL (file requiere Base64)
```bash
# list - FUNCIONA IGUAL
curl -X POST $API_URL/extract \
  -H "x-api-key: YOUR_KEY" \
  -d '{"input_type":"list","input":["juan.perez@old.com"]}'

# text - FUNCIONA IGUAL
curl -X POST $API_URL/extract \
  -H "x-api-key: YOUR_KEY" \
  -d '{"input_type":"text","input":"juan.perez@old.com\nmaria.garcia@old.com"}'

# file - REQUIERE BASE64 (diferente)
curl -X POST $API_URL/extract \
  -H "x-api-key: YOUR_KEY" \
  -d '{"input_type":"file","file_content":"anVhbi5wZXJlekBvbGQuY29t"}'
```

**Implementación:** `lambda_adapter.py` líneas 22-38
```python
if input_type == 'file':
    file_content = data.get('file_content')  # ⚠️ Requiere Base64
    if not file_content:
        raise ValueError('file_content required for input_type=file')
    decoded = base64.b64decode(file_content).decode('utf-8')
    emails = [e.strip() for e in decoded.split('\n') if e.strip()]
```

**🔴 PROBLEMA:** Lambda no puede leer archivos del sistema de archivos local. Requiere que el contenido del archivo se envíe codificado en Base64.

---

### 2. Tipos de Salida (Output Types)

#### ✅ CLI - COMPLETO (guarda archivos en disco)
```bash
# csv - Guarda archivo CSV
--output-type csv --output resultado.csv

# json - Guarda archivo JSON
--output-type json --output resultado.json

# inline - Imprime en consola
--output-type inline

# silent - Sin salida visible
--output-type silent
```

**Implementación:** `cli_adapter.py` líneas 107-165
- CSV: Guarda con `CsvEmailWriter().save_emails(email_objects, output_file)`
- JSON: Guarda con `JsonEmailWriter().save_emails(email_objects, output_file)`
- Inline: Imprime con `print(email)`
- Silent: Solo retorna count

#### ✅ Librería - COMPLETO (guarda archivos en disco)
```python
# csv - Guarda archivo
result = EmailProcessingLibrary.generate(transformed, 'csv', output_file='output.csv')

# json - Guarda archivo
result = EmailProcessingLibrary.generate(transformed, 'json', output_file='output.json')

# inline - Retorna lista
emails = EmailProcessingLibrary.generate(transformed, 'inline')

# silent - Retorna count
count = EmailProcessingLibrary.generate(transformed, 'silent')
```

**Implementación:** `library_adapter.py` líneas 68-123

#### ⚠️ API Local - PARCIAL (NO guarda archivos)
```bash
# csv - NO GUARDA, requiere output_file pero no lo usa correctamente
curl -X POST http://localhost:5000/generate \
  -d '{"transformed":[...],"output_type":"csv","output_file":"result.csv"}'

# json - NO GUARDA, requiere output_file pero no lo usa correctamente
curl -X POST http://localhost:5000/generate \
  -d '{"transformed":[...],"output_type":"json","output_file":"result.json"}'

# inline - Retorna JSON con emails
curl -X POST http://localhost:5000/generate \
  -d '{"transformed":[...],"output_type":"inline"}'

# silent - Retorna count
curl -X POST http://localhost:5000/generate \
  -d '{"transformed":[...],"output_type":"silent"}'
```

**Implementación:** `api_adapter.py` líneas 95-133
```python
if output_type == 'csv':
    if not output_file:
        return jsonify({'error': 'output_file required for csv'}), 400
    from src.features.email_processing.adapters.output.csv_adapter import CsvEmailWriter
    CsvEmailWriter().write(emails, output_file)  # ⚠️ Intenta escribir pero no tiene sentido en API
    return jsonify({'output_file': output_file, 'count': len(emails)})
```

**🔴 PROBLEMA:** La API pide `output_file` pero no puede guardar archivos en el cliente. Debería retornar el contenido del CSV/JSON en la respuesta.

#### ⚠️ API Lambda - PARCIAL (retorna string, no guarda)
```bash
# csv - Retorna CSV como string
curl -X POST $API_URL/generate \
  -H "x-api-key: YOUR_KEY" \
  -d '{"transformed":[...],"output_type":"csv"}'
# Response: {"output": "Nombre,Apellido,...\nJuan,Perez,...", "format": "csv"}

# json - Retorna JSON
curl -X POST $API_URL/generate \
  -H "x-api-key: YOUR_KEY" \
  -d '{"transformed":[...],"output_type":"json"}'
# Response: {"data": [...], "format": "json"}

# inline - Retorna JSON
curl -X POST $API_URL/generate \
  -H "x-api-key: YOUR_KEY" \
  -d '{"transformed":[...],"output_type":"inline"}'

# silent - Retorna count
curl -X POST $API_URL/generate \
  -H "x-api-key: YOUR_KEY" \
  -d '{"transformed":[...],"output_type":"silent"}'
```

**Implementación:** `lambda_handler.py` líneas 78-99
```python
if output_type == 'inline':
    return response(200, {'data': valid_items, 'count': len(valid_items)})
elif output_type == 'csv':
    csv_lines = ['Nombre,Apellido,Correo Original,Correo Nuevo']
    for item in valid_items:
        csv_lines.append(f"{item['nombre']},{item['apellido']},...")
    return response(200, {'output': '\n'.join(csv_lines), 'format': 'csv'})
```

**✅ CORRECTO:** Lambda retorna el contenido como string, el cliente decide qué hacer con él.

---

### 3. Archivos de Salida Adicionales

#### ✅ CLI - COMPLETO
```bash
# Genera automáticamente:
# 1. error_log.txt - Log de errores de validación
# 2. summary.txt - Resumen con estadísticas
```

**Implementación:** `cli_adapter.py` líneas 167-207
```python
# Guardar error log
error_logger.save()  # Guarda error_log.txt

# Generar resumen
stats = {
    'total': len(emails),
    'processed': valid,
    'errors': error_logger.get_error_count(),
    ...
}
SummaryGenerator.generate(stats)  # Guarda summary.txt
```

#### ❌ Librería - NO DISPONIBLE
No genera archivos de log ni resumen automáticamente.

#### ❌ API Local - NO DISPONIBLE
No genera archivos de log ni resumen.

#### ❌ API Lambda - NO DISPONIBLE
No genera archivos de log ni resumen (solo CloudWatch logs).

---

### 4. Validación y Transformación

#### ✅ TODAS LAS INTERFACES - COMPLETO

Todas las interfaces usan el mismo `EmailProcessingService` que implementa:

**Reglas de Validación (BR-001 a BR-005):**
- BR-001: Exactamente un @
- BR-002: Exactamente un punto en prefijo
- BR-003: Nombre 2-50 caracteres
- BR-004: Apellido 2-50 caracteres
- BR-005: Solo letras

**Reglas de Transformación (TR-001 a TR-005):**
- TR-001: Capitalizar nombre
- TR-002: Capitalizar apellido
- TR-003: Minúsculas en correo
- TR-004: Preservar dominio original
- TR-005: Aplicar nuevo dominio

**Implementación compartida:** `email_service.py`

---

## 🚨 Problemas Identificados

### 1. API Local - Salida CSV/JSON no funcional
**Problema:** La API pide `output_file` pero intenta escribir en el servidor, no en el cliente.

**Código actual:**
```python
# api_adapter.py línea 100
CsvEmailWriter().write(emails, output_file)  # ⚠️ Escribe en servidor
return jsonify({'output_file': output_file, 'count': len(emails)})
```

**Solución esperada:**
```python
# Debería retornar el contenido
csv_content = generate_csv_string(emails)
return jsonify({'content': csv_content, 'format': 'csv', 'count': len(emails)})
```

### 2. Lambda - Input type 'file' inconsistente
**Problema:** Lambda requiere Base64 para archivos, mientras que otras interfaces usan rutas.

**Código actual:**
```python
# lambda_adapter.py línea 26
file_content = data.get('file_content')  # ⚠️ Requiere Base64
decoded = base64.b64decode(file_content).decode('utf-8')
```

**Impacto:** Los usuarios deben codificar archivos manualmente antes de enviarlos a Lambda.

### 3. Librería - Sin logging de errores
**Problema:** La librería no genera `error_log.txt` ni `summary.txt` como el CLI.

**Impacto:** Los usuarios que usan la librería no tienen visibilidad de errores detallados.

---

## 📋 Recomendaciones

### Prioridad Alta

1. **Arreglar API Local - Salida CSV/JSON**
   - Cambiar para que retorne contenido en lugar de intentar guardar archivos
   - Hacer consistente con Lambda

2. **Documentar diferencias de Lambda**
   - Aclarar en README que `input_type=file` requiere Base64 en Lambda
   - Agregar ejemplos de cómo codificar archivos

### Prioridad Media

3. **Agregar logging a Librería**
   - Opción para generar `error_log.txt` y `summary.txt`
   - Mantener compatibilidad con uso actual

4. **Estandarizar respuestas de APIs**
   - API Local y Lambda deberían tener el mismo formato de respuesta
   - Actualmente Lambda retorna `{'output': '...'}` y API Local retorna `{'output_file': '...'}`

### Prioridad Baja

5. **Agregar método `validate()` a CLI**
   - CLI no expone método de validación individual como la librería
   - Útil para validar correos sin transformarlos

---

## 📊 Matriz de Compatibilidad

| Caso de Uso | CLI | Librería | API Local | Lambda |
|-------------|-----|----------|-----------|--------|
| Procesar archivo local | ✅ | ✅ | ✅ | ⚠️ Base64 |
| Procesar lista de correos | ✅ | ✅ | ✅ | ✅ |
| Procesar texto con correos | ✅ | ✅ | ✅ | ✅ |
| Guardar resultado en CSV | ✅ | ✅ | ❌ | ❌ |
| Guardar resultado en JSON | ✅ | ✅ | ❌ | ❌ |
| Ver resultado en pantalla | ✅ | ✅ | ✅ | ✅ |
| Obtener solo count | ✅ | ✅ | ✅ | ✅ |
| Log de errores detallado | ✅ | ❌ | ❌ | ❌ |
| Resumen de ejecución | ✅ | ❌ | ❌ | ❌ |
| Validar sin transformar | ❌ | ✅ | ❌ | ❌ |
| Autenticación | ❌ | ❌ | ❌ | ✅ |

---

## 🎯 Conclusión

**Funcionalidades principales:** ✅ Todas las interfaces soportan las funcionalidades core (validación, transformación, tipos de entrada/salida).

**Diferencias clave:**
1. **CLI** es la interfaz más completa (logging, resumen, archivos)
2. **Librería** es flexible pero sin logging automático
3. **API Local** tiene bug en salida CSV/JSON
4. **Lambda** funciona bien pero requiere Base64 para archivos

**Acción requerida:** Arreglar API Local para que sea consistente con Lambda en el manejo de salidas CSV/JSON.
