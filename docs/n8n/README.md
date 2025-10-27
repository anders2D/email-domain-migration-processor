# n8n Workflow Assets

## 📁 Contents

- **n8n_flow.png** - Visual diagram of the complete workflow
- **../N8N_INTEGRATION.md** - Complete integration guide

## 🔄 Workflow Overview

The n8n workflow orchestrates the Email Processor API through 5 sequential nodes:

1. **Start** - Manual trigger
2. **Input Data** - Define emails and target domain
3. **Extract** - Call `/extract` endpoint
4. **Transform** - Call `/transform` endpoint
5. **Generate CSV** - Call `/generate` endpoint
6. **Prepare Download** - Convert to binary CSV file

## 📥 Import Workflow

The workflow JSON is located at: `examples/n8n_workflow.json`

**Steps:**
1. Open n8n
2. Go to **Workflows** → **Import from File**
3. Select `examples/n8n_workflow.json`
4. Update API key in all HTTP Request nodes
5. Execute workflow

## 🔗 Quick Links

- **Full Documentation:** [N8N_INTEGRATION.md](../N8N_INTEGRATION.md)
- **Workflow JSON:** [n8n_workflow.json](../../examples/n8n_workflow.json)
- **API Documentation:** [API_LAMBDA.md](../API_LAMBDA.md)

## 🎯 Use Cases

- Scheduled batch email processing
- File upload → process → download workflows
- Integration with SharePoint, S3, email services
- Multi-domain parallel processing
- Approval workflows with human-in-the-loop

## 📊 Visual Flow

![n8n Workflow](n8n_flow.png)

The diagram shows the complete data flow from input to CSV output, including API calls and data transformations.
