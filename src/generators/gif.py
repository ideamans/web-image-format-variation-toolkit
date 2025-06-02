"""
GIF format variation generator.

This module handles generation of all GIF format variations.
"""

import os
from PIL import Image
import sys
import os
# Add parent directory to path for image_generator import
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from image_generator import create_gif_test_animation, save_gif_with_options


class GifGenerator:
    """GIF format variation generator."""
    
    @staticmethod
    def generate_variations(source_file, output_dir):
        """Generate GIF format variations."""
        try:
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
            GifGenerator._generate_critical_combinations(output_dir)
            
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
    
    @staticmethod
    def _generate_critical_combinations(output_dir):
        """Generate critical GIF combinations."""
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