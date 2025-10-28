"""CLI Entry Point for email-processor command"""
import sys
import argparse
from src.features.email_processing.adapters.input.cli_adapter import EmailProcessingCLI


def main():
    parser = argparse.ArgumentParser(description='Email Processor - Hexagonal Architecture')
    parser.add_argument('--input-type', choices=['file', 'list', 'text'], default='file', help='Input type')
    parser.add_argument('--input', required=True, help='Input data')
    parser.add_argument('--new-domain', required=True, help='New domain for emails')
    parser.add_argument('--output-type', choices=['csv', 'json', 'excel', 'txt', 'inline', 'silent'], default='csv', help='Output type')
    parser.add_argument('--output', help='Output file (required for csv/json)')
    
    args = parser.parse_args()
    
    if args.output_type in ['csv', 'json', 'excel', 'txt'] and not args.output:
        parser.error(f"--output required for {args.output_type}")
    
    config = {
        'input_type': args.input_type,
        'input': args.input,
        'new_domain': args.new_domain,
        'output_type': args.output_type,
        'output_file': args.output
    }
    
    cli = EmailProcessingCLI()
    try:
        cli.run(config)
    except FileNotFoundError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
