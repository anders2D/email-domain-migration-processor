#!/bin/bash
# Demo básico del CLI

echo "=== Email Processor CLI - Demo Básico ==="
echo ""
sleep 1

echo "$ email-processor --help"
sleep 1
email-processor --help
sleep 2

echo ""
echo "$ email-processor --input-type list --input \"john.doe@old.com,jane.smith@old.com\" --new-domain new.com --output-type inline"
sleep 1
email-processor --input-type list --input "john.doe@old.com,jane.smith@old.com" --new-domain new.com --output-type inline
sleep 2
