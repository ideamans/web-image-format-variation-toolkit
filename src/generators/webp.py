"""
WebP format variation generator.

This module handles generation of all WebP format variations across
lossy, lossless, and animation categories.
"""

import os
from pathlib import Path
from PIL import Image
import sys
import os
# Add parent directory to path for image_generator import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from image_generator import create_gif_test_animation


class WebpGenerator:
    """WebP format variation generator."""
    
    @staticmethod
    def generate_variations(source_dir, output_dir):
        """Generate WebP format variations."""
        try:
            variations_index = []
            source_path = Path(source_dir)
            output_path = Path(output_dir)
            
            # Create WebP subdirectories
            lossy_dir = output_path / "webp" / "lossy"
            lossless_dir = output_path / "webp" / "lossless" 
            animation_dir = output_path / "webp" / "animation"
            
            lossy_dir.mkdir(parents=True, exist_ok=True)
            lossless_dir.mkdir(parents=True, exist_ok=True)
            animation_dir.mkdir(parents=True, exist_ok=True)
            
            # Source images
            jpeg_source = source_path / "test_original.jpg"
            png_source = source_path / "test_original.png"
            gif_source = source_path / "test_original.gif"
            
            print("Generating WebP variations...")
            
            # Generate lossy WebP from JPEG source
            if jpeg_source.exists():
                WebpGenerator._generate_lossy_webp(jpeg_source, lossy_dir, variations_index)
            
            # Generate lossless WebP from PNG source
            if png_source.exists():
                WebpGenerator._generate_lossless_webp(png_source, lossless_dir, variations_index)
            
            # Generate animation WebP from GIF source
            if gif_source.exists():
                WebpGenerator._generate_animation_webp(gif_source, animation_dir, variations_index)
            
            print("WebP variations generated successfully")
            return variations_index
            
        except Exception as e:
            print(f"Error generating WebP variations: {e}")
            return None
    
    @staticmethod
    def _generate_lossy_webp(source_file, output_dir, variations_index):
        """Generate lossy WebP variations."""
        try:
            # Load source JPEG
            with Image.open(source_file) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')
                
                # Generate quality variations matching JPEG quality levels
                quality_levels = [20, 50, 80, 95]
                
                for quality in quality_levels:
                    output_path = output_dir / f"quality_{quality}.webp"
                    img.save(output_path, 'WEBP', quality=quality, method=6)
                    
                    variations_index.append({
                        "format": "webp",
                        "path": f"webp/lossy/quality_{quality}.webp",
                        "jp": f"WebP損失圧縮 品質{quality}（JPEG源画像から変換）",
                        "en": f"WebP lossy compression quality {quality} (converted from JPEG source)"
                    })
                    
                    print(f"Generated lossy WebP quality {quality}: {output_path}")
                
        except Exception as e:
            print(f"Error generating lossy WebP: {e}")
    
    @staticmethod
    def _generate_lossless_webp(source_file, output_dir, variations_index):
        """Generate lossless WebP variations."""
        try:
            # Load source PNG
            with Image.open(source_file) as img:
                # Basic lossless WebP
                output_path = output_dir / "original.webp"
                img.save(output_path, 'WEBP', lossless=True, quality=100, method=6)
                
                variations_index.append({
                    "format": "webp",
                    "path": "webp/lossless/original.webp",
                    "jp": "WebP無損失圧縮（PNG源画像から変換）",
                    "en": "WebP lossless compression (converted from PNG source)"
                })
                
                print(f"Generated lossless WebP: {output_path}")
                
        except Exception as e:
            print(f"Error generating lossless WebP: {e}")
    
    @staticmethod
    def _generate_animation_webp(source_file, output_dir, variations_index):
        """Generate animation WebP variations."""
        try:
            # Load source GIF frames
            frames = []
            durations = []
            
            with Image.open(source_file) as gif:
                for frame_idx in range(getattr(gif, 'n_frames', 1)):
                    gif.seek(frame_idx)
                    frame = gif.copy()
                    
                    # Convert to RGBA for WebP animation
                    if frame.mode != 'RGBA':
                        frame = frame.convert('RGBA')
                    
                    frames.append(frame)
                    
                    # Get frame duration (default 100ms if not available)
                    duration = gif.info.get('duration', 100)
                    durations.append(duration)
            
            if frames:
                # Basic animation WebP
                output_path = output_dir / "original.webp"
                frames[0].save(
                    output_path,
                    'WEBP',
                    save_all=True,
                    append_images=frames[1:],
                    duration=durations,
                    loop=0,  # Infinite loop
                    quality=80,
                    method=6
                )
                
                variations_index.append({
                    "format": "webp",
                    "path": "webp/animation/original.webp",
                    "jp": "WebPアニメーション（GIF源画像から変換）",
                    "en": "WebP animation (converted from GIF source)"
                })
                
                print(f"Generated animation WebP: {output_path} ({len(frames)} frames)")
            
        except Exception as e:
            print(f"Error generating animation WebP: {e}")