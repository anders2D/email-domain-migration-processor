#!/bin/bash
# CLI Usage Examples - Linux/Mac
# All 12 combinations: 3 input types × 4 output types
#
# OPCION 1 (Recomendado): Instalar desde PyPI
#   pip install email-processor-cli
#   Luego usa: email-processor [opciones]
#
# OPCION 2: Usar código fuente
#   python main_cli.py [opciones]

echo "=== CLI EXAMPLES - ALL COMBINATIONS ==="
echo
echo "Opcion 1 (Recomendado): email-processor (requiere: pip install email-processor-cli)"
echo "Opcion 2: python main_cli.py (codigo fuente)"
echo
echo "Estos ejemplos usan la Opcion 1 (PyPI)"
echo

echo "=== FILE INPUT (3 input types × 4 output types) ==="
echo

echo "1. File to CSV"
email-processor --input-type file --input examples/file_examples/sample_emails.txt --new-domain company.com --output-type csv --output output_file_csv.csv
echo

echo "2. File to JSON"
email-processor --input-type file --input examples/file_examples/sample_emails.txt --new-domain company.com --output-type json --output output_file_json.json
echo

echo "3. File to Inline"
email-processor --input-type file --input examples/file_examples/sample_emails.txt --new-domain company.com --output-type inline
echo

echo "4. File to Silent"
email-processor --input-type file --input examples/file_examples/sample_emails.txt --new-domain company.com --output-type silent
echo

echo "=== LIST INPUT ==="
echo

echo "5. List to CSV"
email-processor --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type csv --output output_list_csv.csv
echo

echo "6. List to JSON"
email-processor --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type json --output output_list_json.json
echo

echo "7. List to Inline"
email-processor --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type inline
echo

echo "8. List to Silent"
email-processor --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type silent
echo

echo "=== TEXT INPUT ==="
echo

echo "9. Text to CSV"
email-processor --input-type text --input "user@old.com
admin@old.com" --new-domain company.com --output-type csv --output output_text_csv.csv
echo

echo "10. Text to JSON"
email-processor --input-type text --input "user@old.com
admin@old.com" --new-domain company.com --output-type json --output output_text_json.json
echo

echo "11. Text to Inline"
email-processor --input-type text --input "user@old.com
admin@old.com" --new-domain company.com --output-type inline
echo

echo "12. Text to Silent"
email-processor --input-type text --input "user@old.com
admin@old.com" --new-domain company.com --output-type silent
echo

echo "=== HELP ==="
echo

echo "13. Show usage"
email-processor --help
