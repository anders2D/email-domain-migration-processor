# Terraform - AWS Lambda + API Gateway

## 📦 Despliegue

### 1. Construir el paquete Lambda

**Windows:**
```bash
cd terraform
build.bat
```

**Linux/Mac:**
```bash
cd terraform
chmod +x build.sh
./build.sh
```

### 2. Configurar AWS Credentials

```bash
aws configure
```

### 3. Desplegar con Terraform

```bash
terraform init
terraform plan
terraform apply
terraform output
```

### 4. Personalizar (opcional)

Editar valores directamente en `main.tf`:
- `region`: línea 7
- `function_name`: línea 14
- `NEW_DOMAIN`: línea 21

## 🧪 Probar el API

```bash
API_URL=$(terraform output -raw api_url)

curl -X POST $API_URL \
  -H "Content-Type: application/json" \
  -d '{"emails": ["juan@example.com"], "new_domain": "company.com"}'
```

## 🗑️ Destruir infraestructura

```bash
terraform destroy
```
