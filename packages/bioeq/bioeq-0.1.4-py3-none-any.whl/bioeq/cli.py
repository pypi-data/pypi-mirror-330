"""
Command Line Interface (CLI) for the BioEq package.

This module provides a command-line interface for the BioEq package,
allowing users to perform common tasks from the command line.
"""

import argparse
import sys
import importlib.metadata
from pathlib import Path
import json

from .validation import run_validation


def get_version() -> str:
    """Get the package version."""
    try:
        return importlib.metadata.version("bioeq")
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def validate_command(args):
    """Run validation and output results based on command arguments."""
    print(f"Running BioEq validation suite (v{get_version()})...")
    print("-" * 50)
    
    report = run_validation(get_version())
    
    if args.output:
        # Save report to the specified file
        try:
            with open(args.output, 'w') as f:
                json.dump({
                    "report_name": report.report_name,
                    "version": report.version,
                    "timestamp": report.timestamp,
                    "summary": report.summary,
                    "validation_results": report.validation_results
                }, f, indent=2)
            print(f"Validation report saved to: {args.output}")
        except Exception as e:
            print(f"Error saving report to {args.output}: {str(e)}")
    
    # Return exit code based on validation results
    return 0 if report.summary["failed_tests"] == 0 else 1


def main():
    """Main entry point for the BioEq CLI."""
    parser = argparse.ArgumentParser(
        description="BioEq - Bioequivalence analysis tools"
    )
    
    # Add version argument
    parser.add_argument(
        '--version', '-v', 
        action='version', 
        version=f'BioEq v{get_version()}'
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(
        title='commands',
        description='valid commands',
        help='additional help',
        dest='command'
    )
    
    # Create parser for 'validate' command
    validate_parser = subparsers.add_parser(
        'validate', 
        help='Run validation tests'
    )
    validate_parser.add_argument(
        '--output', '-o',
        help='Output file for validation report (JSON format)',
        type=str
    )
    validate_parser.set_defaults(func=validate_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    # If no commands are provided, print help and exit
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute the function associated with the command
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main()) 