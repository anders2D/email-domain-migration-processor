#!/bin/bash
# AWS Lambda API Gateway Examples

# Get endpoints from Terraform
EXTRACT_URL=$(cd ../terraform && terraform output -raw extract_url)
TRANSFORM_URL=$(cd ../terraform && terraform output -raw transform_url)
GENERATE_URL=$(cd ../terraform && terraform output -raw generate_url)
API_KEY=$(cd ../terraform && terraform output -raw api_key)

echo "=== LAMBDA API GATEWAY EXAMPLES ==="
echo "API Key: $API_KEY"
echo

echo "1. Extract from list"
curl -X POST $EXTRACT_URL \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"input_type":"list","input":["user@old.com","admin@old.com"]}'
echo -e "\n"

echo "2. Transform emails"
curl -X POST $TRANSFORM_URL \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"emails":["juan.perez@old.com","ana.garcia@old.com"],"new_domain":"company.com"}'
echo -e "\n"

echo "3. Generate inline"
curl -X POST $GENERATE_URL \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"transformed":[{"transformed":"user@new.com","valid":true}],"output_type":"inline"}'
echo -e "\n"

echo "4. Full pipeline"
EMAILS=$(curl -s -X POST $EXTRACT_URL \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d '{"input_type":"list","input":["user@old.com"]}' | jq -r '.emails')

TRANSFORMED=$(curl -s -X POST $TRANSFORM_URL \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"emails\":$EMAILS,\"new_domain\":\"new.com\"}" | jq -r '.transformed')

curl -X POST $GENERATE_URL \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -d "{\"transformed\":$TRANSFORMED,\"output_type\":\"inline\"}"
echo
