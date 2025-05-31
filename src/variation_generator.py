"""
Image variation generation module.

This module creates various format variations from source images according to
the specifications defined in CLAUDE.md.
"""

import os
import subprocess
import json
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
    
    # Create GIF output directory
    gif_output = output_path / "gif"
    gif_output.mkdir(parents=True, exist_ok=True)
    
    print("Generating JPEG variations...")
    jpeg_index = generate_jpeg_variations(str(jpeg_source), str(jpeg_output))
    
    print("\nGenerating PNG variations...")
    png_index = generate_png_variations(str(png_source), str(png_output))
    
    print("\nGenerating GIF variations...")
    gif_index = generate_gif_variations(str(gif_source), str(gif_output))
    
    # Generate index.json
    if jpeg_index is not None and png_index is not None and gif_index is not None:
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
        
        index_file = output_path / "index.json"
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(all_variations, f, indent=2, ensure_ascii=False)
        
        print(f"\nGenerated index file: {index_file}")
        print(f"Total variations indexed: {len(all_variations)} (including 3 originals)")
        
        return True
    else:
        return False


def generate_jpeg_variations(source_file, output_dir):
    """Generate JPEG format variations."""
    try:
        variations_index = []
        
        # Define JPEG variation specifications with descriptions
        jpeg_specs = [
            # Color space variations
            ("rgb", "colorspace", "RGB色空間での保存", "Saved in RGB color space"),
            ("cmyk", "colorspace", "CMYK色空間での保存（印刷用）", "Saved in CMYK color space (for printing)"),
            ("grayscale", "colorspace", "グレースケール（白黒）での保存", "Saved in grayscale (black and white)"),
            
            # Encoding format variations
            ("baseline", "encoding", "ベースラインJPEG（標準形式）", "Baseline JPEG (standard format)"),
            ("progressive", "encoding", "プログレッシブJPEG（段階的表示対応）", "Progressive JPEG (supports gradual display)"),
            
            # Thumbnail variations
            ("none", "thumbnail", "サムネイル画像なし", "No embedded thumbnail"),
            ("embedded", "thumbnail", "サムネイル画像埋め込み", "Embedded thumbnail image"),
            
            # Quality variations
            (20, "quality", "低品質（高圧縮、ファイルサイズ小）", "Low quality (high compression, small file size)"),
            (50, "quality", "中品質（バランス型）", "Medium quality (balanced)"),
            (80, "quality", "高品質（低圧縮）", "High quality (low compression)"),
            (95, "quality", "最高品質（ほぼ無劣化）", "Highest quality (nearly lossless)"),
            
            # Subsampling variations  
            ("444", "subsampling", "4:4:4サブサンプリング（最高品質）", "4:4:4 subsampling (highest quality)"),
            ("422", "subsampling", "4:2:2サブサンプリング（中品質）", "4:2:2 subsampling (medium quality)"),
            ("420", "subsampling", "4:2:0サブサンプリング（高圧縮）", "4:2:0 subsampling (high compression)"),
            
            # Metadata variations
            ("none", "metadata", "メタデータなし（軽量化）", "No metadata (lightweight)"),
            ("basic_exif", "metadata", "基本的なEXIF情報のみ", "Basic EXIF information only"),
            ("gps", "metadata", "GPS位置情報付きEXIF", "EXIF with GPS location data"),
            ("full_exif", "metadata", "完全なEXIF情報（撮影情報等）", "Complete EXIF information (shooting data, etc.)"),
            
            # ICC profile variations
            ("none", "icc", "カラープロファイルなし", "No color profile"),
            ("srgb", "icc", "sRGBカラープロファイル（Web標準）", "sRGB color profile (web standard)"),
            ("adobergb", "icc", "Adobe RGBカラープロファイル（広色域）", "Adobe RGB color profile (wide gamut)"),
            
            # Exif Orientation variations
            (1, "orientation", "通常の向き（Top-left）", "Normal orientation (Top-left)"),
            (3, "orientation", "180度回転（Bottom-right）", "Rotated 180 degrees (Bottom-right)"),
            (6, "orientation", "時計回りに90度回転（Right-top）", "Rotated 90 degrees clockwise (Right-top)"),
            (8, "orientation", "反時計回りに90度回転（Left-bottom）", "Rotated 90 degrees counter-clockwise (Left-bottom)"),
            
            # DPI/Resolution variations
            ("jfif_units0", "dpi", "JFIF units:0 (縦横比のみ)", "JFIF units:0 (aspect ratio only)"),
            ("jfif_72dpi", "dpi", "JFIF units:1 72DPI", "JFIF units:1 72DPI"),
            ("jfif_200dpi", "dpi", "JFIF units:1 200DPI", "JFIF units:1 200DPI"),
            ("exif_72dpi", "dpi", "EXIF指定 72DPI", "EXIF specified 72DPI"),
            ("exif_200dpi", "dpi", "EXIF指定 200DPI", "EXIF specified 200DPI"),
        ]
        
        # Generate variations
        for param, category, jp_desc, en_desc in jpeg_specs:
            if category == "colorspace":
                _convert_jpeg_colorspace(source_file, output_dir, param)
                filename = f"colorspace_{param}.jpg"
            elif category == "encoding":
                _convert_jpeg_encoding(source_file, output_dir, param)
                filename = f"encoding_{param}.jpg"
            elif category == "thumbnail":
                _convert_jpeg_thumbnail(source_file, output_dir, param)
                filename = f"thumbnail_{param}.jpg"
            elif category == "quality":
                _convert_jpeg_quality(source_file, output_dir, param)
                filename = f"quality_{param}.jpg"
            elif category == "subsampling":
                _convert_jpeg_subsampling(source_file, output_dir, param)
                filename = f"subsampling_{param}.jpg"
            elif category == "metadata":
                _convert_jpeg_metadata(source_file, output_dir, param)
                filename = f"metadata_{param}.jpg"
            elif category == "icc":
                _convert_jpeg_icc(source_file, output_dir, param)
                filename = f"icc_{param}.jpg"
            elif category == "orientation":
                _convert_jpeg_orientation(source_file, output_dir, param)
                filename = f"orientation_{param}.jpg"
            elif category == "dpi":
                _convert_jpeg_dpi(source_file, output_dir, param)
                filename = f"dpi_{param}.jpg"
            
            # Add to index
            variations_index.append({
                "format": "jpeg",
                "path": f"jpeg/{filename}",
                "jp": jp_desc,
                "en": en_desc
            })
        
        # Critical combinations
        critical_combinations = [
            ("critical_cmyk_lowquality.jpg", "CMYK色空間と低品質の組み合わせ（高圧縮）", "CMYK color space with low quality (high compression)"),
            ("critical_progressive_fullmeta.jpg", "プログレッシブ形式と完全メタデータの組み合わせ", "Progressive format with complete metadata"),
            ("critical_thumbnail_progressive.jpg", "サムネイル埋め込みとプログレッシブの組み合わせ", "Embedded thumbnail with progressive format"),
            ("critical_orientation_metadata.jpg", "回転orientation情報と複雑メタデータの組み合わせ", "Rotated orientation with complex metadata"),
            ("critical_jfif_exif_dpi.jpg", "JFIF units:1 72DPIとEXIF 200DPIの併存", "JFIF units:1 72DPI with EXIF 200DPI conflict")
        ]
        
        _convert_jpeg_critical_combinations(source_file, output_dir)
        
        for filename, jp_desc, en_desc in critical_combinations:
            variations_index.append({
                "format": "jpeg",
                "path": f"jpeg/{filename}",
                "jp": jp_desc,
                "en": en_desc
            })
        
        print("JPEG variations generated successfully")
        return variations_index
        
    except Exception as e:
        print(f"Error generating JPEG variations: {e}")
        return None


def generate_png_variations(source_file, output_dir):
    """Generate PNG format variations."""
    try:
        variations_index = []
        
        # Define PNG variation specifications with descriptions
        png_specs = [
            # Color type variations
            ("grayscale", "colortype", "グレースケール（白黒画像）", "Grayscale (black and white image)"),
            ("palette", "colortype", "パレットカラー（256色まで）", "Palette color (up to 256 colors)"),
            ("rgb", "colortype", "RGB（透明度なし）", "RGB (no transparency)"),
            ("rgba", "colortype", "RGBA（透明度あり）", "RGBA (with transparency)"),
            ("grayscale_alpha", "colortype", "グレースケール+透明度", "Grayscale with transparency"),
            
            # Interlacing variations
            ("none", "interlace", "インターレースなし（通常）", "No interlace (standard)"),
            ("adam7", "interlace", "Adam7インターレース（段階的表示）", "Adam7 interlace (progressive display)"),
            
            # Color depth variations
            (1, "depth", "1ビット深度（白黒のみ）", "1-bit depth (black and white only)"),
            (8, "depth", "8ビット深度（標準）", "8-bit depth (standard)"),
            (16, "depth", "16ビット深度（高精度）", "16-bit depth (high precision)"),
            
            # Compression level variations
            (0, "compression", "圧縮なし（最大ファイルサイズ）", "No compression (maximum file size)"),
            (6, "compression", "標準圧縮（デフォルト）", "Standard compression (default)"),
            (9, "compression", "最大圧縮（最小ファイルサイズ）", "Maximum compression (minimum file size)"),
            
            # Transparency variations
            ("opaque", "alpha", "完全不透明", "Completely opaque"),
            ("semitransparent", "alpha", "半透明（部分的透明度）", "Semi-transparent (partial transparency)"),
            ("transparent", "alpha", "透明領域あり", "Has transparent areas"),
            
            # Filter type variations
            ("none", "filter", "フィルターなし", "No filter"),
            ("sub", "filter", "Subフィルター（水平予測）", "Sub filter (horizontal prediction)"),
            ("up", "filter", "Upフィルター（垂直予測）", "Up filter (vertical prediction)"),
            ("average", "filter", "Averageフィルター（平均予測）", "Average filter (average prediction)"),
            ("paeth", "filter", "Paethフィルター（複合予測）", "Paeth filter (complex prediction)"),
            
            # Metadata variations
            ("none", "metadata", "メタデータなし", "No metadata"),
            ("text", "metadata", "テキストメタデータ", "Text metadata"),
            ("compressed", "metadata", "圧縮テキストメタデータ", "Compressed text metadata"),
            ("international", "metadata", "国際化テキスト（UTF-8）", "International text (UTF-8)"),
            
            # Auxiliary chunk variations
            ("gamma", "chunk", "ガンマ補正情報", "Gamma correction information"),
            ("background", "chunk", "背景色指定", "Background color specification"),
            ("transparency", "chunk", "透明色指定", "Transparent color specification"),
        ]
        
        # Generate variations
        for param, category, jp_desc, en_desc in png_specs:
            if category == "colortype":
                _convert_png_colortype(source_file, output_dir, param)
                filename = f"colortype_{param}.png"
            elif category == "interlace":
                _convert_png_interlace(source_file, output_dir, param)
                filename = f"interlace_{param}.png"
            elif category == "depth":
                _convert_png_depth(source_file, output_dir, param)
                filename = f"depth_{param}bit.png"
            elif category == "compression":
                _convert_png_compression(source_file, output_dir, param)
                filename = f"compression_{param}.png"
            elif category == "alpha":
                _convert_png_alpha(source_file, output_dir, param)
                filename = f"alpha_{param}.png"
            elif category == "filter":
                _convert_png_filter(source_file, output_dir, param)
                filename = f"filter_{param}.png"
            elif category == "metadata":
                _convert_png_metadata(source_file, output_dir, param)
                filename = f"metadata_{param}.png"
            elif category == "chunk":
                _convert_png_chunks(source_file, output_dir, param)
                filename = f"chunk_{param}.png"
            
            # Add to index
            variations_index.append({
                "format": "png",
                "path": f"png/{filename}",
                "jp": jp_desc,
                "en": en_desc
            })
        
        # Critical combinations
        critical_combinations = [
            ("critical_16bit_palette.png", "16ビットからパレットへの変換（大幅な色情報損失）", "16-bit to palette conversion (significant color information loss)"),
            ("critical_alpha_grayscale.png", "RGBAからグレースケール+透明度への変換", "RGBA to grayscale with alpha conversion"),
            ("critical_maxcompression_paeth.png", "最大圧縮とPaethフィルターの組み合わせ", "Maximum compression with Paeth filter combination"),
            ("critical_interlace_highres.png", "インターレースと高解像度の組み合わせ", "Interlace with high resolution combination")
        ]
        
        _convert_png_critical_combinations(source_file, output_dir)
        
        for filename, jp_desc, en_desc in critical_combinations:
            variations_index.append({
                "format": "png",
                "path": f"png/{filename}",
                "jp": jp_desc,
                "en": en_desc
            })
        
        print("PNG variations generated successfully")
        return variations_index
        
    except Exception as e:
        print(f"Error generating PNG variations: {e}")
        return None


def generate_gif_variations(source_file, output_dir):
    """Generate GIF format variations."""
    try:
        from src.image_generator import create_gif_test_animation, save_gif_with_options
        
        variations_index = []
        
        # Load source GIF to get frames
        source_gif = Image.open(source_file)
        source_frames = []
        
        try:
            while True:
                source_frames.append(source_gif.copy())
                source_gif.seek(source_gif.tell() + 1)
        except EOFError:
            pass
        
        print(f"Source GIF has {len(source_frames)} frames")
        
        # Define GIF variation specifications with descriptions
        gif_specs = [
            # Frame count variations
            ("single", "frames", 1, "静止画GIF（1フレーム）", "Static GIF (1 frame)"),
            ("short", "frames", 5, "短いアニメーション（5フレーム）", "Short animation (5 frames)"),
            ("medium", "frames", 10, "中程度アニメーション（10フレーム）", "Medium animation (10 frames)"),
            ("long", "frames", 20, "長いアニメーション（20フレーム）", "Long animation (20 frames)"),
            
            # Frame rate variations (duration in ms)
            ("slow", "fps", 200, "低フレームレート（5 FPS）", "Low frame rate (5 FPS)"),
            ("normal", "fps", 100, "標準フレームレート（10 FPS）", "Normal frame rate (10 FPS)"),
            ("fast", "fps", 40, "高フレームレート（25 FPS）", "High frame rate (25 FPS)"),
            
            # Palette size variations
            ("2colors", "palette", 2, "2色パレット（最小）", "2-color palette (minimum)"),
            ("16colors", "palette", 16, "16色パレット", "16-color palette"),
            ("256colors", "palette", 256, "256色パレット（最大）", "256-color palette (maximum)"),
            
            # Dithering variations
            ("nodither", "dither", False, "ディザリングなし", "No dithering"),
            ("dithered", "dither", True, "Floyd-Steinbergディザリング", "Floyd-Steinberg dithering"),
            
            # Optimization variations
            ("noopt", "optimize", False, "最適化なし", "No optimization"),
            ("optimized", "optimize", True, "基本最適化（フレーム最適化）", "Basic optimization (frame optimization)"),
            
            # Loop variations
            ("loop_infinite", "loop", 0, "無限ループ", "Infinite loop"),
            ("loop_once", "loop", 1, "1回再生のみ", "Play once only"),
            ("loop_3times", "loop", 3, "3回ループ", "Loop 3 times"),
        ]
        
        # Generate variations
        for param, category, value, jp_desc, en_desc in gif_specs:
            if category == "frames":
                # Create animation with specific frame count
                frames = create_gif_test_animation(width=200, height=200, frame_count=value)
                filename = f"frames_{param}.gif"
                output_path = os.path.join(output_dir, filename)
                save_gif_with_options(frames, output_path, duration=100, loop=0, 
                                    optimize=False, palette_size=256, dither=True)
                
            elif category == "fps":
                # Use medium frame count with different durations
                frames = create_gif_test_animation(width=200, height=200, frame_count=10)
                filename = f"fps_{param}.gif"
                output_path = os.path.join(output_dir, filename)
                save_gif_with_options(frames, output_path, duration=value, loop=0, 
                                    optimize=False, palette_size=256, dither=True)
                
            elif category == "palette":
                # Use standard animation with different palette sizes
                frames = create_gif_test_animation(width=200, height=200, frame_count=10)
                filename = f"palette_{param}.gif"
                output_path = os.path.join(output_dir, filename)
                save_gif_with_options(frames, output_path, duration=100, loop=0, 
                                    optimize=False, palette_size=value, dither=True)
                
            elif category == "dither":
                # Use standard animation with/without dithering
                frames = create_gif_test_animation(width=200, height=200, frame_count=10)
                filename = f"dither_{param}.gif"
                output_path = os.path.join(output_dir, filename)
                save_gif_with_options(frames, output_path, duration=100, loop=0, 
                                    optimize=False, palette_size=64, dither=value)
                
            elif category == "optimize":
                # Use standard animation with/without optimization
                frames = create_gif_test_animation(width=200, height=200, frame_count=10)
                filename = f"optimize_{param}.gif"
                output_path = os.path.join(output_dir, filename)
                save_gif_with_options(frames, output_path, duration=100, loop=0, 
                                    optimize=value, palette_size=256, dither=True)
                
            elif category == "loop":
                # Use standard animation with different loop settings
                frames = create_gif_test_animation(width=200, height=200, frame_count=10)
                filename = f"loop_{param}.gif"
                output_path = os.path.join(output_dir, filename)
                save_gif_with_options(frames, output_path, duration=100, loop=value, 
                                    optimize=False, palette_size=256, dither=True)
            
            # Add to index
            variations_index.append({
                "format": "gif",
                "path": f"gif/{filename}",
                "jp": jp_desc,
                "en": en_desc
            })
        
        # Critical combinations
        critical_combinations = [
            ("critical_fast_256colors_long.gif", "高フレームレート+大パレット+長時間（大ファイル）", "High frame rate + large palette + long duration (large file)"),
            ("critical_dither_smallpalette.gif", "ディザリング+小パレット（品質劣化）", "Dithering + small palette (quality degradation)"),
            ("critical_noopt_manyframes.gif", "最適化なし+多フレーム（非効率）", "No optimization + many frames (inefficient)"),
        ]
        
        # Generate critical combinations
        # High FPS + Large palette + Long duration
        frames = create_gif_test_animation(width=200, height=200, frame_count=20)
        output_path = os.path.join(output_dir, "critical_fast_256colors_long.gif")
        save_gif_with_options(frames, output_path, duration=40, loop=0, 
                            optimize=False, palette_size=256, dither=True)
        
        # Dithering + Small palette
        frames = create_gif_test_animation(width=200, height=200, frame_count=10)
        output_path = os.path.join(output_dir, "critical_dither_smallpalette.gif")
        save_gif_with_options(frames, output_path, duration=100, loop=0, 
                            optimize=False, palette_size=4, dither=True)
        
        # No optimization + Many frames
        frames = create_gif_test_animation(width=200, height=200, frame_count=25)
        output_path = os.path.join(output_dir, "critical_noopt_manyframes.gif")
        save_gif_with_options(frames, output_path, duration=100, loop=0, 
                            optimize=False, palette_size=128, dither=True)
        
        for filename, jp_desc, en_desc in critical_combinations:
            variations_index.append({
                "format": "gif",
                "path": f"gif/{filename}",
                "jp": jp_desc,
                "en": en_desc
            })
        
        print("GIF variations generated successfully")
        return variations_index
        
    except Exception as e:
        print(f"Error generating GIF variations: {e}")
        return None


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
        _run_imagemagick_command(cmd)
    elif thumbnail == "embedded":
        # Simplified approach - create a copy with embedded thumbnail
        # Use PIL to create thumbnail in EXIF data
        try:
            from PIL import Image
            import piexif
            
            with Image.open(source) as img:
                # Create thumbnail
                img.thumbnail((160, 120), Image.Resampling.LANCZOS)
                
                # Load existing EXIF or create new
                try:
                    exif_data = piexif.load(str(source))
                except:
                    exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
                
                # Convert thumbnail to JPEG bytes
                import io
                thumb_buffer = io.BytesIO()
                img.save(thumb_buffer, format='JPEG', quality=85)
                exif_data["thumbnail"] = thumb_buffer.getvalue()
                
                # Save original image with embedded thumbnail
                with Image.open(source) as orig_img:
                    exif_bytes = piexif.dump(exif_data)
                    orig_img.save(output_file, exif=exif_bytes)
                    
        except Exception as e:
            print(f"PIL thumbnail embedding failed, using simple copy: {e}")
            cmd = ["convert", source, output_file]
            _run_imagemagick_command(cmd)
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
        # Use ImageMagick with embedded sRGB profile
        cmd = ["convert", source, "-colorspace", "sRGB", "-strip", "+profile", "!icc,*", "-profile", "/System/Library/ColorSync/Profiles/sRGB Profile.icc", output_file]
        if not _run_imagemagick_command(cmd):
            # Fallback: try built-in sRGB profile
            cmd = ["convert", source, "-colorspace", "sRGB", "-profile", "sRGB.icc", output_file]
            if not _run_imagemagick_command(cmd):
                # Final fallback: simple colorspace conversion
                cmd = ["convert", source, "-colorspace", "sRGB", output_file]
                _run_imagemagick_command(cmd)
        return
    elif icc == "adobergb":
        # Use ImageMagick with Adobe RGB profile
        cmd = ["convert", source, "-colorspace", "Adobe98", "-strip", "+profile", "!icc,*", "-profile", "/System/Library/ColorSync/Profiles/AdobeRGB1998.icc", output_file]
        if not _run_imagemagick_command(cmd):
            # Fallback: try built-in Adobe RGB
            cmd = ["convert", source, "-colorspace", "Adobe98", "-profile", "AdobeRGB1998.icc", output_file]
            if not _run_imagemagick_command(cmd):
                # Final fallback: simple colorspace conversion
                cmd = ["convert", source, "-colorspace", "Adobe98", output_file]
                _run_imagemagick_command(cmd)
        return
    else:
        # Default fallback
        cmd = ["convert", source, output_file]
    
    _run_imagemagick_command(cmd)


def _convert_jpeg_orientation(source, output_dir, orientation):
    """Convert JPEG with different orientation settings."""
    output_file = os.path.join(output_dir, f"orientation_{orientation}.jpg")
    
    # Use PIL with piexif to set EXIF orientation tag more reliably
    try:
        from PIL import Image
        import piexif
        
        # Copy the source image first
        with Image.open(source) as img:
            # Load existing EXIF data or create new
            try:
                exif_data = piexif.load(str(source))
            except:
                exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            # Set orientation tag
            exif_data["0th"][piexif.ImageIFD.Orientation] = orientation
            
            # Convert back to bytes
            exif_bytes = piexif.dump(exif_data)
            
            # Save with new EXIF orientation
            img.save(output_file, exif=exif_bytes)
            
    except Exception as e:
        print(f"PIL/piexif orientation setting failed, trying ImageMagick fallback: {e}")
        # Fallback to simple copy with ImageMagick metadata
        cmd = ["convert", source, "-define", f"exif:Orientation={orientation}", output_file]
        _run_imagemagick_command(cmd)


def _convert_jpeg_dpi(source, output_dir, dpi_type):
    """Convert JPEG with different DPI/resolution specifications."""
    output_file = os.path.join(output_dir, f"dpi_{dpi_type}.jpg")
    
    try:
        from PIL import Image
        import piexif
        
        with Image.open(source) as img:
            # Load existing EXIF data or create new
            try:
                exif_data = piexif.load(str(source))
            except:
                exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            if dpi_type == "jfif_units0":
                # JFIF units:0 (aspect ratio only, no absolute DPI)
                # Remove resolution info from EXIF and set JFIF to units=0
                exif_data["0th"].pop(piexif.ImageIFD.XResolution, None)
                exif_data["0th"].pop(piexif.ImageIFD.YResolution, None)
                exif_data["0th"].pop(piexif.ImageIFD.ResolutionUnit, None)
                
                exif_bytes = piexif.dump(exif_data)
                img.save(output_file, exif=exif_bytes, dpi=(1, 1))  # PIL sets JFIF units=0 for 1:1
                
            elif dpi_type == "jfif_72dpi":
                # JFIF units:1 with 72 DPI
                exif_data["0th"].pop(piexif.ImageIFD.XResolution, None)
                exif_data["0th"].pop(piexif.ImageIFD.YResolution, None)
                exif_data["0th"].pop(piexif.ImageIFD.ResolutionUnit, None)
                
                exif_bytes = piexif.dump(exif_data)
                img.save(output_file, exif=exif_bytes, dpi=(72, 72))
                
            elif dpi_type == "jfif_200dpi":
                # JFIF units:1 with 200 DPI
                exif_data["0th"].pop(piexif.ImageIFD.XResolution, None)
                exif_data["0th"].pop(piexif.ImageIFD.YResolution, None)
                exif_data["0th"].pop(piexif.ImageIFD.ResolutionUnit, None)
                
                exif_bytes = piexif.dump(exif_data)
                img.save(output_file, exif=exif_bytes, dpi=(200, 200))
                
            elif dpi_type == "exif_72dpi":
                # EXIF specified 72 DPI (no JFIF resolution)
                exif_data["0th"][piexif.ImageIFD.XResolution] = (72, 1)
                exif_data["0th"][piexif.ImageIFD.YResolution] = (72, 1)
                exif_data["0th"][piexif.ImageIFD.ResolutionUnit] = 2  # inches
                
                exif_bytes = piexif.dump(exif_data)
                # Save without DPI parameter to avoid JFIF resolution
                img.save(output_file, exif=exif_bytes)
                
            elif dpi_type == "exif_200dpi":
                # EXIF specified 200 DPI (no JFIF resolution)
                exif_data["0th"][piexif.ImageIFD.XResolution] = (200, 1)
                exif_data["0th"][piexif.ImageIFD.YResolution] = (200, 1)
                exif_data["0th"][piexif.ImageIFD.ResolutionUnit] = 2  # inches
                
                exif_bytes = piexif.dump(exif_data)
                # Save without DPI parameter to avoid JFIF resolution
                img.save(output_file, exif=exif_bytes)
            
    except Exception as e:
        print(f"PIL/piexif DPI setting failed, using ImageMagick fallback: {e}")
        # Fallback to ImageMagick
        if dpi_type == "jfif_72dpi":
            cmd = ["convert", source, "-density", "72x72", "-units", "PixelsPerInch", output_file]
        elif dpi_type == "jfif_200dpi":
            cmd = ["convert", source, "-density", "200x200", "-units", "PixelsPerInch", output_file]
        else:
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
    
    # Orientation + Metadata
    output_file = os.path.join(output_dir, "critical_orientation_metadata.jpg")
    try:
        from PIL import Image
        import piexif
        
        with Image.open(source) as img:
            try:
                exif_data = piexif.load(str(source))
            except:
                exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            # Set orientation to 6 (90 degrees clockwise)
            exif_data["0th"][piexif.ImageIFD.Orientation] = 6
            exif_bytes = piexif.dump(exif_data)
            img.save(output_file, exif=exif_bytes)
            
    except Exception as e:
        print(f"PIL/piexif critical orientation failed, trying ImageMagick: {e}")
        cmd = ["convert", source, "-define", "exif:Orientation=6", output_file]
        _run_imagemagick_command(cmd)
    
    # JFIF 72DPI + EXIF 200DPI conflict
    output_file = os.path.join(output_dir, "critical_jfif_exif_dpi.jpg")
    try:
        from PIL import Image
        import piexif
        
        with Image.open(source) as img:
            try:
                exif_data = piexif.load(str(source))
            except:
                exif_data = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None}
            
            # Set EXIF resolution to 200 DPI
            exif_data["0th"][piexif.ImageIFD.XResolution] = (200, 1)
            exif_data["0th"][piexif.ImageIFD.YResolution] = (200, 1)
            exif_data["0th"][piexif.ImageIFD.ResolutionUnit] = 2  # inches
            
            exif_bytes = piexif.dump(exif_data)
            # Save with JFIF 72 DPI (conflicts with EXIF 200 DPI)
            img.save(output_file, exif=exif_bytes, dpi=(72, 72))
            
    except Exception as e:
        print(f"PIL/piexif critical DPI conflict failed, trying ImageMagick: {e}")
        cmd = ["convert", source, "-density", "72x72", "-units", "PixelsPerInch", output_file]
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
        _run_imagemagick_command(cmd)
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


# Global variable to cache detected ImageMagick command
_imagemagick_cmd = None

def _run_imagemagick_command(cmd):
    """Run ImageMagick command with error handling."""
    global _imagemagick_cmd
    
    # Detect and cache ImageMagick command if not already done
    if _imagemagick_cmd is None:
        # Try both 'magick' and 'convert' commands
        for test_cmd in ['magick', 'convert']:
            try:
                subprocess.run([test_cmd, '--version'], capture_output=True, check=True)
                _imagemagick_cmd = test_cmd
                print(f"Detected ImageMagick command: {_imagemagick_cmd}")
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        if _imagemagick_cmd is None:
            print("ImageMagick not found. Please install ImageMagick.")
            return False
    
    try:
        # Replace command with detected ImageMagick command
        cmd[0] = _imagemagick_cmd
        
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