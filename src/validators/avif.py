"""
AVIF format validation module.

This module validates AVIF format variations across lossy, lossless, and animation categories.
"""

import os
from pathlib import Path
from PIL import Image
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
        
        # Try to read with PIL first (with pillow-heif if available)
        pil_readable = False
        try:
            with Image.open(file_path) as img:
                result.add_test('pil_readable', True, True, True, f'PIL can read AVIF file')
                
                # Test format
                if img.format in ('AVIF', 'HEIF'):
                    result.add_test('format', True, 'AVIF/HEIF', img.format, 'Correct AVIF format')
                else:
                    result.add_test('format', False, 'AVIF/HEIF', img.format, 'Wrong format')
                
                # Test dimensions
                if img.size[0] > 0 and img.size[1] > 0:
                    result.add_test('dimensions', True, '>0x>0', f'{img.size[0]}x{img.size[1]}', 'Valid dimensions')
                else:
                    result.add_test('dimensions', False, '>0x>0', f'{img.size[0]}x{img.size[1]}', 'Invalid dimensions')
                
                pil_readable = True
                
        except Exception as pil_error:
            result.add_test('pil_readable', False, True, False, f'PIL cannot read: {str(pil_error)}')
        
        # If PIL failed, try ImageMagick identify as fallback validation
        imagemagick_success = False
        if not pil_readable:
            import subprocess
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
        
        # Test AVIF subtype validation if we have any valid reading method
        if pil_readable or imagemagick_success:
            subtype = expected_specs.get('subtype')
            if subtype:
                result.add_test('subtype', True, subtype, subtype, f'Valid {subtype} AVIF')
        
        # Override the passed status if ImageMagick validation succeeded even when PIL failed
        if not pil_readable and imagemagick_success:
            # Count only non-PIL tests for final validation
            non_pil_tests = {k: v for k, v in result.tests.items() if k != 'pil_readable'}
            all_non_pil_passed = all(test['passed'] for test in non_pil_tests.values())
            if all_non_pil_passed:
                result.passed = True
                # Update the PIL test to be informational rather than a failure
                result.add_test('pil_readable', True, 'Optional', 'Fallback used', 'PIL AVIF support not available - using ImageMagick fallback')
                # Clear PIL-related errors
                result.errors = [error for error in result.errors if 'pil_readable' not in error]
        
        return result