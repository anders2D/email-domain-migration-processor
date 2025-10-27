# Scripts de Utilidad

## clean.bat / clean.sh

Script de limpieza de archivos temporales y basura del proyecto.

### Uso

**Windows:**
```bash
scripts\clean.bat
```

**Linux/Mac:**
```bash
sh scripts/clean.sh
```

### Archivos que elimina

1. **Outputs temporales:** correos_procesados.csv, error_log.txt, summary.txt, test_error_log.txt, test_output.csv, *.log
2. **Artefactos Terraform:** lambda_function.zip (preserva terraform.tfstate para mantener el tracking de recursos)
3. **Cache Python:** __pycache__/, *.pyc
