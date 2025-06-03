"""
Image comparison and analysis module.

This module provides functions to compare images across directories,
calculating metrics like file size, resolution, PSNR, and generating reports.
"""

import os
import json
import csv
from pathlib import Path
from PIL import Image
import numpy as np
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import pandas as pd


def compare_directories(dir_a, dir_b, output_format="table", output_file=None):
    """
    Compare identical filenames across two directories.
    
    Args:
        dir_a (str): First directory to compare
        dir_b (str): Second directory to compare
        output_format (str): Output format ('table', 'json', 'csv')
        output_file (str): Optional file to save results
    """
    path_a = Path(dir_a)
    path_b = Path(dir_b)
    
    if not path_a.exists():
        print(f"Error: Directory {dir_a} does not exist")
        return
        
    if not path_b.exists():
        print(f"Error: Directory {dir_b} does not exist")
        return
    
    # Get all image files from both directories
    files_a = _get_image_files(path_a)
    files_b = _get_image_files(path_b)
    
    # Find common files and differences
    common_files = set(files_a.keys()) & set(files_b.keys())
    only_in_a = set(files_a.keys()) - set(files_b.keys())
    only_in_b = set(files_b.keys()) - set(files_a.keys())
    
    print(f"Comparing directories:")
    print(f"  Directory A: {dir_a} ({len(files_a)} images)")
    print(f"  Directory B: {dir_b} ({len(files_b)} images)")
    print(f"  Common files: {len(common_files)}")
    print(f"  Only in A: {len(only_in_a)}")
    print(f"  Only in B: {len(only_in_b)}")
    
    # Compare common files
    comparison_results = []
    
    for filename in sorted(common_files):
        print(f"Comparing {filename}...")
        result = _compare_images(files_a[filename], files_b[filename], filename)
        comparison_results.append(result)
    
    # Generate report
    report_data = {
        'summary': {
            'dir_a': str(dir_a),
            'dir_b': str(dir_b),
            'total_files_a': len(files_a),
            'total_files_b': len(files_b),
            'common_files': len(common_files),
            'only_in_a': list(only_in_a),
            'only_in_b': list(only_in_b)
        },
        'comparisons': comparison_results
    }
    
    # Output results
    if output_format == "json":
        _output_json(report_data, output_file)
    elif output_format == "csv":
        _output_csv(comparison_results, output_file)
    else:  # table
        _output_table(report_data, output_file)


def _get_image_files(directory):
    """Get all image files in a directory."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif', '.webp', '.avif'}
    files = {}
    
    for file_path in directory.rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            # Use relative path from directory as key
            rel_path = file_path.relative_to(directory)
            files[str(rel_path)] = file_path
    
    return files


def _compare_images(image_a_path, image_b_path, filename):
    """Compare two images and return metrics."""
    result = {
        'filename': filename,
        'file_a': str(image_a_path),
        'file_b': str(image_b_path),
        'error': None
    }
    
    try:
        # Get file sizes
        result['size_a'] = image_a_path.stat().st_size
        result['size_b'] = image_b_path.stat().st_size
        result['size_diff'] = result['size_b'] - result['size_a']
        result['size_ratio'] = result['size_b'] / result['size_a'] if result['size_a'] > 0 else 0
        
        # Check if files are GIFs or AVIFs
        is_gif_a = str(image_a_path).lower().endswith('.gif')
        is_gif_b = str(image_b_path).lower().endswith('.gif')
        is_avif_a = str(image_a_path).lower().endswith('.avif')
        is_avif_b = str(image_b_path).lower().endswith('.avif')
        
        if is_gif_a and is_gif_b:
            # Handle GIF comparison
            result.update(_compare_gif_animations(image_a_path, image_b_path))
        elif is_avif_a or is_avif_b:
            # Handle AVIF comparison using ImageMagick
            result.update(_compare_avif_images(image_a_path, image_b_path))
        else:
            # Handle static image comparison with PIL
            with Image.open(image_a_path) as img_a, Image.open(image_b_path) as img_b:
                # Get resolutions
                result['resolution_a'] = f"{img_a.width}x{img_a.height}"
                result['resolution_b'] = f"{img_b.width}x{img_b.height}"
                result['resolution_match'] = (img_a.width == img_b.width and img_a.height == img_b.height)
                
                # Get color modes
                result['mode_a'] = img_a.mode
                result['mode_b'] = img_b.mode
                result['mode_match'] = img_a.mode == img_b.mode
                
                # Calculate PSNR and SSIM if possible
                if result['resolution_match']:
                    try:
                        psnr_value, ssim_value = _calculate_image_metrics(img_a, img_b)
                        result['psnr'] = psnr_value
                        result['ssim'] = ssim_value
                    except Exception as e:
                        result['psnr'] = None
                        result['ssim'] = None
                        result['metrics_error'] = str(e)
                else:
                    result['psnr'] = None
                    result['ssim'] = None
                    result['metrics_error'] = "Resolution mismatch"
                    
    except Exception as e:
        result['error'] = str(e)
        
    return result


def _calculate_image_metrics(img_a, img_b):
    """Calculate PSNR and SSIM between two images."""
    # Convert to same mode if needed
    if img_a.mode != img_b.mode:
        if img_a.mode == 'RGBA' and img_b.mode == 'RGB':
            img_a = img_a.convert('RGB')
        elif img_a.mode == 'RGB' and img_b.mode == 'RGBA':
            img_b = img_b.convert('RGB')
        elif 'L' in img_a.mode or 'L' in img_b.mode:
            img_a = img_a.convert('L')
            img_b = img_b.convert('L')
        else:
            img_a = img_a.convert('RGB')
            img_b = img_b.convert('RGB')
    
    # Convert to numpy arrays
    arr_a = np.array(img_a)
    arr_b = np.array(img_b)
    
    # Ensure same shape
    if arr_a.shape != arr_b.shape:
        raise ValueError(f"Shape mismatch: {arr_a.shape} vs {arr_b.shape}")
    
    # Calculate PSNR
    psnr_value = peak_signal_noise_ratio(arr_a, arr_b)
    
    # Calculate SSIM
    if len(arr_a.shape) == 3:  # Color image
        ssim_value = structural_similarity(arr_a, arr_b, channel_axis=2)
    else:  # Grayscale
        ssim_value = structural_similarity(arr_a, arr_b)
    
    return psnr_value, ssim_value


def _compare_gif_animations(gif_a_path, gif_b_path):
    """
    Compare two GIF animations frame by frame and return average metrics.
    
    Args:
        gif_a_path (Path): Path to first GIF file
        gif_b_path (Path): Path to second GIF file
        
    Returns:
        dict: Comparison results with average PSNR/SSIM across all frames
    """
    result = {}
    
    try:
        # Open both GIF files
        with Image.open(gif_a_path) as gif_a, Image.open(gif_b_path) as gif_b:
            # Extract all frames from both GIFs
            frames_a = _extract_gif_frames(gif_a)
            frames_b = _extract_gif_frames(gif_b)
            
            # Get basic properties
            result['frames_a'] = len(frames_a)
            result['frames_b'] = len(frames_b)
            result['frame_count_match'] = len(frames_a) == len(frames_b)
            
            # Get frame rate information
            try:
                # Get duration of first frame (in milliseconds)
                duration_a = gif_a.info.get('duration', 100)  # Default 100ms
                duration_b = gif_b.info.get('duration', 100)
                
                # Calculate FPS (frames per second)
                result['framerate_a'] = round(1000 / duration_a, 2) if duration_a > 0 else None
                result['framerate_b'] = round(1000 / duration_b, 2) if duration_b > 0 else None
                result['framerate_match'] = result['framerate_a'] == result['framerate_b']
            except:
                result['framerate_a'] = None
                result['framerate_b'] = None
                result['framerate_match'] = None
            
            if frames_a and frames_b:
                # Get resolution from first frame
                result['resolution_a'] = f"{frames_a[0].width}x{frames_a[0].height}"
                result['resolution_b'] = f"{frames_b[0].width}x{frames_b[0].height}"
                result['resolution_match'] = (frames_a[0].width == frames_b[0].width and 
                                            frames_a[0].height == frames_b[0].height)
                
                # Get color modes
                result['mode_a'] = frames_a[0].mode
                result['mode_b'] = frames_b[0].mode
                result['mode_match'] = frames_a[0].mode == frames_b[0].mode
                
                # Calculate frame-by-frame metrics if resolutions match
                if result['resolution_match'] and result['frame_count_match']:
                    psnr_values = []
                    ssim_values = []
                    
                    min_frames = min(len(frames_a), len(frames_b))
                    
                    for i in range(min_frames):
                        try:
                            frame_psnr, frame_ssim = _calculate_image_metrics(frames_a[i], frames_b[i])
                            if frame_psnr is not None:
                                # Handle infinite PSNR (identical frames)
                                if np.isinf(frame_psnr):
                                    psnr_values.append(100.0)  # Set very high value for identical frames
                                else:
                                    psnr_values.append(frame_psnr)
                            if frame_ssim is not None:
                                ssim_values.append(frame_ssim)
                        except Exception as e:
                            print(f"Warning: Failed to calculate metrics for frame {i}: {e}")
                            continue
                    
                    # Use minimum values for animation quality (worst frame determines quality)
                    if psnr_values:
                        result['psnr'] = float(np.min(psnr_values))  # Minimum PSNR (worst frame)
                        result['psnr_min'] = float(np.min(psnr_values))
                        result['psnr_max'] = float(np.max(psnr_values))
                        result['psnr_mean'] = float(np.mean(psnr_values))
                        result['psnr_std'] = float(np.std(psnr_values))
                    else:
                        result['psnr'] = None
                        
                    if ssim_values:
                        result['ssim'] = float(np.min(ssim_values))  # Minimum SSIM (worst frame)
                        result['ssim_min'] = float(np.min(ssim_values))
                        result['ssim_max'] = float(np.max(ssim_values))
                        result['ssim_mean'] = float(np.mean(ssim_values))
                        result['ssim_std'] = float(np.std(ssim_values))
                    else:
                        result['ssim'] = None
                        
                    result['frames_compared'] = len(psnr_values)
                    
                else:
                    result['psnr'] = None
                    result['ssim'] = None
                    if not result['resolution_match']:
                        result['metrics_error'] = "Resolution mismatch"
                    elif not result['frame_count_match']:
                        result['metrics_error'] = f"Frame count mismatch ({result['frames_a']} vs {result['frames_b']})"
                    else:
                        result['metrics_error'] = "Unknown error"
            else:
                result['psnr'] = None
                result['ssim'] = None
                result['metrics_error'] = "Failed to extract frames"
                
    except Exception as e:
        result['metrics_error'] = f"GIF comparison error: {str(e)}"
        result['psnr'] = None
        result['ssim'] = None
    
    return result


def _extract_gif_frames(gif_image):
    """
    Extract all frames from a GIF image.
    
    Args:
        gif_image (PIL.Image): Opened GIF image
        
    Returns:
        list: List of PIL.Image frames
    """
    frames = []
    
    try:
        # Reset to first frame
        gif_image.seek(0)
        
        while True:
            # Copy current frame
            frame = gif_image.copy()
            
            # Convert to consistent format for comparison
            if frame.mode == 'P':
                # Convert palette mode to RGBA to handle transparency
                frame = frame.convert('RGBA')
            elif frame.mode not in ('RGB', 'RGBA', 'L'):
                # Convert other modes to RGB
                frame = frame.convert('RGB')
                
            frames.append(frame)
            
            # Move to next frame
            gif_image.seek(gif_image.tell() + 1)
            
    except EOFError:
        # End of frames reached
        pass
    except Exception as e:
        print(f"Warning: Error extracting GIF frames: {e}")
        
    return frames


def _compare_avif_images(image_a_path, image_b_path):
    """Compare AVIF images using ImageMagick identify."""
    result = {}
    
    try:
        import subprocess
        
        # Get image information using ImageMagick identify
        for suffix, path in [('_a', image_a_path), ('_b', image_b_path)]:
            try:
                cmd = ['magick', 'identify', '-format', '%wx%h %m %f', str(path)]
                identify_result = subprocess.run(cmd, capture_output=True, text=True)
                
                if identify_result.returncode == 0:
                    parts = identify_result.stdout.strip().split()
                    if len(parts) >= 2:
                        resolution = parts[0]  # e.g., "640x480"
                        format_name = parts[1]  # e.g., "AVIF"
                        result[f'resolution{suffix}'] = resolution
                        result[f'format{suffix}'] = format_name
                    else:
                        result[f'resolution{suffix}'] = "unknown"
                        result[f'format{suffix}'] = "unknown"
                else:
                    result[f'resolution{suffix}'] = "error"
                    result[f'format{suffix}'] = "error"
                    
            except Exception as e:
                result[f'resolution{suffix}'] = "error"
                result[f'format{suffix}'] = "error"
        
        # Check if resolutions match
        res_a = result.get('resolution_a', '')
        res_b = result.get('resolution_b', '')
        result['resolution_match'] = (res_a == res_b and res_a != "error" and res_a != "unknown")
        
        # Set modes to AVIF for consistency
        result['mode_a'] = 'AVIF'
        result['mode_b'] = 'AVIF'
        result['mode_match'] = True
        
        # AVIF quality comparison is limited without PIL - set defaults
        result['psnr'] = None
        result['ssim'] = None
        result['quality_note'] = 'AVIF quality metrics require specialized tools'
        
    except Exception as e:
        result['error'] = f"AVIF comparison error: {str(e)}"
        result['resolution_a'] = "error"
        result['resolution_b'] = "error"
        result['resolution_match'] = False
        
    return result


def _output_table(report_data, output_file=None):
    """Output comparison results as a formatted table."""
    output_lines = []
    
    # Summary
    summary = report_data['summary']
    output_lines.append("=" * 80)
    output_lines.append("IMAGE COMPARISON REPORT")
    output_lines.append("=" * 80)
    output_lines.append(f"Directory A: {summary['dir_a']} ({summary['total_files_a']} files)")
    output_lines.append(f"Directory B: {summary['dir_b']} ({summary['total_files_b']} files)")
    output_lines.append(f"Common files: {summary['common_files']}")
    
    if summary['only_in_a']:
        output_lines.append(f"Only in A: {', '.join(summary['only_in_a'])}")
    if summary['only_in_b']:
        output_lines.append(f"Only in B: {', '.join(summary['only_in_b'])}")
    
    output_lines.append("")
    
    # Detailed comparison table
    if report_data['comparisons']:
        output_lines.append("DETAILED COMPARISON")
        output_lines.append("-" * 80)
        
        # Table header
        header = f"{'Filename':<30} {'Size A':<10} {'Size B':<10} {'Ratio':<8} {'PSNR(min)':<10} {'SSIM(min)':<10} {'Frames A':<9} {'Frames B':<9} {'FPS A':<7} {'FPS B':<7}"
        output_lines.append(header)
        output_lines.append("-" * len(header))
        
        # Table rows
        for comp in report_data['comparisons']:
            filename = comp['filename'][:29]  # Truncate long filenames
            size_a = _format_size(comp.get('size_a', 0))
            size_b = _format_size(comp.get('size_b', 0))
            ratio = f"{comp.get('size_ratio', 0):.2f}" if comp.get('size_ratio') else "N/A"
            psnr = f"{comp.get('psnr', 0):.2f}" if comp.get('psnr') else "N/A"
            ssim = f"{comp.get('ssim', 0):.3f}" if comp.get('ssim') else "N/A"
            
            # Handle GIF frame and FPS information
            frames_a_info = f"{comp.get('frames_a', 0)}" if comp.get('frames_a') is not None else "N/A"
            frames_b_info = f"{comp.get('frames_b', 0)}" if comp.get('frames_b') is not None else "N/A"
            fps_a_info = f"{comp.get('framerate_a', 0):.1f}" if comp.get('framerate_a') is not None else "N/A"
            fps_b_info = f"{comp.get('framerate_b', 0):.1f}" if comp.get('framerate_b') is not None else "N/A"
            
            row = f"{filename:<30} {size_a:<10} {size_b:<10} {ratio:<8} {psnr:<10} {ssim:<10} {frames_a_info:<9} {frames_b_info:<9} {fps_a_info:<7} {fps_b_info:<7}"
            output_lines.append(row)
            
            
            # Show errors if any
            if comp.get('error'):
                output_lines.append(f"  ERROR: {comp['error']}")
            elif comp.get('metrics_error'):
                output_lines.append(f"  METRICS ERROR: {comp['metrics_error']}")
    
    # Output to console and file
    output_text = "\n".join(output_lines)
    print(output_text)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        print(f"\nReport saved to: {output_file}")


def _output_json(report_data, output_file=None):
    """Output comparison results as JSON."""
    json_str = json.dumps(report_data, indent=2, ensure_ascii=False)
    
    print(json_str)
    
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(json_str)
        print(f"\nReport saved to: {output_file}")


def _output_csv(comparison_results, output_file=None):
    """Output comparison results as CSV."""
    if not comparison_results:
        print("No comparison data to output")
        return
    
    # Create DataFrame
    df = pd.DataFrame(comparison_results)
    
    # Select relevant columns
    columns = ['filename', 'size_a', 'size_b', 'size_diff', 'size_ratio', 
               'resolution_a', 'resolution_b', 'resolution_match',
               'mode_a', 'mode_b', 'mode_match', 'psnr', 'ssim',
               'frames_a', 'frames_b', 'framerate_a', 'framerate_b']
    
    # Filter columns that exist
    available_columns = [col for col in columns if col in df.columns]
    df_output = df[available_columns]
    
    # Output to console (first 10 rows)
    print("CSV Preview (first 10 rows):")
    print(df_output.head(10).to_string(index=False))
    
    if output_file:
        df_output.to_csv(output_file, index=False)
        print(f"\nFull CSV report saved to: {output_file}")
    else:
        # If no output file specified, print full CSV
        print("\nFull CSV data:")
        print(df_output.to_csv(index=False))


def _format_size(size_bytes):
    """Format file size in human-readable format."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f}{size_names[i]}"


def analyze_image_quality(image_path):
    """
    Analyze individual image quality metrics.
    
    Args:
        image_path (str): Path to image file
        
    Returns:
        dict: Quality analysis results
    """
    try:
        with Image.open(image_path) as img:
            # Basic properties
            analysis = {
                'filename': os.path.basename(image_path),
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'megapixels': (img.width * img.height) / 1_000_000,
                'file_size': os.path.getsize(image_path),
                'bits_per_pixel': len(img.getbands()) * 8 if hasattr(img, 'getbands') else None
            }
            
            # Calculate compression ratio if possible
            if analysis['bits_per_pixel']:
                uncompressed_size = img.width * img.height * (analysis['bits_per_pixel'] / 8)
                analysis['compression_ratio'] = uncompressed_size / analysis['file_size']
            
            # Histogram analysis
            if img.mode in ('RGB', 'L'):
                arr = np.array(img)
                analysis['mean_intensity'] = np.mean(arr)
                analysis['std_intensity'] = np.std(arr)
                analysis['min_intensity'] = np.min(arr)
                analysis['max_intensity'] = np.max(arr)
            
            # EXIF data if available
            if hasattr(img, '_getexif') and img._getexif():
                analysis['has_exif'] = True
                analysis['exif_entries'] = len(img._getexif())
            else:
                analysis['has_exif'] = False
                analysis['exif_entries'] = 0
            
            return analysis
            
    except Exception as e:
        return {'filename': os.path.basename(image_path), 'error': str(e)}


def batch_quality_analysis(directory, output_file=None):
    """
    Perform quality analysis on all images in a directory.
    
    Args:
        directory (str): Directory containing images
        output_file (str): Optional file to save results
    """
    dir_path = Path(directory)
    
    if not dir_path.exists():
        print(f"Error: Directory {directory} does not exist")
        return
    
    image_files = _get_image_files(dir_path)
    
    print(f"Analyzing {len(image_files)} images in {directory}...")
    
    analyses = []
    for rel_path, file_path in image_files.items():
        print(f"Analyzing {rel_path}...")
        analysis = analyze_image_quality(file_path)
        analyses.append(analysis)
    
    # Create summary report
    successful_analyses = [a for a in analyses if 'error' not in a]
    
    if successful_analyses:
        df = pd.DataFrame(successful_analyses)
        
        print("\nQUALITY ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"Total images analyzed: {len(analyses)}")
        print(f"Successful analyses: {len(successful_analyses)}")
        print(f"Errors: {len(analyses) - len(successful_analyses)}")
        
        if 'file_size' in df.columns:
            print(f"\nFile size statistics:")
            print(f"  Mean: {_format_size(df['file_size'].mean())}")
            print(f"  Min: {_format_size(df['file_size'].min())}")
            print(f"  Max: {_format_size(df['file_size'].max())}")
        
        if 'compression_ratio' in df.columns:
            print(f"\nCompression ratio statistics:")
            print(f"  Mean: {df['compression_ratio'].mean():.2f}x")
            print(f"  Min: {df['compression_ratio'].min():.2f}x")
            print(f"  Max: {df['compression_ratio'].max():.2f}x")
    
    # Save detailed results if requested
    if output_file:
        df = pd.DataFrame(analyses)
        if output_file.endswith('.json'):
            df.to_json(output_file, orient='records', indent=2)
        else:
            df.to_csv(output_file, index=False)
        print(f"\nDetailed analysis saved to: {output_file}")
    
    return analyses