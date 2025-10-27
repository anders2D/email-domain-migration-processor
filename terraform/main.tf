terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "aws_profile" {
  description = "AWS Profile to use"
  type        = string
  default     = "kubernates"
}

variable "aws_region" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

# Lambda Function
resource "aws_lambda_function" "email_processor" {
  filename         = "lambda_function.zip"
  function_name    = "email-processor"
  role            = aws_iam_role.lambda_role.arn
  handler         = "lambda_handler.handler"
  source_code_hash = filebase64sha256("lambda_function.zip")
  runtime         = "python3.11"
  timeout         = 30
  memory_size     = 512

  environment {
    variables = {
      NEW_DOMAIN = "company.com"
      API_KEY    = "prod-email-processor-2024-secure-key"
    }
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "email-processor-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.lambda_role.name
}

# API Gateway
resource "aws_apigatewayv2_api" "email_api" {
  name          = "email-processor-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["POST"]
    allow_headers = ["content-type", "x-api-key"]
    max_age       = 300
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.email_api.id
  name        = "$default"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })
  }

  default_route_settings {
    throttling_burst_limit = 100
    throttling_rate_limit  = 50
  }
}

resource "aws_apigatewayv2_integration" "lambda" {
  api_id           = aws_apigatewayv2_api.email_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.email_processor.invoke_arn
}

resource "aws_apigatewayv2_route" "extract" {
  api_id    = aws_apigatewayv2_api.email_api.id
  route_key = "POST /extract"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "transform" {
  api_id    = aws_apigatewayv2_api.email_api.id
  route_key = "POST /transform"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_apigatewayv2_route" "generate" {
  api_id    = aws_apigatewayv2_api.email_api.id
  route_key = "POST /generate"
  target    = "integrations/${aws_apigatewayv2_integration.lambda.id}"
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.email_processor.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.email_api.execution_arn}/*/*"
}

# CloudWatch Logs for API Gateway
resource "aws_cloudwatch_log_group" "api_logs" {
  name              = "/aws/apigateway/email-processor"
  retention_in_days = 7
}

# CloudWatch Logs for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/email-processor"
  retention_in_days = 7
}


