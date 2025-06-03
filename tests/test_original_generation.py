"""
Tests for original image generation functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.image_generator import generate_original_images, test_original_compliance


class TestOriginalGeneration:
    """Test suite for original image generation."""
    
    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary directory for test outputs."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_generate_original_images_success(self, temp_output_dir):
        """Test that original images are generated successfully."""
        success = generate_original_images(temp_output_dir)
        assert success, "Original image generation should succeed"
        
        # Check that all expected files are created
        output_path = Path(temp_output_dir)
        expected_files = [
            "test_original.jpg",
            "test_original.png", 
            "test_original.gif"
        ]
        
        for filename in expected_files:
            file_path = output_path / filename
            assert file_path.exists(), f"Expected file {filename} should be created"
            assert file_path.stat().st_size > 0, f"File {filename} should not be empty"
    
    def test_jpeg_original_specifications(self, temp_output_dir):
        """Test that generated JPEG meets specifications."""
        success = generate_original_images(temp_output_dir)
        assert success, "Original image generation should succeed"
        
        jpeg_path = Path(temp_output_dir) / "test_original.jpg"
        
        with Image.open(jpeg_path) as img:
            # Test format and mode
            assert img.format == "JPEG", "Image should be JPEG format"
            assert img.mode == "RGB", "JPEG should be RGB mode"
            
            # Test size (640x480 as configured)
            assert img.size == (640, 480), f"JPEG should be 640x480, got {img.size}"
            
            # Test EXIF data existence
            exif = img.getexif()
            assert len(exif) > 0, "JPEG should have EXIF data"
    
    def test_png_original_specifications(self, temp_output_dir):
        """Test that generated PNG meets specifications."""
        success = generate_original_images(temp_output_dir)
        assert success, "Original image generation should succeed"
        
        png_path = Path(temp_output_dir) / "test_original.png"
        
        with Image.open(png_path) as img:
            # Test format and mode
            assert img.format == "PNG", "Image should be PNG format"
            assert img.mode == "RGBA", "PNG should be RGBA mode (with alpha)"
            
            # Test size (480x480 as configured)
            assert img.size == (480, 480), f"PNG should be 480x480, got {img.size}"
            
            # Test transparency
            assert img.mode in ('RGBA', 'LA'), "PNG should have alpha channel"
            
            # Test metadata
            assert hasattr(img, 'text'), "PNG should have text metadata"
            assert len(img.text) > 0, "PNG should have metadata chunks"
    
    def test_gif_original_specifications(self, temp_output_dir):
        """Test that generated GIF meets specifications."""
        success = generate_original_images(temp_output_dir)
        assert success, "Original image generation should succeed"
        
        gif_path = Path(temp_output_dir) / "test_original.gif"
        
        with Image.open(gif_path) as img:
            # Test format
            assert img.format == "GIF", "Image should be GIF format"
            
            # Test animation (should have multiple frames)
            frame_count = 0
            try:
                while True:
                    img.seek(frame_count)
                    frame_count += 1
            except EOFError:
                pass
            
            assert frame_count >= 5, f"GIF should have at least 5 frames, got {frame_count}"
    
    def test_original_compliance_check(self, temp_output_dir):
        """Test the compliance checking functionality."""
        success = generate_original_images(temp_output_dir)
        assert success, "Original image generation should succeed"
        
        # This should not raise an exception
        try:
            test_original_compliance(temp_output_dir)
        except Exception as e:
            pytest.fail(f"Original compliance test should not raise exception: {e}")
    
    def test_output_directory_creation(self):
        """Test that output directory is created if it doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_base:
            output_dir = os.path.join(temp_base, "new_output_dir")
            assert not os.path.exists(output_dir), "Output directory should not exist initially"
            
            success = generate_original_images(output_dir)
            assert success, "Generation should succeed even with new directory"
            assert os.path.exists(output_dir), "Output directory should be created"
    
    def test_file_size_reasonable(self, temp_output_dir):
        """Test that generated files have reasonable sizes."""
        success = generate_original_images(temp_output_dir)
        assert success, "Original image generation should succeed"
        
        output_path = Path(temp_output_dir)
        
        # Test JPEG file size (should be reasonable for 640x480)
        jpeg_path = output_path / "test_original.jpg"
        jpeg_size = jpeg_path.stat().st_size
        assert 50000 <= jpeg_size <= 500000, f"JPEG size {jpeg_size} should be reasonable (50KB-500KB)"
        
        # Test PNG file size (should be reasonable for 480x480 RGBA)
        png_path = output_path / "test_original.png"
        png_size = png_path.stat().st_size
        assert 45000 <= png_size <= 1000000, f"PNG size {png_size} should be reasonable (45KB-1MB)"
        
        # Test GIF file size
        gif_path = output_path / "test_original.gif"
        gif_size = gif_path.stat().st_size
        assert 5000 <= gif_size <= 100000, f"GIF size {gif_size} should be reasonable (5KB-100KB)"


if __name__ == "__main__":
    pytest.main([__file__])