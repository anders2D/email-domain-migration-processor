# n8n Integration Guide

## 🎯 Overview

This guide explains how to integrate the Email Processor with n8n, a workflow automation platform. The integration allows you to orchestrate the email transformation process visually and connect it with other services.

## 🏗️ Architecture

The n8n workflow calls the Email Processor API (AWS Lambda) in three sequential steps:

```
Input Data → Extract → Transform → Generate → Output CSV
```

Each step corresponds to an API endpoint that follows the hexagonal architecture pattern.

## 📋 Prerequisites

- n8n instance (cloud or self-hosted)
- Email Processor API deployed on AWS Lambda
- API Key for authentication

## 🚀 Quick Start

### 1. Import Workflow

Import the pre-configured workflow from `examples/n8n_workflow.json`:

1. Open n8n
2. Click **Workflows** → **Import from File**
3. Select `examples/n8n_workflow.json`
4. Click **Import**

### 2. Configure API Credentials

Update the API Key in all HTTP Request nodes:

1. Open each node: **1. Extract**, **2. Transform**, **3. Generate CSV**
2. Navigate to **Headers** section
3. Update `x-api-key` value with your API key
4. Update API URL if using a different endpoint

**Get your API Key:**
```bash
cd terraform
terraform output api_key
```

### 3. Test Workflow

1. Click **Execute Workflow** button
2. Check execution results in each node
3. Download the generated CSV from the last node

## 🔧 Workflow Configuration

### Node 1: Input Data

**Type:** Set Node  
**Purpose:** Define input emails and target domain

**Configuration:**
```json
{
  "emails": "[\"user1@old.com\",\"user2@old.com\"]",
  "new_domain": "company.com"
}
```

**Customization:**
- Modify `emails` array with your email list
- Change `new_domain` to your target domain

### Node 2: Extract

**Type:** HTTP Request  
**Method:** POST  
**Endpoint:** `/extract`

**Headers:**
```
x-api-key: prod-email-processor-2024-secure-key
Content-Type: application/json
```

**Body:**
```json
{
  "input": ["user1@old.com", "user2@old.com"],
  "input_type": "list"
}
```

**Response:**
```json
{
  "emails": ["user1@old.com", "user2@old.com"],
  "count": 2,
  "source": "list"
}
```

### Node 3: Transform

**Type:** HTTP Request  
**Method:** POST  
**Endpoint:** `/transform`

**Headers:**
```
x-api-key: prod-email-processor-2024-secure-key
Content-Type: application/json
```

**Body:**
```json
{
  "emails": ["user1@old.com", "user2@old.com"],
  "new_domain": "company.com"
}
```

**Response:**
```json
{
  "transformed": [
    {
      "nombre": "User1",
      "apellido": "Old",
      "correo_original": "user1@old.com",
      "correo_nuevo": "user1.old@company.com"
    }
  ],
  "count": 1,
  "errors": []
}
```

### Node 4: Generate CSV

**Type:** HTTP Request  
**Method:** POST  
**Endpoint:** `/generate`

**Headers:**
```
x-api-key: prod-email-processor-2024-secure-key
Content-Type: application/json
```

**Body:**
```json
{
  "transformed": [...],
  "output_type": "csv"
}
```

**Response:**
```json
{
  "output": "Nombre,Apellido,Correo Ejemplo,Correo Nuevo\nUser1,Old,user1@old.com,user1.old@company.com",
  "count": 1,
  "format": "csv"
}
```

### Node 5: Prepare CSV Download

**Type:** Code Node  
**Purpose:** Convert CSV string to downloadable binary file

**Code:**
```javascript
const item = $input.first().json;
const csvContent = item.output || '';
const fileName = 'emails_transformed_' + new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5) + '.csv';

return [{
  json: {
    fileName: fileName,
    csvContent: csvContent,
    count: item.count || 0,
    format: item.format || 'csv'
  },
  binary: {
    data: {
      data: Buffer.from(csvContent, 'utf-8').toString('base64'),
      mimeType: 'text/csv',
      fileName: fileName
    }
  }
}];
```

## 🔄 Advanced Workflows

### Scheduled Email Processing

Add a **Cron** trigger to process emails automatically:

```
Cron Trigger → Read File → Extract → Transform → Generate → Send Email
```

**Cron Configuration:**
- **Mode:** Every Day
- **Hour:** 9:00 AM
- **Timezone:** Your timezone

### Email Notification

Add an **Email** node after CSV generation:

```
Generate CSV → Prepare CSV → Send Email (with attachment)
```

**Email Configuration:**
- **To:** recipient@company.com
- **Subject:** Email Processing Results
- **Attachments:** Use binary data from previous node

### Error Handling

Add **IF** node to handle errors:

```
Transform → IF (check errors) → Send Alert Email
                              → Continue to Generate
```

**IF Condition:**
```javascript
{{ $json.errors.length > 0 }}
```

### Multi-Domain Processing

Process emails for multiple domains in parallel:

```
Input → Split In Batches → Transform (domain1)
                         → Transform (domain2)
                         → Transform (domain3)
      → Merge → Generate CSV
```

## 📊 Monitoring

### Execution Logs

View execution details in n8n:

1. Go to **Executions** tab
2. Click on any execution
3. Review each node's input/output
4. Check error messages if any

### CloudWatch Integration

Monitor Lambda invocations from n8n:

- **Log Group:** `/aws/lambda/email-processor`
- **Metrics:** Invocations, Errors, Duration
- **Retention:** 7 days

## 🔐 Security Best Practices

### API Key Management

**Don't hardcode API keys in workflows:**

1. Use n8n **Credentials** feature
2. Create a new credential type: **Header Auth**
3. Set header name: `x-api-key`
4. Set header value: Your API key
5. Reference credential in HTTP Request nodes

### Environment Variables

Store sensitive data in n8n environment variables:

```bash
# .env file (self-hosted n8n)
EMAIL_PROCESSOR_API_KEY=your-api-key
EMAIL_PROCESSOR_API_URL=https://your-api.execute-api.us-east-1.amazonaws.com
```

**Access in workflow:**
```javascript
{{ $env.EMAIL_PROCESSOR_API_KEY }}
```

### Network Security

- Use HTTPS endpoints only
- Enable API Gateway throttling
- Implement IP whitelisting if needed
- Use VPC endpoints for private APIs

## 🐛 Troubleshooting

### Error: 401 Unauthorized

**Cause:** Invalid or missing API key

**Solution:**
1. Verify API key in HTTP Request headers
2. Check API key in AWS API Gateway
3. Ensure header name is exactly `x-api-key`

### Error: 500 Internal Server Error

**Cause:** Lambda execution error

**Solution:**
1. Check CloudWatch logs: `/aws/lambda/email-processor`
2. Verify request body format
3. Test endpoint with curl or Postman

### Error: Timeout

**Cause:** Lambda cold start or large dataset

**Solution:**
1. Increase n8n HTTP Request timeout (default: 300s)
2. Process emails in smaller batches
3. Increase Lambda timeout in Terraform

### Empty CSV Output

**Cause:** All emails failed validation

**Solution:**
1. Check `errors` array in Transform response
2. Review validation rules (BR-001 to BR-005)
3. Fix email format in input data

## 📚 Examples

### Example 1: Basic Processing

**Input:**
```json
{
  "emails": ["john.doe@old.com", "jane.smith@old.com"],
  "new_domain": "new.com"
}
```

**Output CSV:**
```csv
Nombre,Apellido,Correo Ejemplo,Correo Nuevo
John,Doe,john.doe@old.com,john.doe@new.com
Jane,Smith,jane.smith@old.com,jane.smith@new.com
```

### Example 2: With Validation Errors

**Input:**
```json
{
  "emails": ["valid@old.com", "invalid", "no@at@sign.com"],
  "new_domain": "new.com"
}
```

**Transform Response:**
```json
{
  "transformed": [
    {
      "nombre": "Valid",
      "apellido": "Old",
      "correo_original": "valid@old.com",
      "correo_nuevo": "valid.old@new.com"
    }
  ],
  "count": 1,
  "errors": [
    "Email 'invalid' no contiene exactamente un '@'",
    "Email 'no@at@sign.com' no contiene exactamente un '@'"
  ]
}
```

### Example 3: Batch Processing

Process 1000+ emails in batches of 100:

```
Read File → Split In Batches (100) → Extract → Transform → Generate → Merge Results
```

## 🔗 Integration Patterns

### Pattern 1: File Upload → Process → Download

```
Webhook (file upload) → Extract → Transform → Generate → Return CSV
```

### Pattern 2: Scheduled Batch Processing

```
Cron → Read SharePoint → Extract → Transform → Generate → Upload to S3
```

### Pattern 3: Event-Driven Processing

```
SQS Trigger → Extract → Transform → Generate → Send SNS Notification
```

### Pattern 4: Multi-Step Approval

```
Extract → Transform → Send Approval Email → Wait for Approval → Generate → Deliver
```

## 📖 Additional Resources

- **n8n Documentation:** https://docs.n8n.io
- **Workflow Template:** `examples/n8n_workflow.json`
- **Visual Flow:** `docs/n8n/n8n_flow.png`
- **API Documentation:** `docs/API_LAMBDA.md`
- **Deployment Guide:** `docs/DEPLOYMENT_GUIDE.md`

## 🆘 Support

For issues or questions:

1. Check CloudWatch logs for Lambda errors
2. Review n8n execution logs
3. Test API endpoints independently with curl
4. Verify API key and endpoint URLs
5. Check validation rules in README.md
