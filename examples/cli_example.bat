@echo off
REM CLI Usage Examples - Windows
REM All 12 combinations: 3 input types × 4 output types

echo === CLI EXAMPLES - ALL COMBINATIONS ===
echo.

echo === FILE INPUT (3 input types × 4 output types) ===
echo.

echo 1. File to CSV
python ..\main_cli.py --input-type file --input file_examples\sample_emails.txt --new-domain company.com --output-type csv --output output_file_csv.csv
echo.

echo 2. File to JSON
python ..\main_cli.py --input-type file --input file_examples\sample_emails.txt --new-domain company.com --output-type json --output output_file_json.json
echo.

echo 3. File to Inline
python ..\main_cli.py --input-type file --input file_examples\sample_emails.txt --new-domain company.com --output-type inline
echo.

echo 4. File to Silent
python ..\main_cli.py --input-type file --input file_examples\sample_emails.txt --new-domain company.com --output-type silent
echo.

echo === LIST INPUT ===
echo.

echo 5. List to CSV
python ..\main_cli.py --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type csv --output output_list_csv.csv
echo.

echo 6. List to JSON
python ..\main_cli.py --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type json --output output_list_json.json
echo.

echo 7. List to Inline
python ..\main_cli.py --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type inline
echo.

echo 8. List to Silent
python ..\main_cli.py --input-type list --input "juan.perez@old.com,ana.garcia@old.com" --new-domain company.com --output-type silent
echo.

echo === TEXT INPUT ===
echo.

echo 9. Text to CSV
python ..\main_cli.py --input-type text --input "user@old.com\nadmin@old.com" --new-domain company.com --output-type csv --output output_text_csv.csv
echo.

echo 10. Text to JSON
python ..\main_cli.py --input-type text --input "user@old.com\nadmin@old.com" --new-domain company.com --output-type json --output output_text_json.json
echo.

echo 11. Text to Inline
python ..\main_cli.py --input-type text --input "user@old.com\nadmin@old.com" --new-domain company.com --output-type inline
echo.

echo 12. Text to Silent
python ..\main_cli.py --input-type text --input "user@old.com\nadmin@old.com" --new-domain company.com --output-type silent
echo.

echo === HELP ===
echo.

echo 13. Show usage
python ..\main_cli.py --help
