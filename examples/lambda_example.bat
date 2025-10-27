@echo off
REM AWS Lambda API Gateway Examples (Windows)

cd ..\terraform
for /f "delims=" %%i in ('terraform output -raw extract_url') do set EXTRACT_URL=%%i
for /f "delims=" %%i in ('terraform output -raw transform_url') do set TRANSFORM_URL=%%i
for /f "delims=" %%i in ('terraform output -raw generate_url') do set GENERATE_URL=%%i
for /f "delims=" %%i in ('terraform output -raw api_key') do set API_KEY=%%i
cd ..\examples

echo === LAMBDA API GATEWAY EXAMPLES ===
echo API Key: %API_KEY%
echo.

echo 1. Extract from list
curl -X POST %EXTRACT_URL% -H "Content-Type: application/json" -H "x-api-key: %API_KEY%" -d "{\"input_type\":\"list\",\"input\":[\"user@old.com\",\"admin@old.com\"]}"
echo.
echo.

echo 2. Transform emails
curl -X POST %TRANSFORM_URL% -H "Content-Type: application/json" -H "x-api-key: %API_KEY%" -d "{\"emails\":[\"juan.perez@old.com\",\"ana.garcia@old.com\"],\"new_domain\":\"company.com\"}"
echo.
echo.

echo 3. Generate inline
curl -X POST %GENERATE_URL% -H "Content-Type: application/json" -H "x-api-key: %API_KEY%" -d "{\"transformed\":[{\"transformed\":\"user@new.com\",\"valid\":true}],\"output_type\":\"inline\"}"
echo.
