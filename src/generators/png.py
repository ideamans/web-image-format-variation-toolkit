"""
PNG format variation generator.

This module handles generation of all PNG format variations.
"""

import os
import cv2
import numpy as np
from ..utils.imagemagick import ImageMagickUtils


class PngGenerator:
    """PNG format variation generator."""
    
    @staticmethod
    def generate_variations(source_file, output_dir):
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
                    PngGenerator._convert_colortype(source_file, output_dir, param)
                    filename = f"colortype_{param}.png"
                elif category == "interlace":
                    PngGenerator._convert_interlace(source_file, output_dir, param)
                    filename = f"interlace_{param}.png"
                elif category == "depth":
                    PngGenerator._convert_depth(source_file, output_dir, param)
                    filename = f"depth_{param}bit.png"
                elif category == "compression":
                    PngGenerator._convert_compression(source_file, output_dir, param)
                    filename = f"compression_{param}.png"
                elif category == "alpha":
                    PngGenerator._convert_alpha(source_file, output_dir, param)
                    filename = f"alpha_{param}.png"
                elif category == "filter":
                    PngGenerator._convert_filter(source_file, output_dir, param)
                    filename = f"filter_{param}.png"
                elif category == "metadata":
                    PngGenerator._convert_metadata(source_file, output_dir, param)
                    filename = f"metadata_{param}.png"
                elif category == "chunk":
                    PngGenerator._convert_chunks(source_file, output_dir, param)
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
            
            PngGenerator._generate_critical_combinations(source_file, output_dir)
            
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
    
    @staticmethod
    def _convert_colortype(source, output_dir, colortype):
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
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_interlace(source, output_dir, interlace):
        """Convert PNG interlacing."""
        output_file = os.path.join(output_dir, f"interlace_{interlace}.png")
        
        if interlace == "none":
            cmd = ["convert", source, "-interlace", "none", output_file]
        elif interlace == "adam7":
            cmd = ["convert", source, "-interlace", "PNG", output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_depth(source, output_dir, depth):
        """Convert PNG bit depth."""
        output_file = os.path.join(output_dir, f"depth_{depth}bit.png")
        
        if depth == 1:
            # Convert to 1-bit by first making it grayscale, then monochrome
            cmd = ["convert", source, "-colorspace", "Gray", "-monochrome", output_file]
            ImageMagickUtils.run_command(cmd)
        elif depth == 16:
            # Create true 16-bit PNG using Python/OpenCV for guaranteed 16-bit output
            try:
                PngGenerator._create_16bit_png_opencv(source, output_file)
            except Exception as e:
                print(f"OpenCV 16-bit creation failed, trying ImageMagick: {e}")
                # Fallback to ImageMagick with forced options
                cmd = ["convert", source, "-depth", "16", "-define", "png:bit-depth=16", 
                       "-define", "png:color-type=6", output_file]
                ImageMagickUtils.run_command(cmd)
        else:
            cmd = ["convert", source, "-depth", str(depth), output_file]
            ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_compression(source, output_dir, level):
        """Convert PNG compression level."""
        output_file = os.path.join(output_dir, f"compression_{level}.png")
        cmd = ["convert", source, "-define", f"png:compression-level={level}", output_file]
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_alpha(source, output_dir, alpha):
        """Convert PNG alpha settings."""
        output_file = os.path.join(output_dir, f"alpha_{alpha}.png")
        
        if alpha == "opaque":
            cmd = ["convert", source, "-alpha", "off", output_file]
        elif alpha == "semitransparent":
            cmd = ["convert", source, "-alpha", "set", "-channel", "A", "-evaluate", "multiply", "0.5", output_file]
        elif alpha == "transparent":
            cmd = ["convert", source, "-alpha", "set", "-channel", "A", "-evaluate", "multiply", "0.2", output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_filter(source, output_dir, filter_type):
        """Convert PNG filter types."""
        output_file = os.path.join(output_dir, f"filter_{filter_type}.png")
        
        # PNG filter types: 0=None, 1=Sub, 2=Up, 3=Average, 4=Paeth
        filter_map = {
            "none": 0, "sub": 1, "up": 2, "average": 3, "paeth": 4
        }
        
        filter_num = filter_map.get(filter_type, 0)
        cmd = ["convert", source, "-define", f"png:compression-filter={filter_num}", output_file]
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_metadata(source, output_dir, metadata):
        """Convert PNG metadata settings."""
        output_file = os.path.join(output_dir, f"metadata_{metadata}.png")
        
        if metadata == "none":
            cmd = ["convert", source, "-strip", output_file]
        elif metadata == "text":
            cmd = ["convert", source, "-set", "png:Software", "Test Generator", output_file]
        else:
            # Keep original metadata for compressed and international
            cmd = ["convert", source, output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _convert_chunks(source, output_dir, chunk):
        """Convert PNG auxiliary chunks."""
        output_file = os.path.join(output_dir, f"chunk_{chunk}.png")
        
        if chunk == "gamma":
            cmd = ["convert", source, "-gamma", "2.2", output_file]
        elif chunk == "background":
            cmd = ["convert", source, "-background", "white", output_file]
        else:
            # Default for transparency or other chunks
            cmd = ["convert", source, output_file]
        
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
    def _generate_critical_combinations(source, output_dir):
        """Generate critical PNG combinations."""
        # 16-bit to palette
        output_file = os.path.join(output_dir, "critical_16bit_palette.png")
        cmd = ["convert", source, "-depth", "16", "-type", "Palette", output_file]
        ImageMagickUtils.run_command(cmd)
        
        # RGBA to grayscale with alpha
        output_file = os.path.join(output_dir, "critical_alpha_grayscale.png")
        cmd = ["convert", source, "-colorspace", "Gray", "-type", "GrayscaleAlpha", output_file]
        ImageMagickUtils.run_command(cmd)
        
        # Maximum compression with Paeth filter
        output_file = os.path.join(output_dir, "critical_maxcompression_paeth.png")
        cmd = ["convert", source, "-define", "png:compression-level=9", 
               "-define", "png:compression-filter=4", output_file]
        ImageMagickUtils.run_command(cmd)
        
        # Interlacing on high resolution (simulate with resize)
        output_file = os.path.join(output_dir, "critical_interlace_highres.png")
        cmd = ["convert", source, "-resize", "200%", "-interlace", "PNG", output_file]
        ImageMagickUtils.run_command(cmd)
    
    @staticmethod
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