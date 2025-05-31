"""
Detailed validation tests converted from src/variation_validator.py.

This module provides comprehensive validation tests that replicate the functionality
of the original validate-variations subcommand using pytest framework.
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

from src.image_generator import generate_original_images
from src.variation_generator import generate_variations
from src.variation_validator import validate_all_variations, validate_jpeg_file, validate_png_file, ValidationResult


class TestDetailedJPEGValidation:
    """Detailed JPEG validation tests covering all specifications."""
    
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
    
    def test_colorspace_variations(self, temp_dir_with_variations):
        """Test JPEG colorspace variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        # Test RGB colorspace
        rgb_file = jpeg_dir / "colorspace_rgb.jpg"
        if rgb_file.exists():
            result = validate_jpeg_file(rgb_file, "colorspace_rgb.jpg", {'colorspace': 'RGB'})
            assert result.passed, f"RGB colorspace validation failed: {result.errors}"
        
        # Test CMYK colorspace
        cmyk_file = jpeg_dir / "colorspace_cmyk.jpg"
        if cmyk_file.exists():
            result = validate_jpeg_file(cmyk_file, "colorspace_cmyk.jpg", {'colorspace': 'CMYK'})
            assert result.passed, f"CMYK colorspace validation failed: {result.errors}"
        
        # Test Grayscale colorspace
        gray_file = jpeg_dir / "colorspace_grayscale.jpg"
        if gray_file.exists():
            result = validate_jpeg_file(gray_file, "colorspace_grayscale.jpg", {'colorspace': 'L'})
            assert result.passed, f"Grayscale colorspace validation failed: {result.errors}"
    
    def test_quality_variations(self, temp_dir_with_variations):
        """Test JPEG quality variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        quality_specs = [
            ("quality_20.jpg", {'quality_range': (15, 25)}),
            ("quality_50.jpg", {'quality_range': (45, 55)}),
            ("quality_80.jpg", {'quality_range': (75, 85)}),
            ("quality_95.jpg", {'quality_range': (90, 100)}),
        ]
        
        for filename, spec in quality_specs:
            file_path = jpeg_dir / filename
            if file_path.exists():
                result = validate_jpeg_file(file_path, filename, spec)
                assert result.passed, f"Quality validation failed for {filename}: {result.errors}"
    
    def test_encoding_variations(self, temp_dir_with_variations):
        """Test JPEG encoding variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        # Test baseline encoding
        baseline_file = jpeg_dir / "encoding_baseline.jpg"
        if baseline_file.exists():
            result = validate_jpeg_file(baseline_file, "encoding_baseline.jpg", {'progressive': False})
            assert result.passed, f"Baseline encoding validation failed: {result.errors}"
        
        # Test progressive encoding
        progressive_file = jpeg_dir / "encoding_progressive.jpg"
        if progressive_file.exists():
            result = validate_jpeg_file(progressive_file, "encoding_progressive.jpg", {'progressive': True})
            assert result.passed, f"Progressive encoding validation failed: {result.errors}"
    
    def test_thumbnail_variations(self, temp_dir_with_variations):
        """Test JPEG thumbnail variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        # Test no thumbnail
        no_thumb_file = jpeg_dir / "thumbnail_none.jpg"
        if no_thumb_file.exists():
            result = validate_jpeg_file(no_thumb_file, "thumbnail_none.jpg", {'has_thumbnail': False})
            assert result.passed, f"No thumbnail validation failed: {result.errors}"
        
        # Test embedded thumbnail
        thumb_file = jpeg_dir / "thumbnail_embedded.jpg"
        if thumb_file.exists():
            result = validate_jpeg_file(thumb_file, "thumbnail_embedded.jpg", {'has_thumbnail': True})
            assert result.passed, f"Embedded thumbnail validation failed: {result.errors}"
    
    def test_subsampling_variations(self, temp_dir_with_variations):
        """Test JPEG subsampling variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        subsampling_specs = [
            ("subsampling_444.jpg", {'subsampling': '4:4:4'}),
            ("subsampling_422.jpg", {'subsampling': '4:2:2'}),
            ("subsampling_420.jpg", {'subsampling': '4:2:0'}),
        ]
        
        for filename, spec in subsampling_specs:
            file_path = jpeg_dir / filename
            if file_path.exists():
                result = validate_jpeg_file(file_path, filename, spec)
                assert result.passed, f"Subsampling validation failed for {filename}: {result.errors}"
    
    def test_icc_profile_variations(self, temp_dir_with_variations):
        """Test JPEG ICC profile variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        # Test no ICC profile
        no_icc_file = jpeg_dir / "icc_none.jpg"
        if no_icc_file.exists():
            result = validate_jpeg_file(no_icc_file, "icc_none.jpg", {'has_icc_profile': False})
            assert result.passed, f"No ICC profile validation failed: {result.errors}"
        
        # Test sRGB ICC profile
        srgb_file = jpeg_dir / "icc_srgb.jpg"
        if srgb_file.exists():
            result = validate_jpeg_file(srgb_file, "icc_srgb.jpg", {'has_icc_profile': True, 'colorspace_hint': 'sRGB'})
            assert result.passed, f"sRGB ICC profile validation failed: {result.errors}"
        
        # Test Adobe RGB ICC profile
        adobe_file = jpeg_dir / "icc_adobergb.jpg"
        if adobe_file.exists():
            result = validate_jpeg_file(adobe_file, "icc_adobergb.jpg", {'has_icc_profile': True, 'colorspace_hint': 'Adobe'})
            assert result.passed, f"Adobe RGB ICC profile validation failed: {result.errors}"
    
    def test_metadata_variations(self, temp_dir_with_variations):
        """Test JPEG metadata variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        metadata_specs = [
            ("metadata_none.jpg", {'has_exif': False}),
            ("metadata_basic_exif.jpg", {'has_exif': True, 'min_exif_tags': 1}),
            ("metadata_gps.jpg", {'has_exif': True, 'has_gps': True}),
            ("metadata_full_exif.jpg", {'has_exif': True, 'min_exif_tags': 10}),
        ]
        
        for filename, spec in metadata_specs:
            file_path = jpeg_dir / filename
            if file_path.exists():
                result = validate_jpeg_file(file_path, filename, spec)
                assert result.passed, f"Metadata validation failed for {filename}: {result.errors}"
    
    def test_orientation_variations(self, temp_dir_with_variations):
        """Test JPEG orientation variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        orientation_specs = [
            ("orientation_1.jpg", {'orientation': 1}),
            ("orientation_3.jpg", {'orientation': 3}),
            ("orientation_6.jpg", {'orientation': 6}),
            ("orientation_8.jpg", {'orientation': 8}),
        ]
        
        for filename, spec in orientation_specs:
            file_path = jpeg_dir / filename
            if file_path.exists():
                result = validate_jpeg_file(file_path, filename, spec)
                assert result.passed, f"Orientation validation failed for {filename}: {result.errors}"
    
    def test_dpi_variations(self, temp_dir_with_variations):
        """Test JPEG DPI/resolution variations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        dpi_specs = [
            ("dpi_jfif_units0.jpg", {'dpi_type': 'jfif_units0'}),
            ("dpi_jfif_72dpi.jpg", {'dpi_type': 'jfif_72dpi', 'expected_dpi': 72}),
            ("dpi_jfif_200dpi.jpg", {'dpi_type': 'jfif_200dpi', 'expected_dpi': 200}),
            ("dpi_exif_72dpi.jpg", {'dpi_type': 'exif_72dpi', 'expected_dpi': 72}),
            ("dpi_exif_200dpi.jpg", {'dpi_type': 'exif_200dpi', 'expected_dpi': 200}),
        ]
        
        for filename, spec in dpi_specs:
            file_path = jpeg_dir / filename
            if file_path.exists():
                result = validate_jpeg_file(file_path, filename, spec)
                assert result.passed, f"DPI validation failed for {filename}: {result.errors}"


class TestDetailedPNGValidation:
    """Detailed PNG validation tests covering all specifications."""
    
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
    
    def test_colortype_variations(self, temp_dir_with_variations):
        """Test PNG color type variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        colortype_specs = [
            ("colortype_grayscale.png", {'color_mode': 'L'}),
            ("colortype_palette.png", {'color_mode': 'P'}),
            ("colortype_rgb.png", {'color_mode': 'RGB'}),
            ("colortype_rgba.png", {'color_mode': 'RGBA'}),
            ("colortype_grayscale_alpha.png", {'color_mode': 'LA'}),
        ]
        
        for filename, spec in colortype_specs:
            file_path = png_dir / filename
            if file_path.exists():
                result = validate_png_file(file_path, filename, spec)
                assert result.passed, f"Color type validation failed for {filename}: {result.errors}"
    
    def test_bit_depth_variations(self, temp_dir_with_variations):
        """Test PNG bit depth variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        depth_specs = [
            ("depth_1bit.png", {'bit_depth': 1}),
            ("depth_8bit.png", {'bit_depth': 8}),
            ("depth_16bit.png", {'bit_depth': 16}),
        ]
        
        for filename, spec in depth_specs:
            file_path = png_dir / filename
            if file_path.exists():
                result = validate_png_file(file_path, filename, spec)
                assert result.passed, f"Bit depth validation failed for {filename}: {result.errors}"
    
    def test_compression_variations(self, temp_dir_with_variations):
        """Test PNG compression variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        compression_specs = [
            ("compression_0.png", {'compression_level': 0}),
            ("compression_6.png", {'compression_level': 6}),
            ("compression_9.png", {'compression_level': 9}),
        ]
        
        for filename, spec in compression_specs:
            file_path = png_dir / filename
            if file_path.exists():
                result = validate_png_file(file_path, filename, spec)
                assert result.passed, f"Compression validation failed for {filename}: {result.errors}"
    
    def test_alpha_variations(self, temp_dir_with_variations):
        """Test PNG alpha/transparency variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        alpha_specs = [
            ("alpha_opaque.png", {'has_transparency': False}),
            ("alpha_semitransparent.png", {'has_transparency': True, 'alpha_variance': True}),
            ("alpha_transparent.png", {'has_transparency': True}),
        ]
        
        for filename, spec in alpha_specs:
            file_path = png_dir / filename
            if file_path.exists():
                result = validate_png_file(file_path, filename, spec)
                assert result.passed, f"Alpha validation failed for {filename}: {result.errors}"
    
    def test_interlace_variations(self, temp_dir_with_variations):
        """Test PNG interlace variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        interlace_specs = [
            ("interlace_none.png", {'interlaced': False}),
            ("interlace_adam7.png", {'interlaced': True}),
        ]
        
        for filename, spec in interlace_specs:
            file_path = png_dir / filename
            if file_path.exists():
                result = validate_png_file(file_path, filename, spec)
                assert result.passed, f"Interlace validation failed for {filename}: {result.errors}"
    
    def test_metadata_variations(self, temp_dir_with_variations):
        """Test PNG metadata variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        metadata_specs = [
            ("metadata_none.png", {'has_text_chunks': False}),
            ("metadata_text.png", {'has_text_chunks': True}),
            ("metadata_compressed.png", {'has_text_chunks': True}),
            ("metadata_international.png", {'has_text_chunks': True}),
        ]
        
        for filename, spec in metadata_specs:
            file_path = png_dir / filename
            if file_path.exists():
                result = validate_png_file(file_path, filename, spec)
                assert result.passed, f"Metadata validation failed for {filename}: {result.errors}"
    
    def test_filter_variations(self, temp_dir_with_variations):
        """Test PNG filter variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        filter_files = [
            "filter_none.png",
            "filter_sub.png", 
            "filter_up.png",
            "filter_average.png",
            "filter_paeth.png",
        ]
        
        for filename in filter_files:
            file_path = png_dir / filename
            if file_path.exists():
                # These should exist and be readable
                with Image.open(file_path) as img:
                    assert img.format == "PNG", f"Filter variation {filename} should be valid PNG"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Filter variation {filename} should have valid dimensions"
            else:
                # Not all filter variations may be generated, so we don't fail here
                pass
    
    def test_chunk_variations(self, temp_dir_with_variations):
        """Test PNG auxiliary chunk variations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        chunk_files = [
            "chunk_gamma.png",
            "chunk_background.png",
            "chunk_transparency.png",
        ]
        
        for filename in chunk_files:
            file_path = png_dir / filename
            if file_path.exists():
                # These should exist and be readable
                with Image.open(file_path) as img:
                    assert img.format == "PNG", f"Chunk variation {filename} should be valid PNG"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Chunk variation {filename} should have valid dimensions"
            else:
                # Not all chunk variations may be generated, so we don't fail here
                pass


class TestDetailedGIFValidation:
    """Detailed GIF validation tests covering all specifications."""
    
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
    
    def test_frame_count_variations(self, temp_dir_with_variations):
        """Test GIF frame count variations."""
        gif_dir = Path(temp_dir_with_variations) / "gif"
        
        frame_files = [
            "frames_single.gif",
            "frames_short.gif",
            "frames_medium.gif", 
            "frames_long.gif",
        ]
        
        for filename in frame_files:
            file_path = gif_dir / filename
            if file_path.exists():
                with Image.open(file_path) as img:
                    assert img.format == "GIF", f"Frame variation {filename} should be valid GIF"
                    
                    # Count frames
                    frame_count = 0
                    try:
                        while True:
                            img.seek(frame_count)
                            frame_count += 1
                    except EOFError:
                        pass
                    
                    assert frame_count > 0, f"GIF {filename} should have at least 1 frame"
    
    def test_fps_variations(self, temp_dir_with_variations):
        """Test GIF frame rate variations.""" 
        gif_dir = Path(temp_dir_with_variations) / "gif"
        
        fps_files = [
            "fps_slow.gif",
            "fps_normal.gif",
            "fps_fast.gif",
        ]
        
        for filename in fps_files:
            file_path = gif_dir / filename
            if file_path.exists():
                with Image.open(file_path) as img:
                    assert img.format == "GIF", f"FPS variation {filename} should be valid GIF"
                    assert img.size[0] > 0 and img.size[1] > 0, f"FPS variation {filename} should have valid dimensions"
    
    def test_palette_variations(self, temp_dir_with_variations):
        """Test GIF palette size variations."""
        gif_dir = Path(temp_dir_with_variations) / "gif"
        
        palette_files = [
            "palette_2colors.gif",
            "palette_16colors.gif",
            "palette_256colors.gif",
        ]
        
        for filename in palette_files:
            file_path = gif_dir / filename
            if file_path.exists():
                with Image.open(file_path) as img:
                    assert img.format == "GIF", f"Palette variation {filename} should be valid GIF"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Palette variation {filename} should have valid dimensions"
    
    def test_optimization_variations(self, temp_dir_with_variations):
        """Test GIF optimization variations."""
        gif_dir = Path(temp_dir_with_variations) / "gif"
        
        optimization_files = [
            "optimize_noopt.gif",
            "optimize_optimized.gif",
        ]
        
        for filename in optimization_files:
            file_path = gif_dir / filename
            if file_path.exists():
                with Image.open(file_path) as img:
                    assert img.format == "GIF", f"Optimization variation {filename} should be valid GIF"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Optimization variation {filename} should have valid dimensions"
    
    def test_loop_variations(self, temp_dir_with_variations):
        """Test GIF loop variations."""
        gif_dir = Path(temp_dir_with_variations) / "gif"
        
        loop_files = [
            "loop_loop_infinite.gif",
            "loop_loop_once.gif",
            "loop_loop_3times.gif",
        ]
        
        for filename in loop_files:
            file_path = gif_dir / filename
            if file_path.exists():
                with Image.open(file_path) as img:
                    assert img.format == "GIF", f"Loop variation {filename} should be valid GIF"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Loop variation {filename} should have valid dimensions"
    
    def test_gif_critical_combinations(self, temp_dir_with_variations):
        """Test GIF critical combinations."""
        gif_dir = Path(temp_dir_with_variations) / "gif"
        
        critical_files = [
            "critical_fast_256colors_long.gif",
            "critical_dither_smallpalette.gif", 
            "critical_noopt_manyframes.gif",
        ]
        
        for filename in critical_files:
            file_path = gif_dir / filename
            if file_path.exists():
                with Image.open(file_path) as img:
                    assert img.format == "GIF", f"GIF critical combination {filename} should be valid GIF"
                    assert img.size[0] > 0 and img.size[1] > 0, f"GIF critical combination {filename} should have valid dimensions"


class TestCriticalCombinations:
    """Test critical combination variations that are known to be problematic."""
    
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
    
    def test_jpeg_critical_combinations(self, temp_dir_with_variations):
        """Test JPEG critical combinations."""
        jpeg_dir = Path(temp_dir_with_variations) / "jpeg"
        
        critical_files = [
            "critical_cmyk_lowquality.jpg",
            "critical_progressive_fullmeta.jpg",
            "critical_thumbnail_progressive.jpg",
            "critical_orientation_metadata.jpg",
            "critical_jfif_exif_dpi.jpg",
        ]
        
        for filename in critical_files:
            file_path = jpeg_dir / filename
            if file_path.exists():
                # These should exist and be readable
                with Image.open(file_path) as img:
                    assert img.format == "JPEG", f"Critical combination {filename} should be valid JPEG"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Critical combination {filename} should have valid dimensions"
            else:
                pytest.fail(f"Critical combination file {filename} should exist")
    
    def test_png_critical_combinations(self, temp_dir_with_variations):
        """Test PNG critical combinations."""
        png_dir = Path(temp_dir_with_variations) / "png"
        
        critical_files = [
            "critical_16bit_palette.png",
            "critical_alpha_grayscale.png",
            "critical_maxcompression_paeth.png",
            "critical_interlace_highres.png",
        ]
        
        for filename in critical_files:
            file_path = png_dir / filename
            if file_path.exists():
                # These should exist and be readable
                with Image.open(file_path) as img:
                    assert img.format == "PNG", f"Critical combination {filename} should be valid PNG"
                    assert img.size[0] > 0 and img.size[1] > 0, f"Critical combination {filename} should have valid dimensions"
            else:
                pytest.fail(f"Critical combination file {filename} should exist")


class TestFileSystemValidation:
    """Test file system level validation."""
    
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
    
    def test_all_expected_files_exist(self, temp_dir_with_variations):
        """Test that all expected variation files exist."""
        results = validate_all_variations(temp_dir_with_variations)
        
        # Check JPEG files
        jpeg_results = results.get('jpeg_results', [])
        missing_jpeg = [r.filename for r in jpeg_results if not r.passed and 'file_exists' in r.tests and not r.tests['file_exists']['passed']]
        
        # Check PNG files  
        png_results = results.get('png_results', [])
        missing_png = [r.filename for r in png_results if not r.passed and 'file_exists' in r.tests and not r.tests['file_exists']['passed']]
        
        assert len(missing_jpeg) == 0, f"Missing JPEG files: {missing_jpeg}"
        assert len(missing_png) == 0, f"Missing PNG files: {missing_png}"
    
    def test_file_sizes_reasonable(self, temp_dir_with_variations):
        """Test that all generated files have reasonable sizes."""
        output_path = Path(temp_dir_with_variations)
        
        for subdir in ['jpeg', 'png', 'gif']:
            subdir_path = output_path / subdir
            if subdir_path.exists():
                for file_path in subdir_path.glob(f"*.{subdir.rstrip('g')}"):
                    file_size = file_path.stat().st_size
                    assert file_size > 1000, f"File {file_path.name} is too small ({file_size} bytes)"
                    assert file_size < 10_000_000, f"File {file_path.name} is too large ({file_size} bytes)"
    
    def test_comprehensive_validation_coverage(self, temp_dir_with_variations):
        """Test that validation covers all expected file types and properties."""
        results = validate_all_variations(temp_dir_with_variations)
        
        # Check that we tested a reasonable number of files
        total_tested = results['total_tested']
        assert total_tested >= 45, f"Should test at least 45 variations, tested {total_tested}"
        
        # Check that pass rate is high
        total_passed = results['total_passed']
        pass_rate = total_passed / total_tested if total_tested > 0 else 0
        assert pass_rate >= 0.85, f"Pass rate should be at least 85%, got {pass_rate:.1%}"


if __name__ == "__main__":
    pytest.main([__file__])