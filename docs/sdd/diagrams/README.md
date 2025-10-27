# Diagramas SDD - Solution Design Document

Diagramas técnicos de la arquitectura de la solución.

## 📊 Diagramas Disponibles

| Diagrama | Descripción | Sección SDD | Estado |
|----------|-------------|-------------|--------|
| `arquitectura-alto-nivel.mmd` / `.svg` | Vista general del sistema con usuarios, interfaces y componentes | 3.1 | ✅ |
| `arquitectura-hexagonal.mmd` / `.svg` | Patrón Ports & Adapters con capas y dependencias | 3.2 | ✅ |
| `patron-etl.mmd` / `.svg` | Flujo Extract → Transform → Generate | 3.3 | ✅ |
| `arquitectura-aws.mmd` / `.svg` | Infraestructura AWS con Lambda, API Gateway y WAF | 7.1 | ✅ |

## 🛠️ Generar SVGs

### Requisitos

```bash
npm install -g @mermaid-js/mermaid-cli
```

### Linux/Mac

```bash
sh convert.sh
```

### Windows

```cmd
convert.bat
```

## 📝 Formato

- **Fuente:** `.mmd` (Mermaid)
- **Salida:** `.svg` (Scalable Vector Graphics)
- **Tema:** Neutral con fondo transparente
