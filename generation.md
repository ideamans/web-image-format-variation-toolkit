# Image Generation Source Code Documentation

## Overview

This document provides complete source code for generating ideal test images for JPEG and PNG format testing. The code creates synthetic images that meet all specified requirements for comprehensive format variation testing.

## Required Libraries

```python
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from scipy import ndimage
import noise  # Perlin noise library
import piexif
from PIL import PngImagePlugin
import colorsys
import random
```

Install required packages:
```bash
pip install pillow numpy matplotlib scipy noise piexif
```

## JPEG Test Image Generation

### Main Generation Function

```python
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
    # Creates smooth blue-to-white transition in upper third
    for y in range(height//3):
        # Calculate gradient position (0.0 to 1.0)
        gradient_pos = y / (height//3)
        
        # Blue component decreases from top to bottom
        blue_val = int(255 * (1 - gradient_pos) * 0.8)
        
        # White mixing increases from top to bottom
        white_mix = int(255 * gradient_pos * 0.3)
        
        # Apply gradient across entire width
        img[y, :] = [blue_val + white_mix, blue_val + white_mix, 255]
    
    # 2. Ground/grass area (high-frequency components)
    # Uses Perlin noise to simulate natural grass texture
    for y in range(height//3, height):
        for x in range(width):
            # Generate Perlin noise for natural texture
            # Scale: 50 = texture size, octaves: 4 = detail levels
            grass_noise = noise.pnoise2(x/50, y/50, octaves=4)
            
            # Convert noise (-1 to 1) to green color variation
            green_base = 80 + int(grass_noise * 40)  # 40-120 range
            
            # Create natural grass color (green dominant)
            img[y, x] = [
                green_base//3,    # Red component (low)
                green_base,       # Green component (high)
                green_base//4     # Blue component (low)
            ]
    
    # 3. Flower scatter (colorful point elements)
    # Adds small colored dots to simulate flowers
    flower_colors = [
        [255, 100, 100],  # Red flowers
        [255, 255, 100],  # Yellow flowers
        [150, 100, 255],  # Purple flowers
        [255, 150, 200]   # Pink flowers
    ]
    
    for _ in range(1000):  # Generate 1000 flowers
        # Random position in lower 2/3 of image (ground area)
        x = np.random.randint(0, width)
        y = np.random.randint(height//2, height)
        
        # Select random flower color
        color = np.random.choice(flower_colors)
        
        # Draw small circular flower (radius ~2 pixels)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                # Check bounds and circular shape
                if (0 <= x+dx < width and 
                    0 <= y+dy < height and 
                    dx*dx + dy*dy <= 4):
                    img[y+dy, x+dx] = color
    
    # 4. Cloud layer (soft white regions)
    # Creates realistic cloud formations using Gaussian distributions
    cloud_layer = np.zeros((height, width))
    
    for i in range(5):  # Generate 5 cloud formations
        # Random cloud center in upper portion of sky
        cx = np.random.randint(100, width-100)
        cy = np.random.randint(0, height//4)
        
        # Create Gaussian cloud shape
        x_coords = np.arange(width)[None, :]
        y_coords = np.arange(height)[:, None]
        
        # Gaussian distribution with 100-pixel standard deviation
        cloud = np.exp(-((x_coords - cx)**2 + (y_coords - cy)**2) / (100**2))
        
        # Add to cloud layer with reduced intensity
        cloud_layer += cloud * 0.3
    
    # Normalize and apply clouds to image
    cloud_layer = np.clip(cloud_layer, 0, 1)
    for c in range(3):  # Apply to all RGB channels
        img[:, :, c] = np.clip(img[:, :, c] + cloud_layer * 100, 0, 255)
    
    # 5. Human skin color elements
    # Adds simplified human figure for skin tone testing
    person_x, person_y = width//4, height//2
    skin_color = [220, 180, 140]  # Realistic skin tone
    
    # Draw elliptical face shape
    for dx in range(-30, 31):
        for dy in range(-40, 41):
            # Ellipse equation: (x/a)² + (y/b)² ≤ 1
            if (dx*dx)/(30*30) + (dy*dy)/(40*40) <= 1:
                if (0 <= person_x+dx < width and 
                    0 <= person_y+dy < height):
                    img[person_y+dy, person_x+dx] = skin_color
    
    # Convert numpy array to PIL Image
    return Image.fromarray(img)
```

### JPEG Metadata and Saving Function

```python
def save_jpeg_with_metadata(img, filename):
    """
    Save JPEG image with comprehensive EXIF metadata for testing.
    
    Args:
        img (PIL.Image): Image to save
        filename (str): Output filename
    """
    # Create comprehensive EXIF data dictionary
    exif_dict = {
        # Primary image data (IFD0)
        "0th": {
            piexif.ImageIFD.Software: "Image Test Generator v1.0",
            piexif.ImageIFD.DateTime: "2025:05:31 12:00:00",
            piexif.ImageIFD.ImageWidth: img.width,
            piexif.ImageIFD.ImageLength: img.height,
            piexif.ImageIFD.Orientation: 1,  # Normal orientation
            piexif.ImageIFD.XResolution: (72, 1),  # 72 DPI
            piexif.ImageIFD.YResolution: (72, 1),  # 72 DPI
            piexif.ImageIFD.ResolutionUnit: 2,  # Inches
            piexif.ImageIFD.Copyright: "Test Image - No Rights Reserved"
        },
        
        # Camera/shooting data (Exif IFD)
        "Exif": {
            piexif.ExifIFD.ExifVersion: b"0230",
            piexif.ExifIFD.ColorSpace: 1,  # sRGB
            piexif.ExifIFD.PixelXDimension: img.width,
            piexif.ExifIFD.PixelYDimension: img.height,
            piexif.ExifIFD.DateTimeOriginal: "2025:05:31 12:00:00",
            piexif.ExifIFD.DateTimeDigitized: "2025:05:31 12:00:00",
            # Simulated camera settings
            piexif.ExifIFD.FNumber: (56, 10),  # f/5.6
            piexif.ExifIFD.ExposureTime: (1, 125),  # 1/125s
            piexif.ExifIFD.ISOSpeedRatings: 200,
            piexif.ExifIFD.FocalLength: (50, 1),  # 50mm
        },
        
        # GPS location data
        "GPS": {
            piexif.GPSIFD.GPSVersionID: (2, 3, 0, 0),
            # Tokyo coordinates: 35.6762°N, 139.6503°E
            piexif.GPSIFD.GPSLatitudeRef: "N",
            piexif.GPSIFD.GPSLatitude: [(35, 1), (40, 1), (34, 1)],  # 35°40'34"N
            piexif.GPSIFD.GPSLongitudeRef: "E", 
            piexif.GPSIFD.GPSLongitude: [(139, 1), (39, 1), (1, 1)],  # 139°39'01"E
            piexif.GPSIFD.GPSAltitudeRef: 0,  # Above sea level
            piexif.GPSIFD.GPSAltitude: (10, 1),  # 10 meters
            piexif.GPSIFD.GPSTimeStamp: [(12, 1), (0, 1), (0, 1)],  # 12:00:00 UTC
            piexif.GPSIFD.GPSDateStamp: "2025:05:31"
        },
        
        # Thumbnail data (optional)
        "1st": {},
        "thumbnail": None
    }
    
    # Convert EXIF dictionary to bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Save with maximum quality and no subsampling
    img.save(filename, "JPEG", 
             quality=98,           # Very high quality
             subsampling=0,        # 4:4:4 (no chroma subsampling)
             exif=exif_bytes,      # Include EXIF data
             optimize=False)       # Don't optimize (preserve exact settings)

    print(f"JPEG test image saved: {filename}")
    print(f"  Size: {img.width}x{img.height}")
    print(f"  EXIF data: {len(exif_bytes)} bytes")
```

## PNG Test Image Generation

### Main Generation Function

```python
def create_png_test_image(width=1500, height=1500):
    """
    Generate an ideal PNG test image with transparency, sharp edges, and various elements.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
    
    Returns:
        PIL.Image: Generated RGBA image suitable for PNG testing
    """
    # Create RGBA image with transparent background
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 1. Background gradient with transparency
    # Creates rainbow hue gradient horizontally, alpha gradient vertically
    pixels = img.load()
    for y in range(height):
        # Alpha decreases from top (128) to bottom (0)
        alpha = int(128 * (1 - y / height))
        
        for x in range(width):
            # Hue shifts from 0° to 360° across width
            hue = (x / width) * 360
            
            # Convert HSV to RGB (high saturation and brightness)
            rgb = hsv_to_rgb(hue, 0.8, 0.9)
            
            # Set pixel with calculated alpha
            pixels[x, y] = (*rgb, alpha)
    
    # 2. Geometric shapes (opaque regions)
    # Solid colored shapes for sharp edge testing
    
    # Red circle
    draw.ellipse([200, 200, 400, 400], 
                fill=(255, 100, 100, 255),    # Solid red
                outline=(150, 50, 50, 255),   # Darker red outline
                width=3)
    
    # Green rectangle
    draw.rectangle([600, 200, 800, 400], 
                  fill=(100, 255, 100, 255),   # Solid green
                  outline=(50, 150, 50, 255),  # Darker green outline
                  width=3)
    
    # Blue triangle
    triangle_points = [(1000, 200), (1100, 400), (900, 400)]
    draw.polygon(triangle_points, 
                fill=(100, 100, 255, 255),    # Solid blue
                outline=(50, 50, 150, 255))   # Darker blue outline
    
    # 3. Semi-transparent gradient effect
    # Concentric circles with decreasing alpha for soft shadows
    center_x, center_y = 750, 750
    for radius in range(100, 0, -5):  # From 100px to 5px, step -5
        # Alpha decreases with radius
        alpha = int(255 * (radius / 100) * 0.3)  # Max 30% opacity
        
        # Yellow gradient circle
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius], 
                    fill=(255, 255, 0, alpha))
    
    # 4. Text elements (anti-aliasing verification)
    # Multi-language text to test font rendering and anti-aliasing
    try:
        # Try to load a standard font
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_medium = ImageFont.truetype("arial.ttf", 40)
    except (OSError, IOError):
        # Fallback to default font if system font not available
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    # Main text with shadow effect
    text = "Test テスト 测试"
    text_x, text_y = 100, 600
    
    # Shadow (offset black text)
    draw.text((text_x + 2, text_y + 2), text, 
             fill=(0, 0, 0, 180), font=font_large)
    
    # Main text (white with slight transparency)
    draw.text((text_x, text_y), text, 
             fill=(255, 255, 255, 220), font=font_large)
    
    # Smaller descriptive text
    draw.text((text_x, text_y + 80), "PNG Alpha Test Image", 
             fill=(200, 200, 200, 200), font=font_medium)
    
    # 5. Complex transparency pattern
    # Checkerboard with three alpha levels for comprehensive testing
    checker_size = 50
    alpha_levels = [0, 128, 255]  # Transparent, semi-transparent, opaque
    
    for x in range(0, width, checker_size):
        for y in range(height//2, height, checker_size):
            # Calculate checker position
            checker_x = x // checker_size
            checker_y = y // checker_size
            
            # Determine alpha level (cycles through 3 levels)
            alpha_index = (checker_x + checker_y) % 3
            alpha = alpha_levels[alpha_index]
            
            # Color based on position (creates gradient effect)
            red = min(255, (x * 255) // width)
            green = min(255, (y * 255) // height)
            blue = 128  # Constant blue component
            
            # Draw checker square
            draw.rectangle([x, y, x + checker_size, y + checker_size], 
                          fill=(red, green, blue, alpha))
    
    # 6. Fine detail noise pattern
    # Add random noise to test compression and fine detail handling
    pixels = img.load()
    noise_count = 10000
    
    for _ in range(noise_count):
        # Random position
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        
        # Get existing pixel
        current_pixel = pixels[x, y]
        
        # Only add noise to non-transparent pixels
        if current_pixel[3] > 0:
            # Random noise value (-20 to +20)
            noise_val = np.random.randint(-20, 21)
            
            # Apply noise to RGB channels, preserve alpha
            r, g, b, a = current_pixel
            pixels[x, y] = (
                np.clip(r + noise_val, 0, 255),
                np.clip(g + noise_val, 0, 255), 
                np.clip(b + noise_val, 0, 255),
                a  # Keep original alpha
            )
    
    # 7. Anti-aliased curved elements
    # Smooth curves to test anti-aliasing preservation
    
    # Draw smooth arc
    draw.arc([50, 50, 200, 200], start=0, end=180, 
            fill=(255, 0, 255, 200), width=8)
    
    # Draw smooth bezier-like curve using multiple line segments
    curve_points = []
    for i in range(100):
        t = i / 99.0  # Parameter from 0 to 1
        x = int(300 + 200 * t + 50 * np.sin(t * 6.28))  # Sinusoidal curve
        y = int(1200 + 100 * np.sin(t * 3.14))
        curve_points.append((x, y))
    
    # Draw smooth curve as connected line segments
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i + 1]], 
                 fill=(0, 255, 255, 180), width=4)
    
    return img

def hsv_to_rgb(h, s, v):
    """
    Convert HSV color to RGB.
    
    Args:
        h (float): Hue (0-360 degrees)
        s (float): Saturation (0.0-1.0)
        v (float): Value/Brightness (0.0-1.0)
    
    Returns:
        tuple: RGB values (0-255)
    """
    rgb_float = colorsys.hsv_to_rgb(h / 360.0, s, v)
    return tuple(int(c * 255) for c in rgb_float)
```

### PNG Metadata and Saving Function

```python
def save_png_with_metadata(img, filename):
    """
    Save PNG image with comprehensive metadata chunks for testing.
    
    Args:
        img (PIL.Image): Image to save
        filename (str): Output filename
    """
    # Create PNG info object for metadata
    pnginfo = PngImagePlugin.PngInfo()
    
    # Add various text chunks for metadata testing
    
    # Standard text chunk (tEXt)
    pnginfo.add_text("Software", "PNG Test Generator v1.0")
    pnginfo.add_text("Author", "Image Processing Toolkit")
    pnginfo.add_text("Description", "Test image with transparency and various PNG features")
    pnginfo.add_text("Creation Time", "2025-05-31T12:00:00Z")
    
    # Compressed text chunk (zTXt) - longer text gets compressed
    long_description = (
        "This PNG test image contains multiple elements designed to test "
        "various PNG format features including transparency gradients, "
        "sharp geometric shapes, anti-aliased text, complex alpha patterns, "
        "and fine detail noise. The image uses 32-bit RGBA format with "
        "full color depth and comprehensive alpha channel variations."
    )
    pnginfo.add_text("Long Description", long_description, compress=True)
    
    # International text chunk (iTXt) - supports UTF-8
    pnginfo.add_itxt("Title", "テスト画像", "ja", "Test Image")  # Japanese
    pnginfo.add_itxt("Keywords", "测试,图像,PNG", "zh", "test,image,PNG")  # Chinese
    
    # Technical parameters
    pnginfo.add_text("Color Type", "RGBA (Truecolor with Alpha)")
    pnginfo.add_text("Bit Depth", "8 bits per channel")
    pnginfo.add_text("Compression", "Deflate")
    pnginfo.add_text("Filter", "Adaptive")
    pnginfo.add_text("Interlace", "None")
    
    # Custom application-specific data
    pnginfo.add_text("Test Version", "1.0")
    pnginfo.add_text("Generator", "Python PIL + Custom Code")
    pnginfo.add_text("Purpose", "Format Variation Testing")
    
    # Save PNG with metadata and specific settings
    img.save(filename, "PNG",
             pnginfo=pnginfo,      # Include metadata
             optimize=False,       # Don't optimize (preserve exact settings)
             compress_level=6)     # Default compression level
    
    print(f"PNG test image saved: {filename}")
    print(f"  Size: {img.width}x{img.height}")
    print(f"  Color mode: {img.mode}")
    print(f"  Metadata chunks: {len(pnginfo.chunks)}")
```

## Complete Generation Script

```python
def main():
    """
    Generate both JPEG and PNG test images with ideal specifications.
    """
    print("Generating ideal test images...")
    
    # Generate JPEG test image
    print("\n1. Creating JPEG test image...")
    jpeg_img = create_jpeg_test_image(width=2000, height=1500)
    save_jpeg_with_metadata(jpeg_img, "test_original.jpg")
    
    # Generate PNG test image  
    print("\n2. Creating PNG test image...")
    png_img = create_png_test_image(width=1500, height=1500)
    save_png_with_metadata(png_img, "test_original.png")
    
    print("\nGeneration complete!")
    print("\nGenerated files:")
    print("  test_original.jpg - JPEG with rich EXIF data, diverse content")
    print("  test_original.png - PNG with transparency, metadata chunks")
    
    # Optional: Display basic image information
    print(f"\nJPEG Image Info:")
    print(f"  Format: {jpeg_img.format}")
    print(f"  Mode: {jpeg_img.mode}")
    print(f"  Size: {jpeg_img.size}")
    
    print(f"\nPNG Image Info:")
    print(f"  Format: {png_img.format}")
    print(f"  Mode: {png_img.mode}")
    print(f"  Size: {png_img.size}")
    print(f"  Has transparency: {png_img.mode in ('RGBA', 'LA')}")

if __name__ == "__main__":
    main()
```

## Usage Instructions

1. **Install dependencies**:
   ```bash
   pip install pillow numpy matplotlib scipy noise piexif
   ```

2. **Run the generation script**:
   ```bash
   python generate_test_images.py
   ```

3. **Output files**:
   - `test_original.jpg`: JPEG with high quality, rich EXIF data, diverse content
   - `test_original.png`: PNG with RGBA, transparency gradients, metadata chunks

## Key Features Explained

### JPEG Image Features
- **Sky gradient**: Low-frequency content for compression testing
- **Grass texture**: High-frequency content using Perlin noise
- **Flower scatter**: Sharp colorful details for artifact detection
- **Cloud layer**: Soft transitions and transparency effects
- **Skin tones**: Human-perceptible color accuracy testing
- **Rich EXIF**: GPS, camera settings, timestamps for metadata testing

### PNG Image Features
- **Alpha gradient**: Full range of transparency values (0-255)
- **Geometric shapes**: Sharp edges for lossless compression verification
- **Text rendering**: Anti-aliasing and font handling
- **Transparency patterns**: Complex alpha channel variations
- **Fine noise**: Compression efficiency testing
- **Metadata chunks**: Text, compressed text, and international text

This code generates ideal source images that meet all specifications for comprehensive JPEG and PNG format variation testing.
