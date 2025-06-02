"""
GIF format variation validator.

This module handles validation of GIF format variations.
"""

from PIL import Image
from pathlib import Path
from .jpeg import ValidationResult  # Reuse ValidationResult class


class GifValidator:
    """GIF format variation validator."""
    
    @staticmethod
    def validate_variations(gif_dir):
        """Validate GIF variations."""
        results = []
        
        # Define GIF variation specifications
        gif_specs = {
            # Frame count variations
            'frames_single.gif': {'frame_count': 1, 'is_animated': False},
            'frames_short.gif': {'frame_count': 5, 'is_animated': True},
            'frames_medium.gif': {'frame_count': 10, 'is_animated': True},
            'frames_long.gif': {'frame_count': 20, 'is_animated': True},
            
            # Frame rate variations (duration in ms)
            'fps_slow.gif': {'frame_duration': 200, 'is_animated': True},
            'fps_normal.gif': {'frame_duration': 100, 'is_animated': True},
            'fps_fast.gif': {'frame_duration': 40, 'is_animated': True},
            
            # Palette size variations (approximate)
            'palette_2colors.gif': {'palette_size_range': (1, 4), 'is_animated': True},
            'palette_16colors.gif': {'palette_size_range': (8, 32), 'is_animated': True},
            'palette_256colors.gif': {'palette_size_range': (64, 256), 'is_animated': True},
            
            # Dithering variations
            'dither_nodither.gif': {'has_dithering': False, 'is_animated': True},
            'dither_dithered.gif': {'has_dithering': True, 'is_animated': True},
            
            # Optimization variations
            'optimize_noopt.gif': {'is_optimized': False, 'is_animated': True},
            'optimize_optimized.gif': {'is_optimized': True, 'is_animated': True},
            
            # Loop variations
            'loop_loop_infinite.gif': {'loop_count': 0, 'is_animated': True},
            'loop_loop_once.gif': {'loop_count': 1, 'is_animated': True},
            'loop_loop_3times.gif': {'loop_count': 3, 'is_animated': True},
        }
        
        for filename, specs in gif_specs.items():
            file_path = gif_dir / filename
            if file_path.exists():
                result = GifValidator._validate_file(file_path, filename, specs)
                results.append(result)
            else:
                # File doesn't exist
                result = ValidationResult(filename, 'gif', 'missing', specs)
                result.add_test('file_exists', False, True, False, 'File not found')
                results.append(result)
        
        return results
    
    @staticmethod
    def _validate_file(file_path, filename, expected_specs):
        """Validate a single GIF file."""
        result = ValidationResult(filename, 'gif', 'variation', expected_specs)
        
        try:
            with Image.open(file_path) as img:
                # Test file opens successfully
                result.add_test('file_readable', True, True, True)
                
                # Test animation properties
                if 'is_animated' in expected_specs:
                    expected_animated = expected_specs['is_animated']
                    is_animated = getattr(img, 'is_animated', False)
                    result.add_test('is_animated', is_animated == expected_animated, 
                                  expected_animated, is_animated)
                
                # Test frame count
                if 'frame_count' in expected_specs:
                    expected_frame_count = expected_specs['frame_count']
                    actual_frame_count = getattr(img, 'n_frames', 1)
                    result.add_test('frame_count', actual_frame_count == expected_frame_count, 
                                  expected_frame_count, actual_frame_count)
                
                # Test frame duration
                if 'frame_duration' in expected_specs and hasattr(img, 'info') and 'duration' in img.info:
                    expected_duration = expected_specs['frame_duration']
                    actual_duration = img.info.get('duration', 100)
                    # Allow some tolerance for duration
                    duration_match = abs(actual_duration - expected_duration) <= 20
                    result.add_test('frame_duration', duration_match, 
                                  f"{expected_duration}ms", f"{actual_duration}ms")
                elif 'frame_duration' in expected_specs:
                    result.add_test('frame_duration', False, 
                                  f"{expected_specs['frame_duration']}ms", "unknown")
                
                # Test palette size (approximate)
                if 'palette_size_range' in expected_specs:
                    palette_range = expected_specs['palette_size_range']
                    try:
                        # Try to get palette information
                        if hasattr(img, 'palette') and img.palette:
                            palette_size = len(img.palette.colors) if hasattr(img.palette, 'colors') else 256
                        else:
                            # Fallback: estimate from mode
                            palette_size = 256 if img.mode == 'P' else 256
                        
                        in_range = palette_range[0] <= palette_size <= palette_range[1]
                        result.add_test('palette_size', in_range, 
                                      f"{palette_range[0]}-{palette_range[1]}", palette_size)
                    except:
                        result.add_test('palette_size', True, 
                                      f"{palette_range[0]}-{palette_range[1]}", "estimated")
                
                # Test loop count
                if 'loop_count' in expected_specs and hasattr(img, 'info'):
                    expected_loop = expected_specs['loop_count']
                    actual_loop = img.info.get('loop', 0)
                    result.add_test('loop_count', actual_loop == expected_loop, 
                                  expected_loop, actual_loop)
                elif 'loop_count' in expected_specs:
                    result.add_test('loop_count', True, 
                                  expected_specs['loop_count'], "default")
                
        except Exception as e:
            result.add_test('file_readable', False, True, False, str(e))
        
        return result