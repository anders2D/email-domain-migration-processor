#!/bin/bash
# Demo de validación de errores

echo "=== Email Processor CLI - Validación ==="
echo ""
sleep 1

echo "$ email-processor --input-type list --input \"valid@old.com,invalid,no@@at.com\" --new-domain new.com --output-type inline"
sleep 1
email-processor --input-type list --input "valid@old.com,invalid,no@@at.com" --new-domain new.com --output-type inline
sleep 2

echo ""
echo "$ cat error_log.txt"
sleep 1
cat error_log.txt
sleep 2
