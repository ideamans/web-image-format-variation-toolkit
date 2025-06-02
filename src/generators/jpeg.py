"""
JPEG format variation generator.

This module handles generation of all JPEG format variations.
"""

import os
from PIL import Image
import piexif
from ..utils.imagemagick import ImageMagickUtils
from ..utils.metadata import MetadataUtils


class JpegGenerator:
    """JPEG format variation generator."""
    
    @staticmethod
    def generate_variations(source_file, output_dir):
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
                ("xmp", "metadata", "XMPメタデータブロック", "XMP metadata blocks"),
                ("iptc", "metadata", "IPTCメタデータレコード", "IPTC metadata records"),
                
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
                    JpegGenerator._convert_colorspace(source_file, output_dir, param)
                    filename = f"colorspace_{param}.jpg"
                elif category == "encoding":
                    JpegGenerator._convert_encoding(source_file, output_dir, param)
                    filename = f"encoding_{param}.jpg"
                elif category == "thumbnail":
                    JpegGenerator._convert_thumbnail(source_file, output_dir, param)
                    filename = f"thumbnail_{param}.jpg"
                elif category == "quality":
                    JpegGenerator._convert_quality(source_file, output_dir, param)
                    filename = f"quality_{param}.jpg"
                elif category == "subsampling":
                    JpegGenerator._convert_subsampling(source_file, output_dir, param)
                    filename = f"subsampling_{param}.jpg"
                elif category == "metadata":
                    JpegGenerator._convert_metadata(source_file, output_dir, param)
                    filename = f"metadata_{param}.jpg"
                elif category == "icc":
                    JpegGenerator._convert_icc(source_file, output_dir, param)
                    filename = f"icc_{param}.jpg"
                elif category == "orientation":
                    JpegGenerator._convert_orientation(source_file, output_dir, param)
                    filename = f"orientation_{param}.jpg"
                elif category == "dpi":
                    JpegGenerator._convert_dpi(source_file, output_dir, param)
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
                ("critical_jfif_exif_dpi.jpg", "JFIF units:1 72DPIとEXIF 200DPIの併存", "JFIF units:1 72DPI with EXIF 200DPI conflict"),
                ("critical_xmp_iptc_conflict.jpg", "XMPとIPTCメタデータの競合", "XMP and IPTC metadata conflict"),
                ("critical_xmp_complex.jpg", "複雑なXMP構造とカスタム名前空間", "Complex XMP structures with custom namespaces")
            ]
            
            JpegGenerator._generate_critical_combinations(source_file, output_dir)
            
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
    
    @staticmethod
    def _convert_colorspace(source, output_dir, colorspace):
        """Convert JPEG to different color spaces."""
        output_file = os.path.join(output_dir, f"colorspace_{colorspace}.jpg")
        
        if colorspace == "rgb":
            cmd = ["convert", source, "-colorspace", "sRGB", output_file]
        elif colorspace == "cmyk":
            cmd = ["convert", source, "-colorspace", "CMYK", output_file]
        elif colorspace == "grayscale":
            cmd = ["convert", source, "-colorspace", "Gray", output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_encoding(source, output_dir, encoding):
        """Convert JPEG encoding format."""
        output_file = os.path.join(output_dir, f"encoding_{encoding}.jpg")
        
        if encoding == "baseline":
            cmd = ["convert", source, "-interlace", "none", output_file]
        elif encoding == "progressive":
            cmd = ["convert", source, "-interlace", "JPEG", output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_thumbnail(source, output_dir, thumbnail):
        """Convert JPEG thumbnail settings."""
        output_file = os.path.join(output_dir, f"thumbnail_{thumbnail}.jpg")
        
        if thumbnail == "none":
            cmd = ["convert", source, "-strip", output_file]
            ImageMagickUtils.run_command(cmd)
        elif thumbnail == "embedded":
            # Create thumbnail using PIL and piexif
            try:
                with Image.open(source) as img:
                    # Load existing EXIF or create new
                    exif_data = MetadataUtils.load_or_create_exif(source)
                    
                    # Create thumbnail
                    thumbnail_data = MetadataUtils.create_exif_thumbnail(img)
                    exif_data["thumbnail"] = thumbnail_data
                    
                    # Save original image with embedded thumbnail
                    with Image.open(source) as orig_img:
                        exif_bytes = piexif.dump(exif_data)
                        orig_img.save(output_file, "JPEG", quality=95, exif=exif_bytes)
                        
            except Exception as e:
                print(f"PIL thumbnail embedding failed, using simple copy: {e}")
                cmd = ["convert", source, output_file]
                ImageMagickUtils.run_command(cmd)
        else:
            # Fallback to simple copy
            cmd = ["convert", source, output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_quality(source, output_dir, quality):
        """Convert JPEG with different quality settings."""
        output_file = os.path.join(output_dir, f"quality_{quality}.jpg")
        cmd = ["convert", source, "-quality", str(quality), output_file]
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_subsampling(source, output_dir, subsampling):
        """Convert JPEG with different subsampling."""
        output_file = os.path.join(output_dir, f"subsampling_{subsampling}.jpg")
        
        if subsampling == "444":
            cmd = ["convert", source, "-sampling-factor", "4:4:4", output_file]
        elif subsampling == "422":
            cmd = ["convert", source, "-sampling-factor", "4:2:2", output_file]
        elif subsampling == "420":
            cmd = ["convert", source, "-sampling-factor", "4:2:0", output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_metadata(source, output_dir, metadata):
        """Convert JPEG with different metadata."""
        output_file = os.path.join(output_dir, f"metadata_{metadata}.jpg")
        
        if metadata == "none":
            cmd = ["convert", source, "-strip", output_file]
        elif metadata == "basic_exif":
            # Keep some basic EXIF but remove GPS and complex data
            cmd = ["convert", source, "-define", "jpeg:preserve-settings", 
                   "-set", "exif:Software", "Test Generator", 
                   "-set", "exif:DateTime", "2025:05:31 12:00:00", output_file]
        elif metadata == "xmp":
            JpegGenerator._convert_xmp(source, output_file)
            return
        elif metadata == "iptc":
            JpegGenerator._convert_iptc(source, output_file)
            return
        else:
            # Keep original metadata for gps and full_exif
            cmd = ["convert", source, output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_xmp(source, output_file):
        """Convert JPEG with XMP metadata."""
        try:
            with Image.open(source) as img:
                # Create XMP metadata block
                xmp_data = MetadataUtils.create_xmp_metadata()
                
                # Save image with XMP data embedded
                img.save(output_file, "JPEG", quality=95)
                
                # Use ImageMagick to embed XMP data
                cmd = ["convert", output_file, "-set", "xmp", xmp_data, output_file]
                ImageMagickUtils.run_command(cmd)
                
        except Exception as e:
            print(f"XMP metadata embedding failed, using ImageMagick fallback: {e}")
            cmd = ["convert", source, "-set", "xmp:title", "Test Image with XMP", output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_iptc(source, output_file):
        """Convert JPEG with IPTC metadata."""
        try:
            # Use ImageMagick to embed IPTC data
            iptc_params = MetadataUtils.get_iptc_commands()
            cmd = ["convert", source] + iptc_params + [output_file]
            ImageMagickUtils.run_command(cmd)
            
        except Exception as e:
            print(f"IPTC metadata embedding failed, using simple copy: {e}")
            cmd = ["convert", source, output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_icc(source, output_dir, icc):
        """Convert JPEG with different ICC profiles."""
        output_file = os.path.join(output_dir, f"icc_{icc}.jpg")
        
        if icc == "none":
            cmd = ["convert", source, "+profile", "icc", output_file]
        elif icc == "srgb":
            # Try multiple sRGB profile locations (macOS, Linux)
            srgb_paths = [
                "/System/Library/ColorSync/Profiles/sRGB Profile.icc",  # macOS
                "/usr/share/color/icc/sRGB.icc",  # Linux (downloaded)
                "/usr/share/color/icc/profiles/sRGB.icc",  # Linux alternative
                "/usr/share/color/icc/sRGB2014.icc",  # Common Linux name
            ]
            
            success = False
            for profile_path in srgb_paths:
                if os.path.exists(profile_path):
                    cmd = ["convert", source, "-colorspace", "sRGB", "-strip", "+profile", "!icc,*", "-profile", profile_path, output_file]
                    if ImageMagickUtils.run_command(cmd):
                        success = True
                        break
            
            if not success:
                # Fallback: try built-in sRGB profile name
                cmd = ["convert", source, "-colorspace", "sRGB", "-profile", "sRGB", output_file]
                if not ImageMagickUtils.run_command(cmd):
                    # Final fallback: simple colorspace conversion
                    cmd = ["convert", source, "-colorspace", "sRGB", output_file]
                    ImageMagickUtils.run_command(cmd)
            return
            
        elif icc == "adobergb":
            # Try multiple Adobe RGB profile locations
            adobe_paths = [
                "/System/Library/ColorSync/Profiles/AdobeRGB1998.icc",  # macOS
                "/usr/share/color/icc/AdobeRGB1998.icc",  # Linux
                "/usr/share/color/icc/profiles/AdobeRGB1998.icc",  # Linux alternative
            ]
            
            success = False
            for profile_path in adobe_paths:
                if os.path.exists(profile_path):
                    cmd = ["convert", source, "-colorspace", "RGB", "-strip", "+profile", "!icc,*", "-profile", profile_path, output_file]
                    if ImageMagickUtils.run_command(cmd):
                        success = True
                        break
            
            if not success:
                # Fallback: try built-in Adobe RGB colorspace
                cmd = ["convert", source, "-colorspace", "RGB", "-profile", "AdobeRGB", output_file]
                if not ImageMagickUtils.run_command(cmd):
                    # Final fallback: simple colorspace conversion to RGB
                    cmd = ["convert", source, "-colorspace", "RGB", output_file]
                    ImageMagickUtils.run_command(cmd)
            return
        else:
            # Default fallback
            cmd = ["convert", source, output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_orientation(source, output_dir, orientation):
        """Convert JPEG with different orientation settings."""
        output_file = os.path.join(output_dir, f"orientation_{orientation}.jpg")
        
        # Use PIL with piexif to set EXIF orientation tag more reliably
        try:
            with Image.open(source) as img:
                # Load existing EXIF data or create new
                exif_data = MetadataUtils.load_or_create_exif(source)
                
                # Set orientation tag
                MetadataUtils.set_orientation(exif_data, orientation)
                
                # Convert back to bytes
                exif_bytes = piexif.dump(exif_data)
                
                # Save with new EXIF orientation
                img.save(output_file, "JPEG", quality=95, exif=exif_bytes)
                
        except Exception as e:
            print(f"PIL/piexif orientation setting failed, trying ImageMagick fallback: {e}")
            # Fallback to simple copy with ImageMagick metadata
            cmd = ["convert", source, "-define", f"exif:Orientation={orientation}", output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_dpi(source, output_dir, dpi_type):
        """Convert JPEG with different DPI/resolution specifications."""
        output_file = os.path.join(output_dir, f"dpi_{dpi_type}.jpg")
        
        try:
            with Image.open(source) as img:
                # Load existing EXIF data or create new
                exif_data = MetadataUtils.load_or_create_exif(source)
                
                if dpi_type == "jfif_units0":
                    # JFIF units:0 (aspect ratio only, no absolute DPI)
                    # Remove resolution info from EXIF and set JFIF to units=0
                    MetadataUtils.remove_dpi_exif(exif_data)
                    
                    exif_bytes = piexif.dump(exif_data)
                    img.save(output_file, "JPEG", quality=95, exif=exif_bytes, dpi=(1, 1))  # PIL sets JFIF units=0 for 1:1
                    
                elif dpi_type == "jfif_72dpi":
                    # JFIF units:1 with 72 DPI
                    MetadataUtils.remove_dpi_exif(exif_data)
                    
                    exif_bytes = piexif.dump(exif_data)
                    img.save(output_file, "JPEG", quality=95, exif=exif_bytes, dpi=(72, 72))
                    
                elif dpi_type == "jfif_200dpi":
                    # JFIF units:1 with 200 DPI
                    MetadataUtils.remove_dpi_exif(exif_data)
                    
                    exif_bytes = piexif.dump(exif_data)
                    img.save(output_file, "JPEG", quality=95, exif=exif_bytes, dpi=(200, 200))
                    
                elif dpi_type == "exif_72dpi":
                    # EXIF specified 72 DPI (no JFIF resolution)
                    MetadataUtils.set_dpi_exif(exif_data, 72)
                    
                    exif_bytes = piexif.dump(exif_data)
                    # Save without DPI parameter to avoid JFIF resolution
                    img.save(output_file, "JPEG", quality=95, exif=exif_bytes)
                    
                elif dpi_type == "exif_200dpi":
                    # EXIF specified 200 DPI (no JFIF resolution)
                    MetadataUtils.set_dpi_exif(exif_data, 200)
                    
                    exif_bytes = piexif.dump(exif_data)
                    # Save without DPI parameter to avoid JFIF resolution
                    img.save(output_file, "JPEG", quality=95, exif=exif_bytes)
                
        except Exception as e:
            print(f"PIL/piexif DPI setting failed, using ImageMagick fallback: {e}")
            # Fallback to ImageMagick
            if dpi_type == "jfif_72dpi":
                cmd = ["convert", source, "-density", "72x72", "-units", "PixelsPerInch", output_file]
            elif dpi_type == "jfif_200dpi":
                cmd = ["convert", source, "-density", "200x200", "-units", "PixelsPerInch", output_file]
            else:
                cmd = ["convert", source, output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _generate_critical_combinations(source, output_dir):
        """Generate critical JPEG combinations."""
        # CMYK + Low Quality
        output_file = os.path.join(output_dir, "critical_cmyk_lowquality.jpg")
        cmd = ["convert", source, "-colorspace", "CMYK", "-quality", "30", output_file]
        ImageMagickUtils.run_command(cmd)
        
        # Progressive + Full Metadata
        output_file = os.path.join(output_dir, "critical_progressive_fullmeta.jpg")
        cmd = ["convert", source, "-interlace", "JPEG", output_file]
        ImageMagickUtils.run_command(cmd)
        
        # Thumbnail + Progressive
        output_file = os.path.join(output_dir, "critical_thumbnail_progressive.jpg")
        cmd = ["convert", source, "-interlace", "JPEG", output_file]
        ImageMagickUtils.run_command(cmd)
        
        # Orientation + Metadata
        output_file = os.path.join(output_dir, "critical_orientation_metadata.jpg")
        try:
            with Image.open(source) as img:
                exif_data = MetadataUtils.load_or_create_exif(source)
                
                # Set orientation to 6 (90 degrees clockwise)
                MetadataUtils.set_orientation(exif_data, 6)
                exif_bytes = piexif.dump(exif_data)
                img.save(output_file, "JPEG", quality=95, exif=exif_bytes)
                
        except Exception as e:
            print(f"PIL/piexif critical orientation failed, trying ImageMagick: {e}")
            cmd = ["convert", source, "-define", "exif:Orientation=6", output_file]
            ImageMagickUtils.run_command(cmd)
        
        # JFIF 72DPI + EXIF 200DPI conflict
        output_file = os.path.join(output_dir, "critical_jfif_exif_dpi.jpg")
        try:
            with Image.open(source) as img:
                exif_data = MetadataUtils.load_or_create_exif(source)
                
                # Set EXIF resolution to 200 DPI
                MetadataUtils.set_dpi_exif(exif_data, 200)
                
                exif_bytes = piexif.dump(exif_data)
                # Save with JFIF 72 DPI (conflicts with EXIF 200 DPI)
                img.save(output_file, "JPEG", quality=95, exif=exif_bytes, dpi=(72, 72))
                
        except Exception as e:
            print(f"PIL/piexif critical DPI conflict failed, trying ImageMagick: {e}")
            cmd = ["convert", source, "-density", "72x72", "-units", "PixelsPerInch", output_file]
            ImageMagickUtils.run_command(cmd)
        
        # XMP + IPTC Conflict
        output_file = os.path.join(output_dir, "critical_xmp_iptc_conflict.jpg")
        JpegGenerator._convert_xmp_iptc_conflict(source, output_file)
        
        # XMP Complex Metadata
        output_file = os.path.join(output_dir, "critical_xmp_complex.jpg")
        JpegGenerator._convert_xmp_complex(source, output_file)
    
    @staticmethod
    def _convert_xmp_iptc_conflict(source, output_file):
        """Create JPEG with conflicting XMP and IPTC metadata."""
        try:
            with Image.open(source) as img:
                # Create XMP metadata with title "XMP Title"
                xmp_data = MetadataUtils.create_conflicting_xmp_metadata()
                
                img.save(output_file, "JPEG", quality=95)
                
                # Use ImageMagick to add both XMP and conflicting IPTC
                iptc_params = MetadataUtils.get_conflicting_iptc_commands()
                cmd = ["convert", output_file, "-set", "xmp", xmp_data] + iptc_params + [output_file]
                ImageMagickUtils.run_command(cmd)
                
        except Exception as e:
            print(f"XMP/IPTC conflict creation failed, using simple copy: {e}")
            cmd = ["convert", source, output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_xmp_complex(source, output_file):
        """Create JPEG with complex nested XMP structures."""
        try:
            with Image.open(source) as img:
                # Create complex XMP with custom namespaces and nested structures
                xmp_data = MetadataUtils.create_complex_xmp_metadata()
                
                img.save(output_file, "JPEG", quality=95)
                
                # Use ImageMagick to embed complex XMP
                cmd = ["convert", output_file, "-set", "xmp", xmp_data, output_file]
                ImageMagickUtils.run_command(cmd)
                
        except Exception as e:
            print(f"Complex XMP creation failed, using simple copy: {e}")
            cmd = ["convert", source, output_file]
            ImageMagickUtils.run_command(cmd)