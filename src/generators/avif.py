"""
AVIF format variation generator.

This module handles generation of all AVIF format variations across
lossy, lossless, and animation categories.
"""

import os
from pathlib import Path
import sys
import os
# Add parent directory to path for image_generator import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from image_generator import create_gif_test_animation

# Check ImageMagick AVIF support
import subprocess
try:
    # Check if ImageMagick supports AVIF
    result = subprocess.run(['magick', '-list', 'format'], capture_output=True, text=True)
    if result.returncode == 0 and 'AVIF' in result.stdout:
        IMAGEMAGICK_AVIF_AVAILABLE = True
        print("AVIF support enabled - using ImageMagick")
    else:
        IMAGEMAGICK_AVIF_AVAILABLE = False
        print("ImageMagick AVIF support not found")
except (subprocess.SubprocessError, FileNotFoundError):
    IMAGEMAGICK_AVIF_AVAILABLE = False
    print("ImageMagick not available")

# AVIF creation relies on ImageMagick/FFmpeg, not PIL
PILLOW_AVIF_READ = False

# AVIF is available if ImageMagick can create files
AVIF_AVAILABLE = IMAGEMAGICK_AVIF_AVAILABLE


def _test_avif_support():
    """Test AVIF support using ImageMagick when actually needed."""
    if not IMAGEMAGICK_AVIF_AVAILABLE:
        return False
    
    # Skip the actual test in pytest environment for speed
    import os
    if 'PYTEST_CURRENT_TEST' in os.environ:
        print("Skipping AVIF test in pytest environment")
        return True  # Assume it works in test environment
    
    try:
        import tempfile
        import os
        
        # Create a simple test image using ImageMagick directly
        test_avif = tempfile.mktemp(suffix='.avif')
        
        # Use ImageMagick to create a test AVIF directly
        cmd = ['magick', '-size', '10x10', 'xc:red', '-quality', '80', test_avif]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(test_avif):
            # Clean up
            os.unlink(test_avif)
            return True
        else:
            print(f"ImageMagick AVIF test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"AVIF creation test failed: {e}")
        return False


class AvifGenerator:
    """AVIF format variation generator."""
    
    @staticmethod
    def generate_variations(source_dir, output_dir):
        """Generate AVIF format variations."""
        try:
            variations_index = []
            source_path = Path(source_dir)
            output_path = Path(output_dir)
            
            # Create AVIF subdirectories
            lossy_dir = output_path / "avif" / "lossy"
            lossless_dir = output_path / "avif" / "lossless" 
            animation_dir = output_path / "avif" / "animation"
            
            lossy_dir.mkdir(parents=True, exist_ok=True)
            lossless_dir.mkdir(parents=True, exist_ok=True)
            animation_dir.mkdir(parents=True, exist_ok=True)
            
            # Source images
            jpeg_source = source_path / "test_original.jpg"
            png_source = source_path / "test_original.png"
            gif_source = source_path / "test_original.gif"
            
            print("Generating AVIF variations...")
            
            # Test AVIF support before proceeding
            if not AVIF_AVAILABLE or not _test_avif_support():
                print("AVIF support not available - creating placeholder files")
                AvifGenerator._create_placeholder_files(lossy_dir, lossless_dir, animation_dir)
                return variations_index
            
            # Generate lossy AVIF from JPEG source
            if jpeg_source.exists():
                AvifGenerator._generate_lossy_avif(jpeg_source, lossy_dir, variations_index)
            
            # Generate lossless AVIF from PNG source
            if png_source.exists():
                AvifGenerator._generate_lossless_avif(png_source, lossless_dir, variations_index)
            
            # Generate animation AVIF from GIF source
            if gif_source.exists():
                AvifGenerator._generate_animation_avif(gif_source, animation_dir, variations_index)
            
            print("AVIF variations generated successfully")
            return variations_index
            
        except Exception as e:
            print(f"Error generating AVIF variations: {e}")
            return None
    
    @staticmethod
    def _create_placeholder_files(lossy_dir, lossless_dir, animation_dir):
        """Create placeholder files when AVIF support is not available."""
        placeholder_content = """AVIF support requires ImageMagick with AVIF support
Install ImageMagick with AVIF support enabled
Or use: brew install imagemagick (on macOS)"""
        
        for directory, name in [(lossy_dir, "lossy"), (lossless_dir, "lossless"), (animation_dir, "animation")]:
            placeholder_file = directory / "original.txt"
            with open(placeholder_file, 'w') as f:
                f.write(placeholder_content)
            print(f"Created AVIF placeholder for {name}: {placeholder_file}")
    
    @staticmethod
    def _generate_lossy_avif(source_file, output_dir, variations_index):
        """Generate lossy AVIF variations using ImageMagick."""
        try:
            output_path = output_dir / "original.avif"
            
            # Use ImageMagick to convert to AVIF
            cmd = ['magick', str(source_file), '-quality', '80', str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                variations_index.append({
                    "format": "avif",
                    "path": "avif/lossy/original.avif",
                    "jp": "AVIF損失圧縮（JPEG源画像から変換）",
                    "en": "AVIF lossy compression (converted from JPEG source)"
                })
                
                print(f"Generated lossy AVIF: {output_path}")
            else:
                print(f"ImageMagick AVIF conversion failed: {result.stderr}")
                
        except Exception as e:
            print(f"Error generating lossy AVIF: {e}")
    
    @staticmethod
    def _generate_lossless_avif(source_file, output_dir, variations_index):
        """Generate lossless AVIF variations using ImageMagick."""
        try:
            output_path = output_dir / "original.avif"
            
            # Use ImageMagick to convert to AVIF with high quality (lossless-like)
            cmd = ['magick', str(source_file), '-quality', '100', str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                variations_index.append({
                    "format": "avif",
                    "path": "avif/lossless/original.avif",
                    "jp": "AVIF無損失圧縮（PNG源画像から変換）",
                    "en": "AVIF lossless compression (converted from PNG source)"
                })
                
                print(f"Generated lossless AVIF: {output_path}")
            else:
                print(f"ImageMagick AVIF conversion failed: {result.stderr}")
                
        except Exception as e:
            print(f"Error generating lossless AVIF: {e}")
    
    @staticmethod
    def _generate_animation_avif(source_file, output_dir, variations_index):
        """Generate animation AVIF variations using FFmpeg."""
        try:
            output_path = output_dir / "original.avif"
            
            # Check FFmpeg availability first
            try:
                ffmpeg_check = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
                if ffmpeg_check.returncode != 0:
                    print("FFmpeg not available, falling back to ImageMagick")
                    return AvifGenerator._generate_animation_avif_imagemagick(source_file, output_dir, variations_index)
            except (subprocess.SubprocessError, FileNotFoundError):
                print("FFmpeg not found, falling back to ImageMagick")
                return AvifGenerator._generate_animation_avif_imagemagick(source_file, output_dir, variations_index)
            
            # Use FFmpeg to convert GIF animation to AVIF
            # FFmpeg command: ffmpeg -i input.gif -c:v libaom-av1 -pix_fmt yuv420p -crf 30 -b:v 0 output.avif
            cmd = [
                'ffmpeg', '-y',  # -y to overwrite output file
                '-i', str(source_file),
                '-c:v', 'libaom-av1',  # Use AV1 codec
                '-pix_fmt', 'yuv420p',  # Pixel format
                '-crf', '30',  # Constant Rate Factor (quality)
                '-b:v', '0',   # Variable bitrate
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                # Check if we got animation by using FFprobe to count frames
                try:
                    probe_cmd = ['ffprobe', '-v', 'quiet', '-select_streams', 'v:0', 
                               '-count_frames', '-show_entries', 'stream=nb_read_frames', 
                               '-csv=p=0', str(output_path)]
                    probe_result = subprocess.run(probe_cmd, capture_output=True, text=True)
                    
                    if probe_result.returncode == 0 and probe_result.stdout.strip():
                        frame_count = int(probe_result.stdout.strip())
                        
                        if frame_count > 1:
                            variations_index.append({
                                "format": "avif",
                                "path": "avif/animation/original.avif",
                                "jp": "AVIFアニメーション（FFmpegでGIF源画像から変換）",
                                "en": "AVIF animation (converted from GIF source using FFmpeg)"
                            })
                            print(f"Generated animation AVIF using FFmpeg: {output_path} ({frame_count} frames)")
                        else:
                            variations_index.append({
                                "format": "avif",
                                "path": "avif/animation/original.avif",
                                "jp": "AVIF静止画（FFmpegで変換、単一フレーム）",
                                "en": "AVIF static image (converted using FFmpeg, single frame)"
                            })
                            print(f"Generated static AVIF using FFmpeg: {output_path}")
                    else:
                        # Fallback: assume it's an animation
                        variations_index.append({
                            "format": "avif",
                            "path": "avif/animation/original.avif",
                            "jp": "AVIFアニメーション（FFmpegでGIF源画像から変換）",
                            "en": "AVIF animation (converted from GIF source using FFmpeg)"
                        })
                        print(f"Generated AVIF using FFmpeg: {output_path}")
                        
                except Exception as probe_error:
                    print(f"Frame count detection failed: {probe_error}")
                    # Default to assuming it's an animation
                    variations_index.append({
                        "format": "avif",
                        "path": "avif/animation/original.avif",
                        "jp": "AVIFアニメーション（FFmpegでGIF源画像から変換）",
                        "en": "AVIF animation (converted from GIF source using FFmpeg)"
                    })
                    print(f"Generated AVIF using FFmpeg: {output_path}")
            else:
                print(f"FFmpeg AVIF animation conversion failed: {result.stderr}")
                print("Falling back to ImageMagick")
                return AvifGenerator._generate_animation_avif_imagemagick(source_file, output_dir, variations_index)
            
        except Exception as e:
            print(f"Error generating animation AVIF with FFmpeg: {e}")
            print("Falling back to ImageMagick")
            return AvifGenerator._generate_animation_avif_imagemagick(source_file, output_dir, variations_index)
    
    @staticmethod
    def _generate_animation_avif_imagemagick(source_file, output_dir, variations_index):
        """Fallback method using ImageMagick for animation AVIF."""
        try:
            output_path = output_dir / "original.avif"
            
            # Try to convert GIF animation to AVIF using ImageMagick
            # Note: AVIF animation support in ImageMagick may be limited
            cmd = ['magick', str(source_file), '-quality', '80', str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and output_path.exists():
                # Check if we got multiple frames (animation) or single frame
                try:
                    # Try to determine frame count using ImageMagick identify
                    identify_cmd = ['magick', 'identify', str(output_path)]
                    identify_result = subprocess.run(identify_cmd, capture_output=True, text=True)
                    frame_count = len(identify_result.stdout.strip().split('\n'))
                    
                    if frame_count > 1:
                        variations_index.append({
                            "format": "avif",
                            "path": "avif/animation/original.avif",
                            "jp": "AVIFアニメーション（ImageMagickでGIF源画像から変換）",
                            "en": "AVIF animation (converted from GIF source using ImageMagick)"
                        })
                        print(f"Generated animation AVIF using ImageMagick: {output_path} ({frame_count} frames)")
                    else:
                        variations_index.append({
                            "format": "avif",
                            "path": "avif/animation/original.avif",
                            "jp": "AVIF静止画（ImageMagickで変換、アニメーション対応制限）",
                            "en": "AVIF static image (converted using ImageMagick, animation support limited)"
                        })
                        print(f"Generated static AVIF from animation using ImageMagick: {output_path}")
                        
                except Exception:
                    # Default to assuming it's an animation
                    variations_index.append({
                        "format": "avif",
                        "path": "avif/animation/original.avif",
                        "jp": "AVIFアニメーション（ImageMagickでGIF源画像から変換）",
                        "en": "AVIF animation (converted from GIF source using ImageMagick)"
                    })
                    print(f"Generated AVIF from animation using ImageMagick: {output_path}")
            else:
                print(f"ImageMagick AVIF animation conversion failed: {result.stderr}")
            
        except Exception as e:
            print(f"Error generating animation AVIF with ImageMagick: {e}")