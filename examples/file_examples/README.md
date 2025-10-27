# File Examples

Archivos de entrada de ejemplo para probar el procesador de correos electrónicos.

## 📁 Archivos Disponibles

### ✅ Casos Válidos

| Archivo | Descripción | Reglas Probadas |
|---------|-------------|-----------------|
| `valid_emails.txt` | Correos completamente válidos | BR-001 a BR-005 ✓ |
| `mixed_case.txt` | Correos válidos con diferentes capitalizaciones | TR-001, TR-002, TR-003 |
| `accented_names.txt` | Nombres con acentos (válidos) | BR-005 (letras acentuadas) |
| `sample_emails.txt` | Dataset completo de 60 correos válidos | Todas las reglas ✓ |

### ❌ Casos Inválidos

| Archivo | Descripción | Regla Violada |
|---------|-------------|---------------|
| `invalid_multiple_at.txt` | Múltiples símbolos @ | BR-001 ✗ |
| `invalid_dots.txt` | Sin punto o múltiples puntos en prefijo | BR-002 ✗ |
| `invalid_length.txt` | Nombres muy cortos (<2) o muy largos (>50) | BR-003, BR-004 ✗ |
| `invalid_characters.txt` | Números, guiones, símbolos especiales | BR-005 ✗ |

### 🔀 Casos Mixtos

| Archivo | Descripción | Propósito |
|---------|-------------|-----------|
| `mixed_valid_invalid.txt` | 50% válidos, 50% inválidos | Probar filtrado y logging |
| `empty_lines.txt` | Correos válidos con líneas vacías | Probar manejo de espacios |

## 🧪 Reglas de Validación (BR)

| ID | Regla | Condición |
|----|-------|-----------|
| BR-001 | Exactamente un @ | `email.count('@') == 1` |
| BR-002 | Exactamente un punto en prefijo | `prefix.count('.') == 1` |
| BR-003 | Nombre 2-50 caracteres | `2 ≤ len(nombre) ≤ 50` |
| BR-004 | Apellido 2-50 caracteres | `2 ≤ len(apellido) ≤ 50` |
| BR-005 | Solo letras (a-z, A-Z, acentuadas) | `nombre.isalpha()` |

## 🔄 Reglas de Transformación (TR)

| ID | Regla | Ejemplo |
|----|-------|---------|
| TR-001 | Capitalizar nombre | juan → Juan |
| TR-002 | Capitalizar apellido | perez → Perez |
| TR-003 | Minúsculas en email | Juan.Perez@NEW.COM → juan.perez@new.com |
| TR-004 | Preservar dominio original | @example.com |
| TR-005 | Aplicar nuevo dominio | @new.com |

## 💡 Uso

```bash
# Procesar archivo válido
python main_cli.py --input-type file --input examples/file_examples/valid_emails.txt --new-domain new.com --output-type inline

# Procesar archivo con errores
python main_cli.py --input-type file --input examples/file_examples/mixed_valid_invalid.txt --new-domain company.com --output-type csv

# Procesar archivo con acentos
python main_cli.py --input-type file --input examples/file_examples/accented_names.txt --new-domain nuevo.com --output-type inline
```

## 📊 Resultados Esperados

| Archivo | Total | Válidos | Inválidos | Tasa Éxito |
|---------|-------|---------|-----------|------------|
| `valid_emails.txt` | 5 | 5 | 0 | 100% |
| `invalid_multiple_at.txt` | 5 | 0 | 5 | 0% |
| `invalid_dots.txt` | 5 | 0 | 5 | 0% |
| `invalid_length.txt` | 5 | 0 | 5 | 0% |
| `invalid_characters.txt` | 6 | 1 | 5 | 17% |
| `mixed_valid_invalid.txt` | 10 | 5 | 5 | 50% |
| `sample_emails.txt` | 60 | 60 | 0 | 100% |
