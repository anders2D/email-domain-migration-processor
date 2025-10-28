#!/bin/bash
# Script wrapper para ejecutar publish_with_timestamp.py en Linux/Mac

cd "$(dirname "$0")/.."
python scripts/publish_with_timestamp.py
