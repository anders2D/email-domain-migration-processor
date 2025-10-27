# ⚡ Guía Rápida de Inicio

## 🎯 Inicio en 5 Minutos

### 1. Verificar Requisitos

```bash
python --version  # 3.11+
pip --version
```

### 2. Instalar Dependencias

```bash
# Desde requirements.txt (recomendado)
pip install -r requirements.txt

# O manualmente
pip install flask requests
```

### 3. Probar CLI

```bash
cd hiperautomatization

# Crear archivo de prueba
echo "juan.perez@old.com" > test.txt

# Ejecutar
python main_cli.py \
  --input-type file \
  --input test.txt \
  --new-domain company.com \
  --output-type inline
```

**Resultado esperado:**
```
juan.perez@company.com
```

---

## 🚀 Casos de Uso Comunes

### Caso 1: Migración de Dominio Corporativo

**Escenario:** Cambiar 1000 correos de `@oldcompany.com` a `@newcompany.com`

```bash
# Preparar archivo
cat employees.txt
# juan.perez@oldcompany.com
# ana.garcia@oldcompany.com
# ...

# Ejecutar migración
python main_cli.py \
  --input-type file \
  --input employees.txt \
  --new-domain newcompany.com \
  --output-type csv \
  --output migrated_emails.csv

# Revisar resultados
cat migrated_emails.csv
cat error_log.txt
cat summary.txt
```

### Caso 2: Validación de Lista de Correos

**Escenario:** Verificar formato de correos antes de importar a sistema

```bash
# Validar y filtrar correos válidos
python main_cli.py \
  --input-type file \
  --input contacts.txt \
  --new-domain company.com \
  --output-type csv \
  --output valid_contacts.csv

# Revisar errores
cat error_log.txt
# BR-001: invalid@email@com - Email must contain exactly one @
# BR-002: noname@domain.com - Email must contain exactly one dot before @
```

### Caso 3: Integración con API Externa

**Escenario:** Procesar correos desde webhook o servicio externo

```python
# webhook_handler.py
import requests

def process_webhook(data):
    API_URL = "http://localhost:5000"
    
    # Extraer correos del webhook
    emails = data.get('emails', [])
    
    # Transformar
    response = requests.post(f"{API_URL}/transform", json={
        "emails": emails,
        "new_domain": "company.com"
    })
    
    result = response.json()
    
    # Enviar a sistema destino
    send_to_crm(result['transformed'])
    
    return {"status": "ok", "processed": result['valid']}
```

### Caso 4: Procesamiento Batch Nocturno

**Escenario:** Procesar archivos diarios automáticamente

```bash
#!/bin/bash
# daily_processor.sh

DATE=$(date +%Y%m%d)
INPUT_DIR="/data/incoming"
OUTPUT_DIR="/data/processed"
ARCHIVE_DIR="/data/archive"

for file in $INPUT_DIR/*.txt; do
    filename=$(basename "$file" .txt)
    
    echo "Processing $filename..."
    
    python main_cli.py \
        --input-type file \
        --input "$file" \
        --new-domain company.com \
        --output-type csv \
        --output "$OUTPUT_DIR/${filename}_${DATE}.csv"
    
    # Archivar original
    mv "$file" "$ARCHIVE_DIR/${filename}_${DATE}.txt"
    
    # Enviar notificación
    echo "Processed $filename" | mail -s "Daily Email Processing" admin@company.com
done
```

**Cron:**
```cron
0 2 * * * /scripts/daily_processor.sh >> /var/log/email_processor.log 2>&1
```

### Caso 5: Microservicio en Docker

**Escenario:** Desplegar como contenedor

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "main_api.py"]
```

```bash
# Construir
docker build -t email-processor .

# Ejecutar
docker run -p 5000:5000 email-processor

# Probar
curl -X POST http://localhost:5000/transform \
  -H "Content-Type: application/json" \
  -d '{"emails":["user@old.com"],"new_domain":"new.com"}'
```

### Caso 6: Integración con n8n

**Escenario:** Automatización visual con n8n

```json
{
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300]
    },
    {
      "name": "Email Processor",
      "type": "n8n-nodes-base.httpRequest",
      "parameters": {
        "url": "http://localhost:5000/transform",
        "method": "POST",
        "jsonParameters": true,
        "options": {},
        "bodyParametersJson": "={{ JSON.stringify({emails: $json.emails, new_domain: 'company.com'}) }}"
      },
      "position": [450, 300]
    },
    {
      "name": "Save to Database",
      "type": "n8n-nodes-base.postgres",
      "position": [650, 300]
    }
  ]
}
```

---

## 📊 Comparación de Interfaces

| Característica | CLI | API Local | Lambda | Librería |
|----------------|-----|-----------|--------|----------|
| **Uso** | Terminal | HTTP | Cloud | Python |
| **Complejidad** | Baja | Media | Alta | Baja |
| **Escalabilidad** | Baja | Media | Alta | Media |
| **Costo** | Gratis | Gratis | Pay-per-use | Gratis |
| **Latencia** | Baja | Baja | Media | Muy baja |
| **Ideal para** | Scripts | Integraciones | Producción | Aplicaciones |

---

## 🎓 Ejemplos por Nivel

### Nivel 1: Principiante

```bash
# Procesar un solo correo
python main_cli.py \
  --input-type list \
  --input "juan.perez@old.com" \
  --new-domain company.com \
  --output-type inline
```

### Nivel 2: Intermedio

```python
# Procesar con validación personalizada
from src.features.email_processing.adapters.input.library_adapter import EmailProcessingLibrary

emails = ["juan.perez@old.com", "invalid@email", "ana.garcia@old.com"]

# Validar primero
valid_emails = [e for e in emails if EmailProcessingLibrary.validate(e)]
print(f"Valid: {len(valid_emails)}/{len(emails)}")

# Transformar solo válidos
transformed = EmailProcessingLibrary.transform(valid_emails, "company.com")

# Generar reporte
for item in transformed:
    if item['valid']:
        print(f"✓ {item['original']} → {item['transformed']}")
```

### Nivel 3: Avanzado

```python
# Pipeline con manejo de errores y reintentos
import requests
import time
from typing import List, Dict

class EmailProcessorClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["x-api-key"] = api_key
    
    def process_batch(self, emails: List[str], new_domain: str, 
                     batch_size: int = 100, max_retries: int = 3) -> Dict:
        results = {"success": [], "failed": []}
        
        # Procesar en lotes
        for i in range(0, len(emails), batch_size):
            batch = emails[i:i+batch_size]
            
            for attempt in range(max_retries):
                try:
                    response = requests.post(
                        f"{self.base_url}/transform",
                        headers=self.headers,
                        json={"emails": batch, "new_domain": new_domain},
                        timeout=30
                    )
                    response.raise_for_status()
                    
                    data = response.json()
                    results["success"].extend([
                        t for t in data["transformed"] if t["valid"]
                    ])
                    results["failed"].extend([
                        t for t in data["transformed"] if not t["valid"]
                    ])
                    break
                    
                except requests.exceptions.RequestException as e:
                    if attempt == max_retries - 1:
                        results["failed"].extend([
                            {"email": e, "error": str(e)} for e in batch
                        ])
                    else:
                        time.sleep(2 ** attempt)  # Exponential backoff
        
        return results

# Uso
client = EmailProcessorClient(
    base_url="https://api.company.com",
    api_key="prod-key-123"
)

emails = load_emails_from_database()  # 10,000 emails
results = client.process_batch(emails, "newcompany.com", batch_size=100)

print(f"Success: {len(results['success'])}")
print(f"Failed: {len(results['failed'])}")
```

---

## 🔍 Debugging Tips

### Ver logs detallados

```bash
# CLI con logs
python main_cli.py ... 2>&1 | tee execution.log

# API con logs
python main_api.py 2>&1 | tee api.log
```

### Probar validaciones

```python
from src.shared.validation_adapter import RegexEmailValidator

validator = RegexEmailValidator()

test_cases = [
    "juan.perez@example.com",      # ✓ Válido
    "invalid@email@com",            # ✗ BR-001: Múltiples @
    "noname@domain.com",            # ✗ BR-002: Sin punto antes de @
    "a.b@domain.com",               # ✗ BR-003: Nombre muy corto
    "juan123.perez@domain.com",     # ✗ BR-005: Números no permitidos
]

for email in test_cases:
    try:
        nombre, apellido = validator.validate_and_parse(email)
        print(f"✓ {email}: {nombre} {apellido}")
    except ValueError as e:
        print(f"✗ {email}: {e}")
```

### Medir performance

```python
import time

start = time.time()

# Procesar 1000 emails
emails = [f"user{i}.test{i}@old.com" for i in range(1000)]
transformed = EmailProcessingLibrary.transform(emails, "new.com")

duration = time.time() - start
print(f"Processed {len(emails)} emails in {duration:.2f}s")
print(f"Rate: {len(emails)/duration:.0f} emails/sec")
```

---

## 📝 Checklist de Producción

### Antes de Desplegar

- [ ] Probar con datos reales en ambiente de desarrollo
- [ ] Validar reglas de negocio (BR-001 a BR-005)
- [ ] Configurar logs y monitoreo
- [ ] Definir estrategia de respaldo
- [ ] Documentar procedimientos de rollback
- [ ] Configurar alertas de errores
- [ ] Realizar pruebas de carga
- [ ] Revisar políticas de seguridad

### Después de Desplegar

- [ ] Verificar endpoints funcionando
- [ ] Monitorear logs en tiempo real
- [ ] Validar métricas de performance
- [ ] Probar casos de error
- [ ] Documentar incidentes
- [ ] Actualizar documentación
- [ ] Capacitar usuarios
- [ ] Establecer SLA

---

## 🆘 Comandos de Emergencia

### Detener API Local

```bash
# Encontrar proceso
ps aux | grep main_api.py

# Matar proceso
kill -9 <PID>

# O usar Ctrl+C en terminal
```

### Rollback Lambda

```bash
cd terraform

# Ver versiones anteriores
terraform state list

# Volver a versión anterior
git checkout <commit-hash>
terraform apply
```

### Limpiar archivos temporales

```bash
# Windows
del /q *.csv *.json error_log.txt summary.txt *.log

# Linux/Mac
rm -f *.csv *.json error_log.txt summary.txt *.log
```

### Reiniciar desde cero

```bash
# Limpiar todo
cd terraform
terraform destroy

# Reconstruir
./build.sh
terraform apply
```

---

## 📚 Recursos Adicionales

- **Documentación completa:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Definición del proceso:** [docs/pdd/PDD.md](pdd/PDD.md)
- **Diseño técnico:** [docs/sdd/SDD.md](sdd/SDD.md)
- **Ejemplos de código:** [examples/](../examples/)
- **Scripts de utilidad:** [scripts/](../scripts/)

---

**¿Necesitas ayuda?** Revisa la sección [Troubleshooting](DEPLOYMENT_GUIDE.md#troubleshooting) en la guía completa.
