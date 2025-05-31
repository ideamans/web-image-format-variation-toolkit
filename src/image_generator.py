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


def create_jpeg_test_image(width=640, height=480):
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
    
    # Scale flower count and size based on image area
    flower_count = max(200, (width * height) // 300)  # Density-based count
    flower_radius = max(1, min(width, height) // 160)  # Adaptive size
    
    for _ in range(flower_count):
        x = np.random.randint(0, width)
        y = np.random.randint(height//2, height)
        color = flower_colors[np.random.randint(0, len(flower_colors))]
        
        for dx in range(-flower_radius, flower_radius + 1):
            for dy in range(-flower_radius, flower_radius + 1):
                if (0 <= x+dx < width and 
                    0 <= y+dy < height and 
                    dx*dx + dy*dy <= flower_radius*flower_radius):
                    img[y+dy, x+dx] = color
    
    # 4. Cloud layer (soft white regions)
    cloud_layer = np.zeros((height, width))
    
    # Scale cloud parameters based on image size
    cloud_radius = max(50, min(width, height) // 8)  # Adaptive cloud size
    cloud_margin = cloud_radius
    
    for i in range(5):
        cx = np.random.randint(cloud_margin, width - cloud_margin)
        cy = np.random.randint(0, height//4)
        
        x_coords = np.arange(width)[None, :]
        y_coords = np.arange(height)[:, None]
        
        cloud = np.exp(-((x_coords - cx)**2 + (y_coords - cy)**2) / (cloud_radius**2))
        cloud_layer += cloud * 0.3
    
    cloud_layer = np.clip(cloud_layer, 0, 1)
    for c in range(3):
        img[:, :, c] = np.clip(img[:, :, c] + cloud_layer * 100, 0, 255)
    
    # 5. Human skin color elements
    person_x, person_y = width//4, height//2
    skin_color = [220, 180, 140]
    
    # Scale person size based on image dimensions
    person_width = max(15, width // 20)  # Adaptive width
    person_height = max(20, height // 12)  # Adaptive height
    
    for dx in range(-person_width, person_width + 1):
        for dy in range(-person_height, person_height + 1):
            if (dx*dx)/(person_width*person_width) + (dy*dy)/(person_height*person_height) <= 1:
                if (0 <= person_x+dx < width and 
                    0 <= person_y+dy < height):
                    img[person_y+dy, person_x+dx] = skin_color
    
    return Image.fromarray(img)


def create_png_test_image(width=480, height=480):
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
    
    # 2. Geometric shapes (opaque regions) - scaled to image size
    shape_size = min(width, height) // 4  # Adaptive shape size
    stroke_width = max(1, min(width, height) // 160)  # Adaptive stroke
    
    # Circle - positioned at 1/3 width, 1/3 height
    circle_x = width // 3
    circle_y = height // 3
    draw.ellipse([circle_x - shape_size//2, circle_y - shape_size//2, 
                  circle_x + shape_size//2, circle_y + shape_size//2], 
                fill=(255, 100, 100, 255),
                outline=(150, 50, 50, 255),
                width=stroke_width)
    
    # Rectangle - positioned at 2/3 width, 1/3 height
    rect_x = (width * 2) // 3
    rect_y = height // 3
    draw.rectangle([rect_x - shape_size//2, rect_y - shape_size//2,
                    rect_x + shape_size//2, rect_y + shape_size//2], 
                  fill=(100, 255, 100, 255),
                  outline=(50, 150, 50, 255),
                  width=stroke_width)
    
    # Triangle - positioned at 1/2 width, 2/3 height
    tri_x = width // 2
    tri_y = (height * 2) // 3
    triangle_points = [(tri_x, tri_y - shape_size//2), 
                      (tri_x + shape_size//2, tri_y + shape_size//2), 
                      (tri_x - shape_size//2, tri_y + shape_size//2)]
    draw.polygon(triangle_points, 
                fill=(100, 100, 255, 255),
                outline=(50, 50, 150, 255))
    
    # 3. Semi-transparent gradient effect - centered and scaled
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 6  # Adaptive radius
    radius_step = max(2, max_radius // 20)  # Adaptive step size
    
    for radius in range(max_radius, 0, -radius_step):
        alpha = int(255 * (radius / max_radius) * 0.3)
        draw.ellipse([center_x - radius, center_y - radius,
                     center_x + radius, center_y + radius], 
                    fill=(255, 255, 0, alpha))
    
    # 4. Text elements - scaled font and positioned
    font_large_size = max(12, min(width, height) // 12)  # Adaptive font size
    font_medium_size = max(8, font_large_size * 2 // 3)  # Proportional medium font
    
    try:
        font_large = ImageFont.truetype("arial.ttf", font_large_size)
        font_medium = ImageFont.truetype("arial.ttf", font_medium_size)
    except (OSError, IOError):
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
    
    text = "Test テスト 测试"
    text_x, text_y = width // 20, height - height // 4  # Positioned relative to image size
    
    draw.text((text_x + 2, text_y + 2), text, 
             fill=(0, 0, 0, 180), font=font_large)
    draw.text((text_x, text_y), text, 
             fill=(255, 255, 255, 220), font=font_large)
    draw.text((text_x, text_y + font_large_size + 10), "PNG Alpha Test Image", 
             fill=(200, 200, 200, 200), font=font_medium)
    
    # 5. Complex transparency pattern - scaled checker size
    checker_size = max(10, min(width, height) // 12)  # Adaptive checker size
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
    
    # 6. Fine detail noise pattern - scaled noise count
    pixels = img.load()
    noise_count = max(1000, (width * height) // 25)  # Density-based noise count
    
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
    
    # 7. Anti-aliased curved elements - scaled and positioned
    arc_size = min(width, height) // 4  # Adaptive arc size
    arc_margin = width // 20
    arc_stroke = max(2, min(width, height) // 80)  # Adaptive stroke width
    
    draw.arc([arc_margin, arc_margin, arc_margin + arc_size, arc_margin + arc_size], 
            start=0, end=180, fill=(255, 0, 255, 200), width=arc_stroke)
    
    # Curved line - positioned and scaled
    curve_points = []
    curve_length = min(width, height) // 3
    curve_amplitude = curve_length // 4
    curve_start_x = width // 4
    curve_start_y = height - height // 4
    
    for i in range(50):  # Reduced points for smaller images
        t = i / 49.0
        x = int(curve_start_x + curve_length * t + curve_amplitude * np.sin(t * 6.28))
        y = int(curve_start_y + curve_amplitude * np.sin(t * 3.14))
        # Keep points within bounds
        x = max(0, min(width - 1, x))
        y = max(0, min(height - 1, y))
        curve_points.append((x, y))
    
    curve_stroke = max(1, min(width, height) // 120)  # Adaptive curve stroke
    for i in range(len(curve_points) - 1):
        draw.line([curve_points[i], curve_points[i + 1]], 
                 fill=(0, 255, 255, 180), width=curve_stroke)
    
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


def create_gif_test_animation(width=200, height=200, frame_count=10):
    """
    Generate an ideal GIF test animation with diverse elements and movement.
    
    Args:
        width (int): Image width in pixels
        height (int): Image height in pixels
        frame_count (int): Number of animation frames
    
    Returns:
        list: List of PIL.Image frames for GIF animation
    """
    frames = []
    
    for frame_idx in range(frame_count):
        # Create base frame
        img = Image.new('RGBA', (width, height), (50, 50, 50, 255))  # Dark gray background
        draw = ImageDraw.Draw(img)
        
        # Animation progress (0.0 to 1.0)
        progress = frame_idx / (frame_count - 1) if frame_count > 1 else 0
        
        # 1. Moving ball (bouncing)
        ball_x = int(30 + (width - 60) * abs(2 * progress - 1))  # Bounce effect
        ball_y = int(height // 2 + 30 * np.sin(progress * 4 * np.pi))
        draw.ellipse([ball_x - 10, ball_y - 10, ball_x + 10, ball_y + 10], 
                    fill=(255, 100, 100, 255))  # Red ball
        
        # 2. Rotating spinner
        center_x, center_y = width // 2, height // 2
        angle = progress * 360 * 2  # 2 full rotations
        spinner_length = 25
        end_x = center_x + spinner_length * np.cos(np.radians(angle))
        end_y = center_y + spinner_length * np.sin(np.radians(angle))
        draw.line([center_x, center_y, end_x, end_y], fill=(100, 255, 100, 255), width=3)
        
        # 3. Color changing background elements
        hue = (progress * 360) % 360
        rgb = hsv_to_rgb(hue, 0.8, 0.9)
        
        # Corner squares with changing colors
        for corner_idx, (x, y) in enumerate([(10, 10), (width-30, 10), (10, height-30), (width-30, height-30)]):
            corner_hue = (hue + corner_idx * 90) % 360
            corner_rgb = hsv_to_rgb(corner_hue, 0.6, 0.8)
            draw.rectangle([x, y, x + 20, y + 20], fill=(*corner_rgb, 255))
        
        # 4. Pulsing text
        text_alpha = int(128 + 127 * np.sin(progress * 4 * np.pi))
        try:
            font = ImageFont.load_default()
        except:
            font = None
        
        draw.text((width//2 - 15, height - 25), "GIF", 
                 fill=(255, 255, 255, text_alpha), font=font)
        
        # 5. Progress bar
        bar_width = int((width - 20) * progress)
        draw.rectangle([10, height - 10, 10 + bar_width, height - 5], 
                      fill=(255, 255, 0, 255))
        
        frames.append(img)
    
    return frames


def save_gif_with_options(frames, filename, duration=100, loop=0, optimize=False, 
                         palette_size=256, dither=True):
    """
    Save GIF animation with specified options.
    
    Args:
        frames (list): List of PIL.Image frames
        filename (str): Output filename
        duration (int): Frame duration in milliseconds
        loop (int): Loop count (0 = infinite)
        optimize (bool): Enable GIF optimization
        palette_size (int): Maximum colors in palette (2-256)
        dither (bool): Enable dithering
    """
    if not frames:
        raise ValueError("No frames provided")
    
    # Ensure all frames are in RGBA mode
    rgba_frames = []
    for frame in frames:
        if frame.mode != 'RGBA':
            frame = frame.convert('RGBA')
        rgba_frames.append(frame)
    
    # Convert to palette mode if specified
    if palette_size < 256:
        # Create quantized frames
        quantized_frames = []
        for frame in rgba_frames:
            # Convert RGBA to RGB for quantization
            if frame.mode == 'RGBA':
                # Create white background for transparency
                background = Image.new('RGB', frame.size, (255, 255, 255))
                background.paste(frame, mask=frame.split()[-1])  # Use alpha as mask
                frame = background
            
            # Quantize to specified palette size
            quantized = frame.quantize(colors=palette_size, dither=Image.FLOYDSTEINBERG if dither else Image.NONE)
            quantized_frames.append(quantized)
        
        save_frames = quantized_frames
    else:
        save_frames = rgba_frames
    
    # Save GIF
    save_frames[0].save(
        filename,
        format='GIF',
        save_all=True,
        append_images=save_frames[1:],
        duration=duration,
        loop=loop,
        optimize=optimize
    )
    
    print(f"GIF animation saved: {filename}")
    print(f"  Frames: {len(save_frames)}")
    print(f"  Duration: {duration}ms per frame")
    print(f"  Palette size: {palette_size} colors")
    print(f"  File size: {Path(filename).stat().st_size} bytes")


def generate_original_images(output_dir="output"):
    """Generate JPEG, PNG, and GIF test images with ideal specifications."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print("Generating ideal test images...")
    
    try:
        # Generate JPEG test image
        print("\n1. Creating JPEG test image...")
        jpeg_img = create_jpeg_test_image(width=640, height=480)
        jpeg_path = output_path / "test_original.jpg"
        save_jpeg_with_metadata(jpeg_img, str(jpeg_path))
        
        # Generate PNG test image  
        print("\n2. Creating PNG test image...")
        png_img = create_png_test_image(width=480, height=480)
        png_path = output_path / "test_original.png"
        save_png_with_metadata(png_img, str(png_path))
        
        # Generate GIF test animation
        print("\n3. Creating GIF test animation...")
        gif_frames = create_gif_test_animation(width=200, height=200, frame_count=10)
        gif_path = output_path / "test_original.gif"
        save_gif_with_options(gif_frames, str(gif_path), duration=100, loop=0, 
                             optimize=False, palette_size=256, dither=True)
        
        print("\nGeneration complete!")
        print("\nGenerated files:")
        print(f"  {jpeg_path} - JPEG with rich EXIF data, diverse content")
        print(f"  {png_path} - PNG with transparency, metadata chunks")
        print(f"  {gif_path} - GIF with animation, diverse elements")
        
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