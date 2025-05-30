"""
Original test image generation module.

This module contains functions to generate ideal JPEG and PNG source images
that meet all specifications for comprehensive format variation testing.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from PIL import PngImagePlugin
import noise
import piexif
import colorsys
import os
from pathlib import Path


def create_jpeg_test_image(width=2000, height=1500):
    """
    Generate an ideal JPEG test image with diverse frequency components and color information.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
    
    Returns:
        PIL.Image: Generated RGB image suitable for JPEG testing
    """
    # Initialize base image array
    img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # 1. Sky gradient (low-frequency components)
    for y in range(height//3):
        gradient_pos = y / (height//3)
        blue_val = int(255 * (1 - gradient_pos) * 0.8)
        white_mix = int(255 * gradient_pos * 0.3)
        img[y, :] = [blue_val + white_mix, blue_val + white_mix, 255]
    
    # 2. Ground/grass area (high-frequency components)
    for y in range(height//3, height):
        for x in range(width):
            grass_noise = noise.pnoise2(x/50, y/50, octaves=4)
            green_base = 80 + int(grass_noise * 40)
            img[y, x] = [
                green_base//3,
                green_base,
                green_base//4
            ]
    
    # 3. Flower scatter (colorful point elements)
    flower_colors = [
        [255, 100, 100],  # Red
        [255, 255, 100],  # Yellow
        [150, 100, 255],  # Purple
        [255, 150, 200]   # Pink
    ]
    
    for _ in range(1000):
        x = np.random.randint(0, width)
        y = np.random.randint(height//2, height)
        color = flower_colors[np.random.randint(0, len(flower_colors))]
        
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if (0 <= x+dx < width and 
                    0 <= y+dy < height and 
                    dx*dx + dy*dy <= 4):
                    img[y+dy, x+dx] = color
    
    # 4. Cloud layer (soft white regions)
    cloud_layer = np.zeros((height, width))
    
    for i in range(5):
        cx = np.random.randint(100, width-100)
        cy = np.random.randint(0, height//4)
        
        x_coords = np.arange(width)[None, :]
        y_coords = np.arange(height)[:, None]
        
        cloud = np.exp(-((x_coords - cx)**2 + (y_coords - cy)**2) / (100**2))
        cloud_layer += cloud * 0.3
    
    cloud_layer = np.clip(cloud_layer, 0, 1)
    for c in range(3):
        img[:, :, c] = np.clip(img[:, :, c] + cloud_layer * 100, 0, 255)
    
    # 5. Human skin color elements
    person_x, person_y = width//4, height//2
    skin_color = [220, 180, 140]
    
    for dx in range(-30, 31):
        for dy in range(-40, 41):
            if (dx*dx)/(30*30) + (dy*dy)/(40*40) <= 1:
                if (0 <= person_x+dx < width and 
                    0 <= person_y+dy < height):
                    img[person_y+dy, person_x+dx] = skin_color
    
    return Image.fromarray(img)


def create_png_test_image(width=1500, height=1500):
    """
    Generate an ideal PNG test image with transparency, sharp edges, and various elements.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
    
    Returns:
        PIL.Image: Generated RGBA image suitable for PNG testing
    """
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Background gradient with transparency
    pixels = img.load()
    for y in range(height):
        alpha = int(128 * (1 - y / height))
        
        for x in range(width):
            hue = (x / width) * 360
            rgb = hsv_to_rgb(hue, 0.8, 0.9)
            pixels[x, y] = (*rgb, alpha)
    
    # 2. Geometric shapes (opaque regions)
    draw.ellipse([200, 200, 400, 400], 
                fill=(255, 100, 100, 255),
                outline=(150, 50, 50, 255),
                width=3)
    
    draw.rectangle([600, 200, 800, 400], 
                  fill=(100, 255, 100, 255),
                  outline=(50, 150, 50, 255),
                  width=3)
    
    triangle_points = [(1000, 200), (1100, 400), (900, 400)]
    draw.polygon(triangle_points, 
                fill=(100, 100, 255, 255),
                outline=(50, 50, 150, 255))
    
    # 3. Semi-transparent gradient effect
    center_x, center_y = 750, 750
    for radius in range(100, 0, -5):
        alpha = int(255 * (radius / 100) * 0.3)
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius], 
                    fill=(255, 255, 0, alpha))
    
    # 4. Text elements
    try:
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_medium = ImageFont.truetype("arial.ttf", 40)
    except (OSError, IOError):
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    text = "Test テスト 测试"
    text_x, text_y = 100, 600
    
    draw.text((text_x + 2, text_y + 2), text, 
             fill=(0, 0, 0, 180), font=font_large)
    draw.text((text_x, text_y), text, 
             fill=(255, 255, 255, 220), font=font_large)
    draw.text((text_x, text_y + 80), "PNG Alpha Test Image", 
             fill=(200, 200, 200, 200), font=font_medium)
    
    # 5. Complex transparency pattern
    checker_size = 50
    alpha_levels = [0, 128, 255]
    
    for x in range(0, width, checker_size):
        for y in range(height//2, height, checker_size):
            checker_x = x // checker_size
            checker_y = y // checker_size
            
            alpha_index = (checker_x + checker_y) % 3
            alpha = alpha_levels[alpha_index]
            
            red = min(255, (x * 255) // width)
            green = min(255, (y * 255) // height)
            blue = 128
            
            draw.rectangle([x, y, x + checker_size, y + checker_size], 
                          fill=(red, green, blue, alpha))
    
    # 6. Fine detail noise pattern
    pixels = img.load()
    noise_count = 10000
    
    for _ in range(noise_count):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        
        current_pixel = pixels[x, y]
        
        if current_pixel[3] > 0:
            noise_val = np.random.randint(-20, 21)
            r, g, b, a = current_pixel
            pixels[x, y] = (
                np.clip(r + noise_val, 0, 255),
                np.clip(g + noise_val, 0, 255), 
                np.clip(b + noise_val, 0, 255),
                a
            )
    
    # 7. Anti-aliased curved elements
    draw.arc([50, 50, 200, 200], start=0, end=180, 
            fill=(255, 0, 255, 200), width=8)
    
    curve_points = []
    for i in range(100):
        t = i / 99.0
        x = int(300 + 200 * t + 50 * np.sin(t * 6.28))
        y = int(1200 + 100 * np.sin(t * 3.14))
        curve_points.append((x, y))
    
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i + 1]], 
                 fill=(0, 255, 255, 180), width=4)
    
    return img


def hsv_to_rgb(h, s, v):
    """Convert HSV color to RGB."""
    rgb_float = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return tuple(int(c * 255) for c in rgb_float)


def save_jpeg_with_metadata(img, filename):
    """Save JPEG image with comprehensive EXIF metadata for testing."""
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Software: "Image Test Generator v1.0",
            piexif.ImageIFD.DateTime: "2025:05:31 12:00:00",
            piexif.ImageIFD.ImageWidth: img.width,
            piexif.ImageIFD.ImageLength: img.height,
            piexif.ImageIFD.Orientation: 1,
            piexif.ImageIFD.XResolution: (72, 1),
            piexif.ImageIFD.YResolution: (72, 1),
            piexif.ImageIFD.ResolutionUnit: 2,
            piexif.ImageIFD.Copyright: "Test Image - No Rights Reserved"
        },
        "Exif": {
            piexif.ExifIFD.ExifVersion: b"0230",
            piexif.ExifIFD.ColorSpace: 1,
            piexif.ExifIFD.PixelXDimension: img.width,
            piexif.ExifIFD.PixelYDimension: img.height,
            piexif.ExifIFD.DateTimeOriginal: "2025:05:31 12:00:00",
            piexif.ExifIFD.DateTimeDigitized: "2025:05:31 12:00:00",
            piexif.ExifIFD.FNumber: (56, 10),
            piexif.ExifIFD.ExposureTime: (1, 125),
            piexif.ExifIFD.ISOSpeedRatings: 200,
            piexif.ExifIFD.FocalLength: (50, 1),
        },
        "GPS": {
            piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
            piexif.GPSIFD.GPSLatitudeRef: "N",
            piexif.GPSIFD.GPSLatitude: [(35, 1), (40, 1), (34, 1)],
            piexif.GPSIFD.GPSLongitudeRef: "E", 
            piexif.GPSIFD.GPSLongitude: [(139, 1), (39, 1), (1, 1)],
            piexif.GPSIFD.GPSAltitudeRef: 0,
            piexif.GPSIFD.GPSAltitude: (10, 1),
            piexif.GPSIFD.GPSTimeStamp: [(12, 1), (0, 1), (0, 1)],
            piexif.GPSIFD.GPSDateStamp: "2025:05:31"
        },
        "1st": {},
        "thumbnail": None
    }
    
    exif_bytes = piexif.dump(exif_dict)
    
    img.save(filename, "JPEG", 
             quality=98,
             subsampling=0,
             exif=exif_bytes,
             optimize=False)
    
    print(f"JPEG test image saved: {filename}")
    print(f"  Size: {img.width}x{img.height}")
    print(f"  EXIF data: {len(exif_bytes)} bytes")


def save_png_with_metadata(img, filename):
    """Save PNG image with comprehensive metadata chunks for testing."""
    pnginfo = PngImagePlugin.PngInfo()
    
    pnginfo.add_text("Software", "PNG Test Generator v1.0")
    pnginfo.add_text("Author", "Image Processing Toolkit")
    pnginfo.add_text("Description", "Test image with transparency and various PNG features")
    pnginfo.add_text("Creation Time", "2025-05-31T12:00:00Z")
    
    long_description = (
        "This PNG test image contains multiple elements designed to test "
        "various PNG format features including transparency gradients, "
        "sharp geometric shapes, anti-aliased text, complex alpha patterns, "
        "and fine detail noise. The image uses 32-bit RGBA format with "
        "full color depth and comprehensive alpha channel variations."
    )
    # Note: PIL doesn't support compressed text directly, using regular text
    pnginfo.add_text("Long Description", long_description)
    
    pnginfo.add_itxt("Title", "テスト画像", "ja", "Test Image")
    pnginfo.add_itxt("Keywords", "测试,图像,PNG", "zh", "test,image,PNG")
    
    pnginfo.add_text("Color Type", "RGBA (Truecolor with Alpha)")
    pnginfo.add_text("Bit Depth", "8 bits per channel")
    pnginfo.add_text("Compression", "Deflate")
    pnginfo.add_text("Filter", "Adaptive")
    pnginfo.add_text("Interlace", "None")
    
    pnginfo.add_text("Test Version", "1.0")
    pnginfo.add_text("Generator", "Python PIL + Custom Code")
    pnginfo.add_text("Purpose", "Format Variation Testing")
    
    img.save(filename, "PNG",
             pnginfo=pnginfo,
             optimize=False,
             compress_level=6)
    
    print(f"PNG test image saved: {filename}")
    print(f"  Size: {img.width}x{img.height}")
    print(f"  Color mode: {img.mode}")
    print(f"  Metadata chunks: {len(pnginfo.chunks)}")


def generate_original_images(output_dir="output"):
    """Generate both JPEG and PNG test images with ideal specifications."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Generating ideal test images...")
    
    try:
        # Generate JPEG test image
        print("\n1. Creating JPEG test image...")
        jpeg_img = create_jpeg_test_image(width=2000, height=1500)
        jpeg_path = output_path / "test_original.jpg"
        save_jpeg_with_metadata(jpeg_img, str(jpeg_path))
        
        # Generate PNG test image  
        print("\n2. Creating PNG test image...")
        png_img = create_png_test_image(width=1500, height=1500)
        png_path = output_path / "test_original.png"
        save_png_with_metadata(png_img, str(png_path))
        
        print("\nGeneration complete!")
        print("\nGenerated files:")
        print(f"  {jpeg_path} - JPEG with rich EXIF data, diverse content")
        print(f"  {png_path} - PNG with transparency, metadata chunks")
        
        return True
        
    except Exception as e:
        print(f"Error generating images: {e}")
        return False


def test_original_compliance(output_dir="output"):
    """Test if generated images meet specifications."""
    output_path = Path(output_dir)
    
    jpeg_path = output_path / "test_original.jpg"
    png_path = output_path / "test_original.png"
    
    print("Testing image compliance...")
    
    # Test JPEG compliance
    if jpeg_path.exists():
        try:
            with Image.open(jpeg_path) as img:
                print(f"\nJPEG Image Analysis:")
                print(f"  Format: {img.format}")
                print(f"  Mode: {img.mode}")
                print(f"  Size: {img.size}")
                
                # Check EXIF data
                exif_data = img._getexif()
                if exif_data:
                    print(f"  EXIF tags: {len(exif_data)} entries")
                else:
                    print("  EXIF data: Not found")
                    
        except Exception as e:
            print(f"  Error reading JPEG: {e}")
    
    # Test PNG compliance
    if png_path.exists():
        try:
            with Image.open(png_path) as img:
                print(f"\nPNG Image Analysis:")
                print(f"  Format: {img.format}")
                print(f"  Mode: {img.mode}")
                print(f"  Size: {img.size}")
                print(f"  Has transparency: {img.mode in ('RGBA', 'LA')}")
                
                # Check PNG info
                if hasattr(img, 'text'):
                    print(f"  Text chunks: {len(img.text)} entries")
                    
        except Exception as e:
            print(f"  Error reading PNG: {e}")
    
    print("\nCompliance testing complete!")