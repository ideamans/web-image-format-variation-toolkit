"""
ImageMagick utility functions.

This module provides common ImageMagick command execution and detection utilities.
"""

import subprocess
import os


class ImageMagickUtils:
    """Utility class for ImageMagick operations."""
    
    # Global variable to cache detected ImageMagick command
    _imagemagick_cmd = None
    
    @classmethod
    def run_command(cls, cmd):
        """
        Run ImageMagick command with error handling.
        
        Args:
            cmd (list): Command list to execute
            
        Returns:
            bool: True if successful, False otherwise
        """
        # Detect and cache ImageMagick command if not already done
        if cls._imagemagick_cmd is None:
            # Try both 'magick' and 'convert' commands
            for test_cmd in ['magick', 'convert']:
                try:
                    subprocess.run([test_cmd, '--version'], capture_output=True, check=True)
                    cls._imagemagick_cmd = test_cmd
                    print(f"Detected ImageMagick command: {cls._imagemagick_cmd}")
                    break
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            if cls._imagemagick_cmd is None:
                print("ImageMagick not found. Please install ImageMagick.")
                return False
        
        try:
            # Replace command with detected ImageMagick command
            cmd[0] = cls._imagemagick_cmd
            
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"ImageMagick command failed: {' '.join(cmd)}")
            print(f"Error: {e.stderr}")
            return False
        except FileNotFoundError:
            print("ImageMagick not found. Please install ImageMagick.")
            return False
    
    @classmethod
    def get_image_properties(cls, file_path):
        """
        Get comprehensive image properties using ImageMagick identify command.
        
        Args:
            file_path (str): Path to image file
            
        Returns:
            dict: Image properties or None if detection failed
        """
        try:
            # Get multiple properties in one command
            format_str = "%[bit-depth],%[colorspace],%[type],%[compression],%[interlace]"
            cmd = ["identify", "-format", format_str, str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            properties = result.stdout.strip().split(',')
            if len(properties) >= 5:
                return {
                    'bit_depth': int(properties[0]) if properties[0].isdigit() else None,
                    'colorspace': properties[1] if properties[1] else None,
                    'type': properties[2] if properties[2] else None,
                    'compression': properties[3] if properties[3] else None,
                    'interlace': properties[4] if properties[4] else None
                }
            else:
                return None
                
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError, IndexError):
            return None
    
    @classmethod
    def get_bit_depth(cls, file_path):
        """
        Get image bit depth using ImageMagick identify command.
        
        Args:
            file_path (str): Path to image file
            
        Returns:
            int or None: Bit depth per channel, or None if detection failed
        """
        try:
            # Use ImageMagick identify to get detailed image information
            cmd = ["identify", "-format", "%[bit-depth]", str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            bit_depth_str = result.stdout.strip()
            if bit_depth_str and bit_depth_str.isdigit():
                return int(bit_depth_str)
            else:
                return None
                
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
            return None
    
    @classmethod
    def get_jpeg_properties(cls, file_path):
        """
        Get JPEG-specific properties using ImageMagick identify command.
        
        Args:
            file_path (str): Path to JPEG file
            
        Returns:
            dict: JPEG properties or None if detection failed
        """
        try:
            # Get JPEG-specific properties
            format_str = "%[colorspace],%[quality],%[interlace],%[sampling-factor]"
            cmd = ["identify", "-format", format_str, str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            properties = result.stdout.strip().split(',')
            if len(properties) >= 4:
                return {
                    'colorspace': properties[0] if properties[0] else None,
                    'quality': int(properties[1]) if properties[1].isdigit() else None,
                    'interlace': properties[2] if properties[2] else None,
                    'sampling_factor': properties[3] if properties[3] else None
                }
            else:
                return None
                
        except (subprocess.CalledProcessError, FileNotFoundError, ValueError, IndexError):
            return None
    
    @classmethod
    def get_jpeg_subsampling(cls, file_path):
        """Get JPEG subsampling information using ImageMagick identify command."""
        try:
            result = subprocess.run(['identify', '-verbose', str(file_path)], 
                                  capture_output=True, text=True, check=True)
            
            for line in result.stdout.split('\n'):
                if 'sampling-factor:' in line.lower():
                    # Extract sampling factor like "2x2,1x1,1x1" and convert to standard notation
                    factor = line.split(':')[-1].strip()
                    if '2x2,1x1,1x1' in factor or '2x2' in factor:
                        return '4:2:0'
                    elif '2x1,1x1,1x1' in factor or '2x1' in factor:
                        return '4:2:2'
                    elif '1x1,1x1,1x1' in factor or '1x1' in factor:
                        return '4:4:4'
            
            return None
        except:
            return None
    
    @classmethod
    def check_xmp_metadata(cls, file_path):
        """
        Check if image has XMP metadata using ImageMagick identify command.
        
        Args:
            file_path (str): Path to image file
            
        Returns:
            bool: True if XMP metadata is present, False otherwise
        """
        try:
            # Get XMP metadata
            cmd = ["identify", "-format", "%[xmp:*]", str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            xmp_data = result.stdout.strip()
            return bool(xmp_data and xmp_data != "")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @classmethod
    def check_iptc_metadata(cls, file_path):
        """
        Check if image has IPTC metadata using ImageMagick identify command.
        
        Args:
            file_path (str): Path to image file
            
        Returns:
            bool: True if IPTC metadata is present, False otherwise
        """
        try:
            # Get IPTC metadata
            cmd = ["identify", "-format", "%[iptc:*]", str(file_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            iptc_data = result.stdout.strip()
            return bool(iptc_data and iptc_data != "")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False