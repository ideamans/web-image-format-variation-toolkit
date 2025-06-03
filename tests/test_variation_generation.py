"""
Tests for variation generation and validation functionality.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import sys
import os
import json

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.image_generator import generate_original_images
from src.variation_generator import generate_variations
from src.variation_validator import validate_all_variations
from src.validators.jpeg import ValidationResult


class TestVariationGeneration:
    """Test suite for variation generation and validation."""
    
    @pytest.fixture
    def temp_dir_with_originals(self):
        """Create a temporary directory with original images."""
        temp_dir = tempfile.mkdtemp()
        
        # Generate original images first
        success = generate_original_images(temp_dir)
        if not success:
            shutil.rmtree(temp_dir)
            pytest.fail("Failed to generate original images for testing")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_generate_variations_success(self, temp_dir_with_originals):
        """Test that variations are generated successfully."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        # Check that variation directories are created
        output_path = Path(temp_dir_with_originals)
        assert (output_path / "jpeg").exists(), "JPEG variations directory should be created"
        assert (output_path / "png").exists(), "PNG variations directory should be created"
        assert (output_path / "gif").exists(), "GIF variations directory should be created"
        assert (output_path / "webp").exists(), "WebP variations directory should be created"
        assert (output_path / "avif").exists(), "AVIF variations directory should be created"
    
    def test_index_json_generation(self, temp_dir_with_originals):
        """Test that index.json file is generated correctly."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        index_path = Path(temp_dir_with_originals) / "index.json"
        assert index_path.exists(), "index.json should be created"
        
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        assert isinstance(index_data, list), "index.json should contain a list"
        assert len(index_data) >= 100, f"Should have 100+ variations (including WebP/AVIF), got {len(index_data)}"
        
        # Check structure of first entry
        first_entry = index_data[0]
        required_keys = ["format", "path", "jp", "en"]
        for key in required_keys:
            assert key in first_entry, f"Index entry should have {key} key"
    
    def test_jpeg_variations_count(self, temp_dir_with_originals):
        """Test that expected number of JPEG variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        jpeg_dir = Path(temp_dir_with_originals) / "jpeg"
        jpeg_files = list(jpeg_dir.glob("*.jpg"))
        
        # Expected: 31 regular variations + 7 critical combinations = 38 total (including XMP/IPTC)
        expected_count = 38
        actual_count = len(jpeg_files)
        assert actual_count >= expected_count - 2, f"Should have at least {expected_count-2} JPEG variations, got {actual_count}"
    
    def test_png_variations_count(self, temp_dir_with_originals):
        """Test that expected number of PNG variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        png_dir = Path(temp_dir_with_originals) / "png"
        png_files = list(png_dir.glob("*.png"))
        
        # Expected: 26 regular variations + 4 critical combinations = 30 total
        expected_count = 30
        actual_count = len(png_files)
        assert actual_count >= expected_count - 2, f"Should have at least {expected_count-2} PNG variations, got {actual_count}"
    
    def test_gif_variations_count(self, temp_dir_with_originals):
        """Test that expected number of GIF variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        gif_dir = Path(temp_dir_with_originals) / "gif"
        gif_files = list(gif_dir.glob("*.gif"))
        
        # Expected: 18 regular variations + 3 critical combinations = 21 total
        expected_count = 21
        actual_count = len(gif_files)
        assert actual_count >= expected_count - 2, f"Should have at least {expected_count-2} GIF variations, got {actual_count}"
    
    def test_specific_jpeg_variations_exist(self, temp_dir_with_originals):
        """Test that specific important JPEG variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        jpeg_dir = Path(temp_dir_with_originals) / "jpeg"
        
        # Test key variations
        expected_variations = [
            "colorspace_rgb.jpg",
            "colorspace_cmyk.jpg", 
            "colorspace_grayscale.jpg",
            "quality_20.jpg",
            "quality_50.jpg",
            "quality_80.jpg",
            "quality_95.jpg",
            "encoding_baseline.jpg",
            "encoding_progressive.jpg",
            "thumbnail_none.jpg",
            "thumbnail_embedded.jpg",
            "icc_none.jpg",
            "icc_srgb.jpg",
            "icc_adobergb.jpg",
            "orientation_1.jpg",
            "orientation_6.jpg",
            "dpi_jfif_72dpi.jpg",
            "dpi_exif_200dpi.jpg",
            "metadata_xmp.jpg",
            "metadata_iptc.jpg"
        ]
        
        for variation in expected_variations:
            file_path = jpeg_dir / variation
            assert file_path.exists(), f"JPEG variation {variation} should exist"
            assert file_path.stat().st_size > 0, f"JPEG variation {variation} should not be empty"
    
    def test_specific_png_variations_exist(self, temp_dir_with_originals):
        """Test that specific important PNG variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        png_dir = Path(temp_dir_with_originals) / "png"
        
        # Test key variations
        expected_variations = [
            "colortype_grayscale.png",
            "colortype_palette.png",
            "colortype_rgb.png", 
            "colortype_rgba.png",
            "depth_1bit.png",
            "depth_8bit.png",
            "depth_16bit.png",
            "compression_0.png",
            "compression_9.png",
            "alpha_opaque.png",
            "alpha_transparent.png",
            "interlace_none.png",
            "interlace_adam7.png"
        ]
        
        for variation in expected_variations:
            file_path = png_dir / variation
            assert file_path.exists(), f"PNG variation {variation} should exist"
            assert file_path.stat().st_size > 0, f"PNG variation {variation} should not be empty"
    
    def test_variations_have_different_properties(self, temp_dir_with_originals):
        """Test that variations actually have different properties."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        jpeg_dir = Path(temp_dir_with_originals) / "jpeg"
        
        # Compare quality variations - they should have different file sizes
        quality_files = [
            jpeg_dir / "quality_20.jpg",
            jpeg_dir / "quality_50.jpg", 
            jpeg_dir / "quality_80.jpg",
            jpeg_dir / "quality_95.jpg"
        ]
        
        sizes = []
        for file_path in quality_files:
            if file_path.exists():
                sizes.append(file_path.stat().st_size)
        
        assert len(sizes) >= 3, "Should have at least 3 quality variations"
        # Higher quality should generally mean larger file size
        assert sizes[0] < sizes[-1], "Quality 20 should be smaller than quality 95"
    
    def test_webp_variations_count(self, temp_dir_with_originals):
        """Test that expected number of WebP variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        webp_dir = Path(temp_dir_with_originals) / "webp"
        assert webp_dir.exists(), "WebP directory should exist"
        
        # Check subdirectories
        subdirs = ["lossy", "lossless", "animation"]
        for subdir in subdirs:
            subdir_path = webp_dir / subdir
            assert subdir_path.exists(), f"WebP {subdir} directory should exist"
            
            webp_files = list(subdir_path.glob("*.webp"))
            assert len(webp_files) >= 1, f"WebP {subdir} should have at least 1 file"
    
    def test_avif_variations_count(self, temp_dir_with_originals):
        """Test that expected number of AVIF variations are generated."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        avif_dir = Path(temp_dir_with_originals) / "avif"
        assert avif_dir.exists(), "AVIF directory should exist"
        
        # Check subdirectories
        subdirs = ["lossy", "lossless", "animation"]
        for subdir in subdirs:
            subdir_path = avif_dir / subdir
            assert subdir_path.exists(), f"AVIF {subdir} directory should exist"
            
            # Check for AVIF files or placeholder files (if AVIF support unavailable)
            avif_files = list(subdir_path.glob("*.avif"))
            placeholder_files = list(subdir_path.glob("*.txt"))
            assert len(avif_files) >= 1 or len(placeholder_files) >= 1, f"AVIF {subdir} should have at least 1 file"
    
    def test_webp_files_are_valid(self, temp_dir_with_originals):
        """Test that generated WebP files are valid."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        webp_dir = Path(temp_dir_with_originals) / "webp"
        
        for subdir in ["lossy", "lossless", "animation"]:
            subdir_path = webp_dir / subdir
            webp_files = list(subdir_path.glob("*.webp"))
            
            for webp_file in webp_files:
                assert webp_file.stat().st_size > 0, f"WebP file {webp_file} should not be empty"
                
                # Try to open with PIL to verify it's a valid WebP
                try:
                    with Image.open(webp_file) as img:
                        assert img.format == "WEBP", f"File {webp_file} should be WebP format"
                        assert img.size[0] > 0 and img.size[1] > 0, f"WebP {webp_file} should have valid dimensions"
                except Exception as e:
                    pytest.fail(f"WebP file {webp_file} is not valid: {e}")
    
    def test_index_json_includes_webp_avif(self, temp_dir_with_originals):
        """Test that index.json includes WebP and AVIF entries."""
        success = generate_variations(temp_dir_with_originals, temp_dir_with_originals)
        assert success, "Variation generation should succeed"
        
        index_path = Path(temp_dir_with_originals) / "index.json"
        with open(index_path, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
        
        # Count formats
        formats = {}
        for item in index_data:
            fmt = item.get('format', 'unknown')
            formats[fmt] = formats.get(fmt, 0) + 1
        
        assert 'webp' in formats, "Index should include WebP entries"
        assert 'avif' in formats, "Index should include AVIF entries"
        assert formats['webp'] >= 3, f"Should have at least 3 WebP entries, got {formats.get('webp', 0)}"
        assert formats['avif'] >= 3, f"Should have at least 3 AVIF entries, got {formats.get('avif', 0)}"
        
        # Check WebP entries structure
        webp_entries = [item for item in index_data if item.get('format') == 'webp']
        for entry in webp_entries:
            assert 'path' in entry and entry['path'].startswith('webp/'), "WebP entries should have correct path"
            assert 'jp' in entry and 'WebP' in entry['jp'], "WebP entries should have Japanese description"
            assert 'en' in entry and 'WebP' in entry['en'], "WebP entries should have English description"
        
        # Check AVIF entries structure
        avif_entries = [item for item in index_data if item.get('format') == 'avif']
        for entry in avif_entries:
            assert 'path' in entry and entry['path'].startswith('avif/'), "AVIF entries should have correct path"
            assert 'jp' in entry and 'AVIF' in entry['jp'], "AVIF entries should have Japanese description"
            assert 'en' in entry and 'AVIF' in entry['en'], "AVIF entries should have English description"


class TestVariationValidation:
    """Test suite for variation validation (converted from validate-variations subcommand)."""
    
    @pytest.fixture
    def temp_dir_with_variations(self):
        """Create a temporary directory with generated variations."""
        temp_dir = tempfile.mkdtemp()
        
        # Generate original images and variations
        success = generate_original_images(temp_dir)
        if not success:
            shutil.rmtree(temp_dir)
            pytest.fail("Failed to generate original images for testing")
        
        success = generate_variations(temp_dir, temp_dir)
        if not success:
            shutil.rmtree(temp_dir)
            pytest.fail("Failed to generate variations for testing")
        
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    def test_validate_all_variations_success(self, temp_dir_with_variations):
        """Test that validation runs successfully on generated variations."""
        results = validate_all_variations(temp_dir_with_variations)
        
        assert isinstance(results, dict), "Validation should return results dictionary"
        assert 'total_tested' in results, "Results should include total_tested"
        assert 'total_passed' in results, "Results should include total_passed" 
        assert 'total_failed' in results, "Results should include total_failed"
        
        # Most variations should pass validation
        total_tested = results['total_tested']
        total_passed = results['total_passed']
        
        assert total_tested > 0, "Should test at least some variations"
        pass_rate = total_passed / total_tested if total_tested > 0 else 0
        assert pass_rate >= 0.8, f"At least 80% of variations should pass validation, got {pass_rate:.1%}"
    
    def test_validation_detects_file_existence(self, temp_dir_with_variations):
        """Test that validation correctly detects file existence."""
        results = validate_all_variations(temp_dir_with_variations)
        
        # Check that some basic files are detected as existing
        jpeg_results = results.get('jpeg_results', [])
        existing_files = [r for r in jpeg_results if r.passed]
        
        assert len(existing_files) > 20, f"Should detect many existing JPEG variations, got {len(existing_files)}"
    
    def test_validation_checks_image_properties(self, temp_dir_with_variations):
        """Test that validation checks actual image properties."""
        results = validate_all_variations(temp_dir_with_variations)
        
        # Look for property tests in results
        all_results = results.get('jpeg_results', []) + results.get('png_results', [])
        property_tests = []
        
        for result in all_results:
            for test_name, test_result in result.tests.items():
                if test_name in ['color_mode', 'quality_file_size', 'has_exif', 'orientation', 'has_xmp', 'has_iptc']:
                    property_tests.append(test_result)
        
        assert len(property_tests) > 10, "Should perform multiple property validation tests"
    
    def test_validation_identifies_failures_correctly(self, temp_dir_with_variations):
        """Test that validation can identify actual failures."""
        # Remove a file to create a known failure
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        test_file = jpeg_dir / "quality_20.jpg"
        
        if test_file.exists():
            test_file.unlink()
        
        results = validate_all_variations(temp_dir_with_variations)
        
        # Should detect the missing file
        failed_results = [r for r in results.get('jpeg_results', []) if not r.passed]
        missing_file_failures = [r for r in failed_results if r.filename == "quality_20.jpg"]
        
        assert len(missing_file_failures) > 0, "Should detect missing quality_20.jpg file"
    
    def test_validation_results_structure(self, temp_dir_with_variations):
        """Test that validation results have correct structure."""
        results = validate_all_variations(temp_dir_with_variations)
        
        # Check top-level structure
        required_keys = ['total_tested', 'total_passed', 'total_failed', 'jpeg_results', 'png_results', 'webp_results', 'avif_results', 'summary']
        for key in required_keys:
            assert key in results, f"Results should include {key}"
        
        # Check that results contain ValidationResult objects
        jpeg_results = results['jpeg_results']
        if jpeg_results:
            first_result = jpeg_results[0]
            assert isinstance(first_result, ValidationResult), "JPEG results should contain ValidationResult objects"
            assert hasattr(first_result, 'filename'), "ValidationResult should have filename"
            assert hasattr(first_result, 'passed'), "ValidationResult should have passed flag"
            assert hasattr(first_result, 'tests'), "ValidationResult should have tests dict"
    
    def test_webp_validation_success(self, temp_dir_with_variations):
        """Test that WebP validation runs successfully."""
        results = validate_all_variations(temp_dir_with_variations)
        
        webp_results = results.get('webp_results', [])
        assert isinstance(webp_results, list), "WebP results should be a list"
        
        if webp_results:
            # Check that WebP validation detects files
            webp_passed = sum(1 for r in webp_results if r.passed)
            assert webp_passed >= 2, f"At least 2 WebP variations should pass validation, got {webp_passed}"
            
            # Check WebP-specific tests
            for result in webp_results:
                assert hasattr(result, 'tests'), "WebP result should have tests"
                tests = result.tests
                
                # Should have basic validation tests
                assert 'file_exists' in tests, "WebP validation should check file existence"
                if 'format' in tests:
                    assert tests['format']['expected'] == 'WEBP', "WebP validation should check format"
    
    def test_avif_validation_success(self, temp_dir_with_variations):
        """Test that AVIF validation runs successfully."""
        results = validate_all_variations(temp_dir_with_variations)
        
        avif_results = results.get('avif_results', [])
        assert isinstance(avif_results, list), "AVIF results should be a list"
        
        if avif_results:
            # Check that AVIF validation detects files (may use ImageMagick fallback)
            avif_passed = sum(1 for r in avif_results if r.passed)
            assert avif_passed >= 1, f"At least 1 AVIF variation should pass validation, got {avif_passed}"
            
            # Check AVIF-specific tests
            for result in avif_results:
                assert hasattr(result, 'tests'), "AVIF result should have tests"
                tests = result.tests
                
                # Should have basic validation tests
                assert 'file_exists' in tests, "AVIF validation should check file existence"
                
                # Should use PIL or ImageMagick validation
                has_pil_test = 'pil_readable' in tests
                has_imagemagick_test = 'imagemagick_valid' in tests
                assert has_pil_test or has_imagemagick_test, "AVIF validation should use PIL or ImageMagick"
    
    def test_webp_avif_validation_coverage(self, temp_dir_with_variations):
        """Test that WebP and AVIF validation covers all generated files."""
        # Count generated files
        output_path = Path(temp_dir_with_variations)
        
        webp_files = []
        for subdir in ["lossy", "lossless", "animation"]:
            webp_subdir = output_path / "webp" / subdir
            if webp_subdir.exists():
                webp_files.extend(list(webp_subdir.glob("*.webp")))
        
        avif_files = []
        for subdir in ["lossy", "lossless", "animation"]:
            avif_subdir = output_path / "avif" / subdir
            if avif_subdir.exists():
                avif_files.extend(list(avif_subdir.glob("*.avif")))
        
        # Run validation
        results = validate_all_variations(temp_dir_with_variations)
        
        # Check coverage
        webp_results = results.get('webp_results', [])
        avif_results = results.get('avif_results', [])
        
        if webp_files:
            assert len(webp_results) >= len(webp_files), f"Should validate all {len(webp_files)} WebP files"
        
        if avif_files:
            assert len(avif_results) >= len(avif_files), f"Should validate all {len(avif_files)} AVIF files"


if __name__ == "__main__":
    pytest.main([__file__])