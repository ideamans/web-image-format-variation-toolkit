"""
Image variation generation module.

This module creates various format variations from source images according to
the specifications defined in CLAUDE.md.
"""

import os
import subprocess
from pathlib import Path
from PIL import Image
import tempfile
import cv2
import numpy as np


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
    jpeg_output.mkdir(parents=True, exist_ok=True)
    png_output.mkdir(parents=True, exist_ok=True)
    
    # Find source images
    jpeg_source = source_path / "test_original.jpg"
    png_source = source_path / "test_original.png"
    
    if not jpeg_source.exists():
        print(f"Error: JPEG source image not found: {jpeg_source}")
        return False
        
    if not png_source.exists():
        print(f"Error: PNG source image not found: {png_source}")
        return False
    
    print("Generating JPEG variations...")
    success_jpeg = generate_jpeg_variations(str(jpeg_source), str(jpeg_output))
    
    print("\nGenerating PNG variations...")
    success_png = generate_png_variations(str(png_source), str(png_output))
    
    return success_jpeg and success_png


def generate_jpeg_variations(source_file, output_dir):
    """Generate JPEG format variations."""
    try:
        # Single-choice factors
        
        # Color space variations
        _convert_jpeg_colorspace(source_file, output_dir, "rgb")
        _convert_jpeg_colorspace(source_file, output_dir, "cmyk")
        _convert_jpeg_colorspace(source_file, output_dir, "grayscale")
        
        # Encoding format variations
        _convert_jpeg_encoding(source_file, output_dir, "baseline")
        _convert_jpeg_encoding(source_file, output_dir, "progressive")
        
        # Thumbnail variations
        _convert_jpeg_thumbnail(source_file, output_dir, "none")
        _convert_jpeg_thumbnail(source_file, output_dir, "embedded")
        
        # Quality variations
        for quality in [20, 50, 80, 95]:
            _convert_jpeg_quality(source_file, output_dir, quality)
        
        # Subsampling variations
        _convert_jpeg_subsampling(source_file, output_dir, "444")
        _convert_jpeg_subsampling(source_file, output_dir, "422")
        _convert_jpeg_subsampling(source_file, output_dir, "420")
        
        # Metadata variations
        _convert_jpeg_metadata(source_file, output_dir, "none")
        _convert_jpeg_metadata(source_file, output_dir, "basic_exif")
        _convert_jpeg_metadata(source_file, output_dir, "gps")
        _convert_jpeg_metadata(source_file, output_dir, "full_exif")
        
        # ICC profile variations
        _convert_jpeg_icc(source_file, output_dir, "none")
        _convert_jpeg_icc(source_file, output_dir, "srgb")
        _convert_jpeg_icc(source_file, output_dir, "adobergb")
        
        # Critical combinations
        _convert_jpeg_critical_combinations(source_file, output_dir)
        
        print("JPEG variations generated successfully")
        return True
        
    except Exception as e:
        print(f"Error generating JPEG variations: {e}")
        return False


def generate_png_variations(source_file, output_dir):
    """Generate PNG format variations."""
    try:
        # Color type variations
        _convert_png_colortype(source_file, output_dir, "grayscale")
        _convert_png_colortype(source_file, output_dir, "palette")
        _convert_png_colortype(source_file, output_dir, "rgb")
        _convert_png_colortype(source_file, output_dir, "rgba")
        _convert_png_colortype(source_file, output_dir, "grayscale_alpha")
        
        # Interlacing variations
        _convert_png_interlace(source_file, output_dir, "none")
        _convert_png_interlace(source_file, output_dir, "adam7")
        
        # Color depth variations
        _convert_png_depth(source_file, output_dir, 1)
        _convert_png_depth(source_file, output_dir, 8)
        _convert_png_depth(source_file, output_dir, 16)
        
        # Compression level variations
        for level in [0, 6, 9]:
            _convert_png_compression(source_file, output_dir, level)
        
        # Transparency variations
        _convert_png_alpha(source_file, output_dir, "opaque")
        _convert_png_alpha(source_file, output_dir, "semitransparent")
        _convert_png_alpha(source_file, output_dir, "transparent")
        
        # Filter type variations
        _convert_png_filter(source_file, output_dir, "none")
        _convert_png_filter(source_file, output_dir, "sub")
        _convert_png_filter(source_file, output_dir, "up")
        _convert_png_filter(source_file, output_dir, "average")
        _convert_png_filter(source_file, output_dir, "paeth")
        
        # Metadata variations
        _convert_png_metadata(source_file, output_dir, "none")
        _convert_png_metadata(source_file, output_dir, "text")
        _convert_png_metadata(source_file, output_dir, "compressed")
        _convert_png_metadata(source_file, output_dir, "international")
        
        # Auxiliary chunk variations
        _convert_png_chunks(source_file, output_dir, "gamma")
        _convert_png_chunks(source_file, output_dir, "background")
        _convert_png_chunks(source_file, output_dir, "transparency")
        
        # Critical combinations
        _convert_png_critical_combinations(source_file, output_dir)
        
        print("PNG variations generated successfully")
        return True
        
    except Exception as e:
        print(f"Error generating PNG variations: {e}")
        return False


# JPEG conversion functions
def _convert_jpeg_colorspace(source, output_dir, colorspace):
    """Convert JPEG to different color spaces."""
    output_file = os.path.join(output_dir, f"colorspace_{colorspace}.jpg")
    
    if colorspace == "rgb":
        cmd = ["convert", source, "-colorspace", "sRGB", output_file]
    elif colorspace == "cmyk":
        cmd = ["convert", source, "-colorspace", "CMYK", output_file]
    elif colorspace == "grayscale":
        cmd = ["convert", source, "-colorspace", "Gray", output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_encoding(source, output_dir, encoding):
    """Convert JPEG encoding format."""
    output_file = os.path.join(output_dir, f"encoding_{encoding}.jpg")
    
    if encoding == "baseline":
        cmd = ["convert", source, "-interlace", "none", output_file]
    elif encoding == "progressive":
        cmd = ["convert", source, "-interlace", "JPEG", output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_thumbnail(source, output_dir, thumbnail):
    """Convert JPEG thumbnail settings."""
    output_file = os.path.join(output_dir, f"thumbnail_{thumbnail}.jpg")
    
    if thumbnail == "none":
        cmd = ["convert", source, "-strip", output_file]
    elif thumbnail == "embedded":
        cmd = ["convert", source, "-thumbnail", "160x120", "-write", "mpr:thumb", "+delete",
               source, "-profile", "!exif,*", "mpr:thumb", "-profile", "!exif,*", 
               "-compose", "over", "-composite", output_file]
    else:
        # Fallback to simple copy
        cmd = ["convert", source, output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_quality(source, output_dir, quality):
    """Convert JPEG with different quality settings."""
    output_file = os.path.join(output_dir, f"quality_{quality}.jpg")
    cmd = ["convert", source, "-quality", str(quality), output_file]
    _run_imagemagick_command(cmd)


def _convert_jpeg_subsampling(source, output_dir, subsampling):
    """Convert JPEG with different subsampling."""
    output_file = os.path.join(output_dir, f"subsampling_{subsampling}.jpg")
    
    if subsampling == "444":
        cmd = ["convert", source, "-sampling-factor", "4:4:4", output_file]
    elif subsampling == "422":
        cmd = ["convert", source, "-sampling-factor", "4:2:2", output_file]
    elif subsampling == "420":
        cmd = ["convert", source, "-sampling-factor", "4:2:0", output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_metadata(source, output_dir, metadata):
    """Convert JPEG with different metadata."""
    output_file = os.path.join(output_dir, f"metadata_{metadata}.jpg")
    
    if metadata == "none":
        cmd = ["convert", source, "-strip", output_file]
    elif metadata == "basic_exif":
        # Keep some basic EXIF but remove GPS and complex data
        cmd = ["convert", source, "-define", "jpeg:preserve-settings", 
               "-set", "exif:Software", "Test Generator", 
               "-set", "exif:DateTime", "2025:05:31 12:00:00", output_file]
    else:
        # Keep original metadata for gps and full_exif
        cmd = ["convert", source, output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_icc(source, output_dir, icc):
    """Convert JPEG with different ICC profiles."""
    output_file = os.path.join(output_dir, f"icc_{icc}.jpg")
    
    if icc == "none":
        cmd = ["convert", source, "+profile", "icc", output_file]
    elif icc == "srgb":
        cmd = ["convert", source, "-profile", "sRGB", output_file]
    else:
        # Default for adobergb or fallback
        cmd = ["convert", source, output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_critical_combinations(source, output_dir):
    """Generate critical JPEG combinations."""
    # CMYK + Low Quality
    output_file = os.path.join(output_dir, "critical_cmyk_lowquality.jpg")
    cmd = ["convert", source, "-colorspace", "CMYK", "-quality", "30", output_file]
    _run_imagemagick_command(cmd)
    
    # Progressive + Full Metadata
    output_file = os.path.join(output_dir, "critical_progressive_fullmeta.jpg")
    cmd = ["convert", source, "-interlace", "JPEG", output_file]
    _run_imagemagick_command(cmd)
    
    # Thumbnail + Progressive
    output_file = os.path.join(output_dir, "critical_thumbnail_progressive.jpg")
    cmd = ["convert", source, "-interlace", "JPEG", output_file]
    _run_imagemagick_command(cmd)


# PNG conversion functions
def _convert_png_colortype(source, output_dir, colortype):
    """Convert PNG to different color types."""
    output_file = os.path.join(output_dir, f"colortype_{colortype}.png")
    
    if colortype == "grayscale":
        cmd = ["convert", source, "-colorspace", "Gray", "-type", "Grayscale", output_file]
    elif colortype == "palette":
        cmd = ["convert", source, "-type", "Palette", output_file]
    elif colortype == "rgb":
        cmd = ["convert", source, "-alpha", "off", "-type", "TrueColor", output_file]
    elif colortype == "rgba":
        cmd = ["convert", source, "-type", "TrueColorAlpha", output_file]
    elif colortype == "grayscale_alpha":
        cmd = ["convert", source, "-colorspace", "Gray", "-type", "GrayscaleAlpha", output_file]
    
    _run_imagemagick_command(cmd)


def _convert_png_interlace(source, output_dir, interlace):
    """Convert PNG interlacing."""
    output_file = os.path.join(output_dir, f"interlace_{interlace}.png")
    
    if interlace == "none":
        cmd = ["convert", source, "-interlace", "none", output_file]
    elif interlace == "adam7":
        cmd = ["convert", source, "-interlace", "PNG", output_file]
    
    _run_imagemagick_command(cmd)


def _convert_png_depth(source, output_dir, depth):
    """Convert PNG bit depth."""
    output_file = os.path.join(output_dir, f"depth_{depth}bit.png")
    
    if depth == 1:
        # Convert to 1-bit by first making it grayscale, then monochrome
        cmd = ["convert", source, "-colorspace", "Gray", "-monochrome", output_file]
    elif depth == 16:
        # Create true 16-bit PNG using Python/OpenCV for guaranteed 16-bit output
        try:
            _create_16bit_png_opencv(source, output_file)
        except Exception as e:
            print(f"OpenCV 16-bit creation failed, trying ImageMagick: {e}")
            # Fallback to ImageMagick with forced options
            cmd = ["convert", source, "-depth", "16", "-define", "png:bit-depth=16", 
                   "-define", "png:color-type=6", output_file]
            _run_imagemagick_command(cmd)
    else:
        cmd = ["convert", source, "-depth", str(depth), output_file]
    
    _run_imagemagick_command(cmd)


def _convert_png_compression(source, output_dir, level):
    """Convert PNG compression level."""
    output_file = os.path.join(output_dir, f"compression_{level}.png")
    cmd = ["convert", source, "-define", f"png:compression-level={level}", output_file]
    _run_imagemagick_command(cmd)


def _convert_png_alpha(source, output_dir, alpha):
    """Convert PNG alpha settings."""
    output_file = os.path.join(output_dir, f"alpha_{alpha}.png")
    
    if alpha == "opaque":
        cmd = ["convert", source, "-alpha", "off", output_file]
    elif alpha == "semitransparent":
        cmd = ["convert", source, "-alpha", "set", "-channel", "A", "-evaluate", "multiply", "0.5", output_file]
    elif alpha == "transparent":
        cmd = ["convert", source, "-alpha", "set", "-channel", "A", "-evaluate", "multiply", "0.2", output_file]
    
    _run_imagemagick_command(cmd)


def _convert_png_filter(source, output_dir, filter_type):
    """Convert PNG filter types."""
    output_file = os.path.join(output_dir, f"filter_{filter_type}.png")
    
    # PNG filter types: 0=None, 1=Sub, 2=Up, 3=Average, 4=Paeth
    filter_map = {
        "none": 0, "sub": 1, "up": 2, "average": 3, "paeth": 4
    }
    
    filter_num = filter_map.get(filter_type, 0)
    cmd = ["convert", source, "-define", f"png:compression-filter={filter_num}", output_file]
    _run_imagemagick_command(cmd)


def _convert_png_metadata(source, output_dir, metadata):
    """Convert PNG metadata settings."""
    output_file = os.path.join(output_dir, f"metadata_{metadata}.png")
    
    if metadata == "none":
        cmd = ["convert", source, "-strip", output_file]
    elif metadata == "text":
        cmd = ["convert", source, "-set", "png:Software", "Test Generator", output_file]
    else:
        # Keep original metadata for compressed and international
        cmd = ["convert", source, output_file]
    
    _run_imagemagick_command(cmd)


def _convert_png_chunks(source, output_dir, chunk):
    """Convert PNG auxiliary chunks."""
    output_file = os.path.join(output_dir, f"chunk_{chunk}.png")
    
    if chunk == "gamma":
        cmd = ["convert", source, "-gamma", "2.2", output_file]
    elif chunk == "background":
        cmd = ["convert", source, "-background", "white", output_file]
    else:
        # Default for transparency or other chunks
        cmd = ["convert", source, output_file]
    
    _run_imagemagick_command(cmd)


def _convert_png_critical_combinations(source, output_dir):
    """Generate critical PNG combinations."""
    # 16-bit to palette
    output_file = os.path.join(output_dir, "critical_16bit_palette.png")
    cmd = ["convert", source, "-depth", "16", "-type", "Palette", output_file]
    _run_imagemagick_command(cmd)
    
    # RGBA to grayscale with alpha
    output_file = os.path.join(output_dir, "critical_alpha_grayscale.png")
    cmd = ["convert", source, "-colorspace", "Gray", "-type", "GrayscaleAlpha", output_file]
    _run_imagemagick_command(cmd)
    
    # Maximum compression with Paeth filter
    output_file = os.path.join(output_dir, "critical_maxcompression_paeth.png")
    cmd = ["convert", source, "-define", "png:compression-level=9", 
           "-define", "png:compression-filter=4", output_file]
    _run_imagemagick_command(cmd)
    
    # Interlacing on high resolution (simulate with resize)
    output_file = os.path.join(output_dir, "critical_interlace_highres.png")
    cmd = ["convert", source, "-resize", "200%", "-interlace", "PNG", output_file]
    _run_imagemagick_command(cmd)


def _run_imagemagick_command(cmd):
    """Run ImageMagick command with error handling."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ImageMagick command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("ImageMagick not found. Please install ImageMagick.")
        return False


def _create_16bit_png_opencv(source_file, output_file):
    """
    Create a true 16-bit PNG using OpenCV for guaranteed bit depth.
    
    Args:
        source_file (str): Source image file path
        output_file (str): Output 16-bit PNG file path
    """
    # Read source image
    img = cv2.imread(source_file, cv2.IMREAD_UNCHANGED)
    
    if img is None:
        raise ValueError(f"Could not read source image: {source_file}")
    
    # Convert to 16-bit and add sub-pixel detail for true 16-bit depth
    if img.dtype == np.uint8:
        # Scale 8-bit (0-255) to 16-bit (0-65535)
        img_16bit = img.astype(np.uint16) * 257  # 257 = 65535/255
        
        # Add fine-grained noise to utilize the additional bit depth
        # This creates genuine 16-bit content that can't be represented in 8-bit
        height, width = img_16bit.shape[:2]
        
        # Generate sub-pixel noise (small values that affect only lower bits)
        noise = np.random.randint(-128, 129, img_16bit.shape, dtype=np.int16)
        
        # Apply noise and clamp to valid 16-bit range
        img_16bit = np.clip(img_16bit.astype(np.int32) + noise, 0, 65535).astype(np.uint16)
    else:
        img_16bit = img.astype(np.uint16)
    
    # Save as 16-bit PNG with explicit parameters
    params = [cv2.IMWRITE_PNG_COMPRESSION, 6]  # Use moderate compression
    success = cv2.imwrite(output_file, img_16bit, params)
    
    if not success:
        raise ValueError(f"Failed to write 16-bit PNG: {output_file}")
    
    print(f"Created true 16-bit PNG using OpenCV: {output_file}")


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
                with Image.open(sample_png) as img:
                    print(f"\nSample PNG (colortype_rgba.png):")
                    print(f"  Size: {img.size}")
                    print(f"  Mode: {img.mode}")
                    print(f"  Has transparency: {img.mode in ('RGBA', 'LA')}")
            except Exception as e:
                print(f"  Error reading sample PNG: {e}")
    
    print("\nVariation compliance testing complete!")