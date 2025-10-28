#!/bin/bash
# Demo de salida CSV

echo "=== Email Processor CLI - Salida CSV ==="
echo ""
sleep 1

echo "$ email-processor --input-type list --input \"maria.garcia@example.com,pedro.lopez@example.com\" --new-domain company.com --output-type csv --output demo_output.csv"
sleep 1
email-processor --input-type list --input "maria.garcia@example.com,pedro.lopez@example.com" --new-domain company.com --output-type csv --output demo_output.csv
sleep 2

echo ""
echo "$ cat demo_output.csv"
sleep 1
cat demo_output.csv
sleep 2
