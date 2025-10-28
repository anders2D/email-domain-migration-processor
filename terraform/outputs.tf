output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.email_api.api_endpoint
}

output "api_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.email_api.id
}

output "lambda_function_name" {
  description = "Lambda function name"
  value       = aws_lambda_function.email_processor.function_name
}

output "lambda_function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.email_processor.arn
}

output "lambda_role_arn" {
  description = "Lambda IAM role ARN"
  value       = aws_iam_role.lambda_role.arn
}

output "extract_url" {
  description = "Extract endpoint URL"
  value       = "${aws_apigatewayv2_api.email_api.api_endpoint}/extract"
}

output "transform_url" {
  description = "Transform endpoint URL"
  value       = "${aws_apigatewayv2_api.email_api.api_endpoint}/transform"
}

output "generate_url" {
  description = "Generate endpoint URL"
  value       = "${aws_apigatewayv2_api.email_api.api_endpoint}/generate"
}

output "region" {
  description = "AWS Region"
  value       = var.aws_region
}

output "aws_profile" {
  description = "AWS Profile used"
  value       = var.aws_profile
}

output "api_key" {
  description = "API Key for authentication (use in x-api-key header)"
  value       = "prod-email-processor-2024-secure-key"
  sensitive   = true
}

output "waf_web_acl_id" {
  description = "WAF Web ACL ID"
  value       = aws_wafv2_web_acl.email_api_waf.id
}

output "waf_web_acl_arn" {
  description = "WAF Web ACL ARN"
  value       = aws_wafv2_web_acl.email_api_waf.arn
}


