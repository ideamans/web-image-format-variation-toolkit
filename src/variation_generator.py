"""
Image variation generation module.

This module creates various format variations from source images according to
the specifications defined in CLAUDE.md.
"""

import json
from pathlib import Path
from .generators.jpeg import JpegGenerator
from .generators.png import PngGenerator
from .generators.gif import GifGenerator
from .generators.webp import WebpGenerator
from .generators.avif import AvifGenerator


def generate_variations(source_dir="output", output_dir="output"):
    """
    Generate all specified format variations from source images.
    
    Args:
        source_dir (str): Directory containing source images
        output_dir (str): Output directory for variations
        
    Returns:
        bool: True if successful, False otherwise
    """
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    
    # Create output directories
    jpeg_output = output_path / "jpeg"
    png_output = output_path / "png"
    gif_output = output_path / "gif"
    
    jpeg_output.mkdir(parents=True, exist_ok=True)
    png_output.mkdir(parents=True, exist_ok=True)
    gif_output.mkdir(parents=True, exist_ok=True)
    
    # Find source images
    jpeg_source = source_path / "test_original.jpg"
    png_source = source_path / "test_original.png"
    gif_source = source_path / "test_original.gif"
    
    if not jpeg_source.exists():
        print(f"Error: JPEG source image not found: {jpeg_source}")
        return False
        
    if not png_source.exists():
        print(f"Error: PNG source image not found: {png_source}")
        return False
        
    if not gif_source.exists():
        print(f"Error: GIF source image not found: {gif_source}")
        return False
    
    print("Generating JPEG variations...")
    jpeg_index = JpegGenerator.generate_variations(str(jpeg_source), str(jpeg_output))
    
    print("\nGenerating PNG variations...")
    png_index = PngGenerator.generate_variations(str(png_source), str(png_output))
    
    print("\nGenerating GIF variations...")
    gif_index = GifGenerator.generate_variations(str(gif_source), str(gif_output))
    
    print("\nGenerating WebP variations...")
    webp_index = WebpGenerator.generate_variations(source_dir, output_dir)
    
    print("\nGenerating AVIF variations...")
    avif_index = AvifGenerator.generate_variations(source_dir, output_dir)
    
    # Generate index.json
    if (jpeg_index is not None and png_index is not None and gif_index is not None and 
        webp_index is not None and avif_index is not None):
        all_variations = []
        
        # Add original images
        all_variations.append({
            "format": "jpeg",
            "path": "test_original.jpg",
            "jp": "JPEG元画像（高品質、豊富なメタデータ、多様なコンテンツ）",
            "en": "Original JPEG image (high quality, rich metadata, diverse content)"
        })
        
        all_variations.append({
            "format": "png",
            "path": "test_original.png",
            "jp": "PNG元画像（RGBA、透明度、メタデータチャンク）",
            "en": "Original PNG image (RGBA, transparency, metadata chunks)"
        })
        
        all_variations.append({
            "format": "gif",
            "path": "test_original.gif",
            "jp": "GIF元画像（アニメーション、多様な動的要素）",
            "en": "Original GIF image (animation, diverse dynamic elements)"
        })
        
        # Add variations
        all_variations.extend(jpeg_index)
        all_variations.extend(png_index)
        all_variations.extend(gif_index)
        all_variations.extend(webp_index)
        all_variations.extend(avif_index)
        
        index_file = output_path / "index.json"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(all_variations, f, indent=2, ensure_ascii=False)
        
        print(f"\nGenerated index file: {index_file}")
        print(f"Total variations indexed: {len(all_variations)} (including 3 originals + WebP/AVIF)")
        
        return True
    else:
        return False


def test_variation_compliance(output_dir="output"):
    """Test if generated variations meet specifications."""
    output_path = Path(output_dir)
    
    jpeg_dir = output_path / "jpeg"
    png_dir = output_path / "png"
    
    print("Testing variation compliance...")
    
    # Count generated files
    jpeg_count = len(list(jpeg_dir.glob("*.jpg"))) if jpeg_dir.exists() else 0
    png_count = len(list(png_dir.glob("*.png"))) if png_dir.exists() else 0
    
    print(f"\nGenerated variations:")
    print(f"  JPEG variations: {jpeg_count}")
    print(f"  PNG variations: {png_count}")
    
    # Test a few sample files
    if jpeg_dir.exists():
        sample_jpeg = jpeg_dir / "quality_80.jpg"
        if sample_jpeg.exists():
            try:
                from PIL import Image
                with Image.open(sample_jpeg) as img:
                    print(f"\nSample JPEG (quality_80.jpg):")
                    print(f"  Size: {img.size}")
                    print(f"  Mode: {img.mode}")
            except Exception as e:
                print(f"  Error reading sample JPEG: {e}")
    
    if png_dir.exists():
        sample_png = png_dir / "colortype_rgba.png"
        if sample_png.exists():
            try:
                from PIL import Image
                with Image.open(sample_png) as img:
                    print(f"\nSample PNG (colortype_rgba.png):")
                    print(f"  Size: {img.size}")
                    print(f"  Mode: {img.mode}")
                    print(f"  Has transparency: {img.mode in ('RGBA', 'LA')}")
            except Exception as e:
                print(f"  Error reading sample PNG: {e}")
    
    print("\nVariation compliance testing complete!")


# Legacy function names for backward compatibility
def generate_jpeg_variations(source_file, output_dir):
    """Legacy function - use JpegGenerator.generate_variations instead."""
    return JpegGenerator.generate_variations(source_file, output_dir)


def generate_png_variations(source_file, output_dir):
    """Legacy function - use PngGenerator.generate_variations instead."""
    return PngGenerator.generate_variations(source_file, output_dir)


def generate_gif_variations(source_file, output_dir):
    """Legacy function - use GifGenerator.generate_variations instead."""
    return GifGenerator.generate_variations(source_file, output_dir)


def generate_webp_variations(source_dir, output_dir):
    """Legacy function - use WebpGenerator.generate_variations instead."""
    return WebpGenerator.generate_variations(source_dir, output_dir)


def generate_avif_variations(source_dir, output_dir):
    """Legacy function - use AvifGenerator.generate_variations instead."""
    return AvifGenerator.generate_variations(source_dir, output_dir)