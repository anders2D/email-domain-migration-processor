# Procesador de Correos - Arquitectura Hexagonal

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/email-processor-cli.svg)](https://pypi.org/project/email-processor-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AWS Lambda](https://img.shields.io/badge/AWS-Lambda-orange.svg)](https://aws.amazon.com/lambda/)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-purple.svg)](https://www.terraform.io/)

> Sistema de migración de dominios de correo electrónico con arquitectura hexagonal, multi-interfaz (CLI, API, Librería) y despliegue en AWS Lambda.

## 📑 Tabla de Contenidos

- [Características](#-características)
- [Instalación](#-instalación)
- [Inicio Rápido](#-inicio-rápido)
- [Documentación](#-documentación)
- [Ejemplos](#-ejemplos)

## ✨ Características

- ✅ **Arquitectura Hexagonal** - Núcleo de negocio aislado de infraestructura
- ✅ **Multi-interfaz** - CLI, API REST (local + Lambda), Librería Python
- ✅ **Sin Estado** - Stateless, escalable horizontalmente
- ✅ **Validación Robusta** - 5 reglas de negocio (BR-001 a BR-005)
- ✅ **Transformación Inteligente** - 5 reglas de transformación (TR-001 a TR-005)
- ✅ **E/S Flexible** - Múltiples formatos de entrada/salida (CSV, JSON, inline)
- ✅ **Seguridad** - Autenticación con API Key en Lambda
- ✅ **IaC** - Infraestructura como código con Terraform
- ✅ **Logging** - CloudWatch logs con retención configurable
- ✅ **Documentación Completa** - PDD, diagramas Mermaid, guías de uso

## 🎯 Formato de Correo

Formato requerido: `nombre.apellido@dominio.com`

✅ Válido: `juan.perez@company.com`  
❌ Inválido: `user@company.com` (falta punto), `j.p@company.com` (muy corto)

Ver reglas completas en [PDD](docs/pdd/PDD.md#31-validación)

## 📦 Instalación

```bash
pip install email-processor-cli
```

Ver [Guía de Instalación](docs/QUICK_START.md) para más opciones.

## 🚀 Inicio Rápido

```bash
email-processor --input-type list --input "juan.perez@old.com" --new-domain new.com --output-type inline
```

Ver [Guía Rápida](docs/QUICK_START.md) para más casos de uso.

## 📚 Ejemplos

Ver [examples/](examples/) para código completo de CLI, API, Librería y n8n.

## 📖 Documentación

| Documento | Descripción |
|-----------|-------------|
| **[Inicio Rápido](docs/QUICK_START.md)** | Comienza en 5 minutos |
| **[Guía de Despliegue](docs/DEPLOYMENT_GUIDE.md)** | CLI, API, Lambda completo |
| **[Cheatsheet](docs/CHEATSHEET.md)** | Referencia rápida de comandos |
| **[PDD](docs/pdd/PDD.md)** | Proceso de negocio y reglas |
| **[Integración n8n](docs/N8N_INTEGRATION.md)** | Automatización con n8n |

## 👤 Autor

**Anderson Taguada**

- GitHub: [@anders2d](https://github.com/anders2d)
- Email: ferchoafta@gmail.com