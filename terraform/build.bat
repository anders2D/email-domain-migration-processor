@echo off
echo Building Lambda deployment package...

if exist lambda_package rmdir /s /q lambda_package
if exist lambda_function.zip del lambda_function.zip

mkdir lambda_package
xcopy /E /I /Y ..\src lambda_package\src
copy /Y lambda_handler.py lambda_package\

cd lambda_package
powershell Compress-Archive -Path * -DestinationPath ..\lambda_function.zip -Force
cd ..

rmdir /s /q lambda_package

echo Lambda package created: lambda_function.zip
