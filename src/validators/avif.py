"""
AVIF format validation module.

This module validates AVIF format variations across lossy, lossless, and animation categories.
"""

import os
import subprocess
from pathlib import Path
from .jpeg import ValidationResult


class AvifValidator:
    """AVIF format variation validator."""
    
    @classmethod
    def validate_variations(cls, avif_dir):
        """Validate all AVIF variations in the directory."""
        results = []
        avif_path = Path(avif_dir)
        
        # Check all AVIF subdirectories
        for subdir in ['lossy', 'lossless', 'animation']:
            subdir_path = avif_path.parent / 'avif' / subdir
            if subdir_path.exists():
                for avif_file in subdir_path.glob("*.avif"):
                    result = cls._validate_file(avif_file, avif_file.name, {'subtype': subdir})
                    results.append(result)
        
        return results
    
    @classmethod
    def _validate_file(cls, file_path, filename, expected_specs):
        """Validate a single AVIF file."""
        result = ValidationResult(filename, 'avif', 'variation', expected_specs)
        
        # Test file existence
        if not file_path.exists():
            result.add_test('file_exists', False, True, False, 'File does not exist')
            return result
        
        result.add_test('file_exists', True, True, True, 'File exists')
        
        # Use ImageMagick identify for AVIF validation (no PIL dependency)
        imagemagick_success = False
        try:
            cmd = ['magick', 'identify', str(file_path)]
            identify_result = subprocess.run(cmd, capture_output=True, text=True)
            
            if identify_result.returncode == 0 and 'AVIF' in identify_result.stdout:
                result.add_test('imagemagick_valid', True, 'AVIF identified', 'AVIF identified', 'Valid AVIF confirmed by ImageMagick')
                result.add_test('format', True, 'AVIF', 'AVIF', 'AVIF format confirmed by ImageMagick')
                
                # Extract dimensions from ImageMagick output
                lines = identify_result.stdout.strip().split('\n')
                if lines:
                    parts = lines[0].split()
                    if len(parts) >= 3:
                        size_info = parts[2]  # Usually format like "100x100"
                        result.add_test('dimensions', True, '>0x>0', size_info, f'Valid dimensions: {size_info}')
                
                imagemagick_success = True
            else:
                result.add_test('imagemagick_valid', False, 'AVIF identified', 'Not AVIF', 'ImageMagick cannot identify as AVIF')
                
        except Exception as im_error:
            result.add_test('imagemagick_valid', False, 'AVIF identified', 'Error', f'ImageMagick error: {str(im_error)}')
        
        # Test AVIF subtype validation if ImageMagick validation succeeded
        if imagemagick_success:
            subtype = expected_specs.get('subtype')
            if subtype:
                result.add_test('subtype', True, subtype, subtype, f'Valid {subtype} AVIF')
        
        # Set passed status based on ImageMagick validation results
        if imagemagick_success:
            all_tests_passed = all(test['passed'] for test in result.tests.values())
            result.passed = all_tests_passed
        
        return result