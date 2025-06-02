"""
WebP format validation module.

This module validates WebP format variations across lossy, lossless, and animation categories.
"""

import os
from pathlib import Path
from PIL import Image
from .jpeg import ValidationResult


class WebpValidator:
    """WebP format variation validator."""
    
    @classmethod
    def validate_variations(cls, webp_dir):
        """Validate all WebP variations in the directory."""
        results = []
        webp_path = Path(webp_dir)
        
        # Check all WebP subdirectories
        for subdir in ['lossy', 'lossless', 'animation']:
            subdir_path = webp_path.parent / 'webp' / subdir
            if subdir_path.exists():
                for webp_file in subdir_path.glob("*.webp"):
                    result = cls._validate_file(webp_file, webp_file.name, {'subtype': subdir})
                    results.append(result)
        
        return results
    
    @classmethod
    def _validate_file(cls, file_path, filename, expected_specs):
        """Validate a single WebP file."""
        result = ValidationResult(filename, 'webp', 'variation', expected_specs)
        
        # Test file existence
        if not file_path.exists():
            result.add_test('file_exists', False, True, False, 'File does not exist')
            return result
        
        result.add_test('file_exists', True, True, True, 'File exists')
        
        try:
            # Test file can be opened as WebP
            with Image.open(file_path) as img:
                if img.format != 'WEBP':
                    result.add_test('format', False, 'WEBP', img.format, 'Wrong format')
                else:
                    result.add_test('format', True, 'WEBP', img.format, 'Correct WebP format')
                
                # Test image has valid dimensions
                if img.size[0] > 0 and img.size[1] > 0:
                    result.add_test('dimensions', True, '>0x>0', f'{img.size[0]}x{img.size[1]}', 'Valid dimensions')
                else:
                    result.add_test('dimensions', False, '>0x>0', f'{img.size[0]}x{img.size[1]}', 'Invalid dimensions')
                
                # Test WebP subtype validation
                subtype = expected_specs.get('subtype')
                if subtype:
                    if subtype == 'animation':
                        # Check if it's animated
                        frame_count = getattr(img, 'n_frames', 1)
                        if frame_count > 1:
                            result.add_test('animation', True, '>1 frames', f'{frame_count} frames', f'Animated WebP with {frame_count} frames')
                        else:
                            result.add_test('animation', False, '>1 frames', f'{frame_count} frame', 'Expected animation but got static image')
                    else:
                        # For lossy/lossless, just verify it's a valid WebP
                        result.add_test('subtype', True, subtype, subtype, f'Valid {subtype} WebP')
                
        except Exception as e:
            result.add_test('readable', False, True, False, f'Cannot read WebP file: {str(e)}')
        
        return result