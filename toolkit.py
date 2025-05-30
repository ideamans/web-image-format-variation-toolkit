#!/usr/bin/env python3
"""
Image Processing Toolkit

A comprehensive toolkit for generating JPEG and PNG test images with various format variations
and comparing image quality across different processing pipelines.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.image_generator import generate_original_images, test_original_compliance
from src.variation_generator import generate_variations, test_variation_compliance
from src.image_comparator import compare_directories
from src.variation_validator import validate_all_variations, save_validation_report


def main():
    """Main entry point for the toolkit."""
    parser = argparse.ArgumentParser(
        description="Image Processing Toolkit for JPEG/PNG format testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python toolkit.py generate-original --test-compliance
  python toolkit.py generate-variations --source-dir originals --output-dir variations
  python toolkit.py compare-directories dir_a dir_b --output-format json
  python toolkit.py validate-variations --report-file validation_report.json
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate original images command
    orig_parser = subparsers.add_parser(
        'generate-original',
        help='Generate ideal JPEG and PNG source images'
    )
    orig_parser.add_argument(
        '--test-compliance',
        action='store_true',
        help='Test if generated images meet specifications'
    )
    orig_parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for generated images (default: output)'
    )
    
    # Generate variations command
    var_parser = subparsers.add_parser(
        'generate-variations',
        help='Generate all specified format variations from source images'
    )
    var_parser.add_argument(
        '--source-dir',
        default='output',
        help='Directory containing source images (default: output)'
    )
    var_parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for variations (default: output)'
    )
    var_parser.add_argument(
        '--test-compliance',
        action='store_true',
        help='Validate that each variation meets its requirements'
    )
    
    # Compare directories command
    comp_parser = subparsers.add_parser(
        'compare-directories',
        help='Compare identical filenames across two directories'
    )
    comp_parser.add_argument(
        'dir_a',
        help='First directory to compare'
    )
    comp_parser.add_argument(
        'dir_b',
        help='Second directory to compare'
    )
    comp_parser.add_argument(
        '--output-format',
        choices=['table', 'json', 'csv'],
        default='table',
        help='Output format for comparison results (default: table)'
    )
    comp_parser.add_argument(
        '--output-file',
        help='Save comparison results to file'
    )
    
    # Validate variations command
    validate_parser = subparsers.add_parser(
        'validate-variations',
        help='Validate that generated variations meet specifications'
    )
    validate_parser.add_argument(
        '--output-dir',
        default='output',
        help='Directory containing variations to validate (default: output)'
    )
    validate_parser.add_argument(
        '--report-file',
        help='Save validation report to file (JSON or text format)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        if args.command == 'generate-original':
            print("Generating original test images...")
            success = generate_original_images(args.output_dir)
            
            if success and args.test_compliance:
                print("\nTesting image compliance...")
                test_original_compliance(args.output_dir)
            
        elif args.command == 'generate-variations':
            print("Generating format variations...")
            success = generate_variations(args.source_dir, args.output_dir)
            
            if success and args.test_compliance:
                print("\nTesting variation compliance...")
                test_variation_compliance(args.output_dir)
                
        elif args.command == 'compare-directories':
            print(f"Comparing directories: {args.dir_a} vs {args.dir_b}")
            compare_directories(
                args.dir_a, 
                args.dir_b, 
                output_format=args.output_format,
                output_file=args.output_file
            )
            
        elif args.command == 'validate-variations':
            print("Validating generated variations...")
            results = validate_all_variations(args.output_dir)
            
            if args.report_file:
                save_validation_report(results, args.report_file)
            
        print("\nOperation completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())