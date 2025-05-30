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
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
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
        
        # Open images
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
        header = f"{'Filename':<30} {'Size A':<10} {'Size B':<10} {'Ratio':<8} {'PSNR':<8} {'SSIM':<8}"
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
            
            row = f"{filename:<30} {size_a:<10} {size_b:<10} {ratio:<8} {psnr:<8} {ssim:<8}"
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
               'mode_a', 'mode_b', 'mode_match', 'psnr', 'ssim']
    
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