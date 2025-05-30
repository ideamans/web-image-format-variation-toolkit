"""
Utility functions for the image processing toolkit.

This module contains common helper functions used across the toolkit.
"""

import os
import sys
import subprocess
from pathlib import Path


def check_dependencies():
    """
    Check if required external tools are available.
    
    Returns:
        dict: Status of each dependency
    """
    dependencies = {
        'imagemagick': False,
        'python_libs': True  # Assume Python libs are OK if we got this far
    }
    
    # Check ImageMagick
    try:
        result = subprocess.run(['convert', '-version'], 
                              capture_output=True, text=True, check=True)
        if 'ImageMagick' in result.stdout:
            dependencies['imagemagick'] = True
    except (subprocess.CalledProcessError, FileNotFoundError):
        dependencies['imagemagick'] = False
    
    return dependencies


def print_dependency_status():
    """Print the status of all dependencies."""
    deps = check_dependencies()
    
    print("Dependency Status:")
    print("-" * 30)
    
    for tool, available in deps.items():
        status = "✓ Available" if available else "✗ Missing"
        print(f"{tool:15}: {status}")
    
    if not deps['imagemagick']:
        print("\nImageMagick is required for image format conversions.")
        print("Please install ImageMagick:")
        print("  macOS: brew install imagemagick")
        print("  Ubuntu: sudo apt-get install imagemagick")
        print("  Windows: Download from https://imagemagick.org/script/download.php")
    
    return all(deps.values())


def ensure_directory(path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        path (str or Path): Directory path to create
        
    Returns:
        Path: Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_file_size(file_path):
    """
    Get file size in bytes.
    
    Args:
        file_path (str or Path): Path to file
        
    Returns:
        int: File size in bytes, or 0 if file doesn't exist
    """
    try:
        return Path(file_path).stat().st_size
    except (OSError, FileNotFoundError):
        return 0


def format_file_size(size_bytes):
    """
    Format file size in human-readable format.
    
    Args:
        size_bytes (int): Size in bytes
        
    Returns:
        str: Formatted size string
    """
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    if i == 0:
        return f"{int(size_bytes)}{size_names[i]}"
    else:
        return f"{size_bytes:.1f}{size_names[i]}"


def validate_image_file(file_path):
    """
    Validate if a file is a supported image format.
    
    Args:
        file_path (str or Path): Path to image file
        
    Returns:
        bool: True if file is a valid image, False otherwise
    """
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    
    path = Path(file_path)
    
    # Check if file exists
    if not path.exists():
        return False
    
    # Check extension
    if path.suffix.lower() not in supported_extensions:
        return False
    
    # Try to open with PIL
    try:
        from PIL import Image
        with Image.open(path) as img:
            img.verify()  # Verify it's a valid image
        return True
    except Exception:
        return False


def get_image_files(directory, recursive=True):
    """
    Get all image files in a directory.
    
    Args:
        directory (str or Path): Directory to search
        recursive (bool): Whether to search subdirectories
        
    Returns:
        list: List of Path objects for image files
    """
    supported_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.gif'}
    
    dir_path = Path(directory)
    
    if not dir_path.exists():
        return []
    
    image_files = []
    
    if recursive:
        pattern = "**/*"
    else:
        pattern = "*"
    
    for file_path in dir_path.glob(pattern):
        if (file_path.is_file() and 
            file_path.suffix.lower() in supported_extensions and
            validate_image_file(file_path)):
            image_files.append(file_path)
    
    return sorted(image_files)


def safe_filename(filename):
    """
    Create a safe filename by removing/replacing problematic characters.
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Safe filename
    """
    # Characters that are problematic in filenames
    unsafe_chars = '<>:"/\\|?*'
    
    safe_name = filename
    for char in unsafe_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip(' .')
    
    # Ensure it's not empty
    if not safe_name:
        safe_name = "unnamed"
    
    return safe_name


def print_progress(current, total, prefix="Progress", suffix="Complete", length=50):
    """
    Print a progress bar.
    
    Args:
        current (int): Current progress
        total (int): Total items
        prefix (str): Prefix text
        suffix (str): Suffix text
        length (int): Length of progress bar
    """
    if total <= 0:
        return
    
    percent = (current / total) * 100
    filled_length = int(length * current // total)
    bar = '█' * filled_length + '-' * (length - filled_length)
    
    print(f'\r{prefix} |{bar}| {current}/{total} ({percent:.1f}%) {suffix}', end='')
    
    if current == total:
        print()  # New line when complete


def log_operation(operation, success=True, details=None):
    """
    Log an operation result.
    
    Args:
        operation (str): Description of operation
        success (bool): Whether operation was successful
        details (str): Additional details
    """
    status = "SUCCESS" if success else "FAILED"
    timestamp = __import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    log_line = f"[{timestamp}] {status}: {operation}"
    if details:
        log_line += f" - {details}"
    
    print(log_line)


def create_project_structure(base_dir="."):
    """
    Create the standard project directory structure.
    
    Args:
        base_dir (str): Base directory for project
        
    Returns:
        dict: Created directory paths
    """
    base_path = Path(base_dir)
    
    directories = {
        'src': base_path / 'src',
        'tests': base_path / 'tests',
        'output': base_path / 'output',
        'output_jpeg': base_path / 'output' / 'jpeg',
        'output_png': base_path / 'output' / 'png',
    }
    
    for name, path in directories.items():
        ensure_directory(path)
        log_operation(f"Created directory: {path}")
    
    return directories


def get_toolkit_info():
    """
    Get information about the toolkit.
    
    Returns:
        dict: Toolkit information
    """
    try:
        from src import __version__
        version = __version__
    except ImportError:
        version = "Unknown"
    
    return {
        'name': 'Image Processing Toolkit',
        'version': version,
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'platform': sys.platform,
        'cwd': os.getcwd()
    }


def print_toolkit_info():
    """Print toolkit information."""
    info = get_toolkit_info()
    
    print("Image Processing Toolkit")
    print("=" * 30)
    print(f"Version: {info['version']}")
    print(f"Python: {info['python_version']}")
    print(f"Platform: {info['platform']}")
    print(f"Working Directory: {info['cwd']}")
    print()


class ToolkitError(Exception):
    """Custom exception for toolkit errors."""
    pass


class ImageProcessingError(ToolkitError):
    """Exception for image processing errors."""
    pass


class ValidationError(ToolkitError):
    """Exception for validation errors."""
    pass