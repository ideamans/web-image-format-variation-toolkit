# Image Processing Toolkit Requirements

## Project Overview

This project aims to develop a Python-based image processing toolkit for generating and testing various image format variations, specifically focusing on JPEG, PNG, GIF, WebP, and AVIF formats. The toolkit will be used to create comprehensive test datasets for image conversion library development.

## Technical Stack

- **Python**: Primary programming language
- **Bash**: Shell scripting for system integration
- **ImageMagick**: Image manipulation and conversion
- **FFmpeg**: Additional media processing capabilities
- **Required Python Libraries**:
  - Pillow (PIL): Basic image operations and metadata handling
  - piexif: Detailed EXIF data manipulation
  - numpy: Numerical computations and image array operations
  - opencv-python: Advanced image processing and color space conversions
  - scikit-image: Image quality metrics (SSIM, PSNR)
  - matplotlib: Visualization and histogram comparison
  - pytest: Test automation framework

- **WebP and AVIF Support Libraries**:
  - **WebP**: Native Pillow support (no additional libraries required)
  - **AVIF**: pillow-heif>=0.22.0 (optional for reading AVIF files in validation)
  - **AVIF Generation**: ImageMagick with AVIF support (system dependency)
  - **AVIF Animation**: FFmpeg with libaom-av1 encoder (system dependency)

- **System Dependencies**:
  - **ImageMagick**: Required for AVIF generation and advanced image operations
  - **FFmpeg**: Required for AVIF animation generation using libaom-av1 encoder
  - **libavif**: System library for AVIF support in ImageMagick

## Code Architecture

The toolkit follows a modular architecture with format-specific components:

### Directory Structure

```
src/
├── generators/          # Format-specific variation generators
│   ├── __init__.py
│   ├── jpeg.py         # JPEG format variation generator
│   ├── png.py          # PNG format variation generator
│   ├── gif.py          # GIF format variation generator
│   ├── webp.py         # WebP format variation generator
│   └── avif.py         # AVIF format variation generator
├── validators/         # Format-specific variation validators
│   ├── __init__.py
│   ├── jpeg.py         # JPEG format variation validator
│   ├── png.py          # PNG format variation validator
│   ├── gif.py          # GIF format variation validator
│   ├── webp.py         # WebP format variation validator
│   └── avif.py         # AVIF format variation validator
├── utils/              # Common utility modules
│   ├── __init__.py
│   ├── imagemagick.py  # ImageMagick command wrapper utilities
│   └── metadata.py     # Metadata manipulation utilities
├── image_generator.py  # Original test image generation
├── image_comparator.py # Image comparison functionality
├── variation_generator.py # Main variation generation coordinator
├── variation_validator.py # Main validation coordinator
└── utils.py           # Legacy utilities
```

### Architecture Benefits

- **Modularity**: Each format has its own dedicated generator and validator
- **Maintainability**: Format-specific code is isolated and easier to maintain
- **Extensibility**: New formats can be added by creating new generator/validator modules
- **Reusability**: Common utilities are shared across all formats
- **Testing**: Each module can be tested independently

## Core Functionality

The toolkit consists of three main components:

### 1. Original Image Generation and Testing

Generate ideal source images that meet specific requirements for comprehensive format variation testing.

### 2. Variation Generation and Testing

Create all specified format variations from source images and validate they meet requirements.

### 3. Image Comparison

Compare identical images across different directories, analyzing file size, resolution, PSNR, SSIM, and file presence/absence. Supports static images and animated GIF frame-by-frame comparison.

## Original Image Specifications

### JPEG Source Image Requirements

**Color Space and Model**

- **RGB color space** (sRGB recommended)
- Rationale: Enables conversion testing to CMYK and Grayscale without information loss

**Compression and Quality Settings**

- **Quality 95 or higher** (highest possible quality)
- **4:4:4 subsampling** (no chroma subsampling)
- **Baseline JPEG encoding**
- Rationale: Allows testing degradation from high to low quality and various subsampling modes

**Color Depth**

- **8 bits per channel**
- Standard depth allowing all conversion tests

**Metadata Requirements**

- **Rich EXIF data included**
- GPS information, shooting parameters, copyright information
- Rationale: Enables metadata preservation/removal testing

**Content Requirements**

- **High-frequency components**: Fine details like grass, leaves, flower petals
- **Low-frequency components**: Sky, blurred backgrounds, gradients
- **Rich color information**: Balanced green, warm, and cool tones
- **Skin-like color regions**: For human perception testing
- **Gradient elements**: Sky, shadows for compression artifact visibility

### PNG Source Image Requirements

**Color Depth and Channel Configuration**

- **32-bit RGBA** (8 bits per channel + alpha)
- Rationale: Allows conversion testing to all other color depths

**Transparency Requirements**

- **Full transparency, semi-transparency, and opaque regions all included**
- Alpha channel values: 0, 64, 128, 192, 255 (gradual steps)
- Rationale: Enables transparency processing and tRNS chunk generation testing

**Color Composition**

- **Full color** (not palette-indexed)
- Rich color count
- Rationale: Allows palette conversion and grayscale conversion testing

**Compression Settings**

- **Compression level 6** (default)
- **Adaptive filter type**
- **No interlacing**
- Rationale: Enables testing of higher compression and different filters

**Content Requirements**

- **Sharp edges**: Text, geometric shapes
- **Flat color areas**: PNG compression efficiency verification
- **Anti-aliased curves**: Smooth curve rendering
- **Multiple color depth elements**: Gradients + flat areas
- **Transparent elements**: For PNG-specific feature testing

## Programmatic Image Generation

**Note**: For complete source code implementation of the image generation functions described below, refer to `generation-draft.md` which contains the full Python code with detailed explanations and usage instructions.

### JPEG Test Image Generation Approach

Create a synthetic photograph-like image containing:

1. **Sky gradient** (low-frequency components): Blue to white gradient
2. **Ground/grass area** (high-frequency components): Perlin noise-generated grass texture
3. **Flower scatter** (colorful point elements): Random red, yellow, purple, pink dots
4. **Cloud addition** (soft white regions): Gaussian blur-based cloud layers
5. **Skin color elements** (human representation): Simple elliptical face shapes

### PNG Test Image Generation Approach

Create a design graphic containing:

1. **Background gradient** (semi-transparent): Horizontal hue shift with vertical alpha fade
2. **Geometric shapes** (opaque regions): Circles, rectangles, triangles in solid colors
3. **Semi-transparent gradient effects**: Layered transparent circles
4. **Text elements** (anti-aliasing verification): Multi-language text with outline effects
5. **Complex transparency patterns**: Checkerboard with varying alpha levels
6. **Noise patterns** (fine details): Random pixel noise for texture

### GIF Test Image Generation Approach
Create an animated sequence containing:

1. **Moving elements** (temporal variation): Bouncing ball animation for motion testing
2. **Rotating elements** (geometric transformation): Spinning geometric shapes
3. **Color changes** (palette transitions): Animated color cycling effects
4. **Text elements** (anti-aliasing in animation): Pulsing text with transparency
5. **Progress indicators** (linear animation): Moving progress bars

**Animation Properties**
- **Resolution**: 200x200 pixels (optimized for file size management)
- **Frame count**: 10 frames (sufficient for variation testing)
- **Frame rate**: 10 FPS (100ms per frame)
- **Color depth**: 256 colors with dithering support

## Format Variation Specifications

### JPEG Variations

#### Single-Choice Factors

**Color Space**

- `jpeg/colorspace_rgb.jpg` - Convert to RGB color space, most common web format
- `jpeg/colorspace_cmyk.jpg` - Convert to CMYK color space for print applications  
- `jpeg/colorspace_grayscale.jpg` - Convert to grayscale, single channel image

**Encoding Format**

- `jpeg/encoding_baseline.jpg` - Standard baseline JPEG encoding
- `jpeg/encoding_progressive.jpg` - Progressive JPEG for web streaming display

**Thumbnail**

- `jpeg/thumbnail_none.jpg` - JPEG without embedded thumbnail
- `jpeg/thumbnail_embedded.jpg` - JPEG with embedded EXIF thumbnail

**Exif Orientation**

- `jpeg/orientation_1.jpg` - Normal orientation (Top-left)
- `jpeg/orientation_3.jpg` - Rotated 180 degrees (Bottom-right)
- `jpeg/orientation_6.jpg` - Rotated 90 degrees clockwise (Right-top)
- `jpeg/orientation_8.jpg` - Rotated 90 degrees counter-clockwise (Left-bottom)

#### Numerical Factors

**Quality Settings**

- `jpeg/quality_20.jpg` - Very low quality with high compression artifacts
- `jpeg/quality_50.jpg` - Medium quality, balanced compression
- `jpeg/quality_80.jpg` - High quality, minimal compression artifacts
- `jpeg/quality_95.jpg` - Very high quality, near lossless

**Subsampling**

- `jpeg/subsampling_444.jpg` - No chroma subsampling, full color information
- `jpeg/subsampling_422.jpg` - Moderate chroma subsampling
- `jpeg/subsampling_420.jpg` - Heavy chroma subsampling, smallest file size

#### Multi-Choice Factors (Individual)

**Metadata Individual**

- `jpeg/metadata_none.jpg` - No metadata, clean JPEG file
- `jpeg/metadata_basic_exif.jpg` - Basic EXIF data only
- `jpeg/metadata_gps.jpg` - GPS location data included
- `jpeg/metadata_full_exif.jpg` - Complete EXIF metadata set
- `jpeg/metadata_xmp.jpg` - XMP metadata blocks included
- `jpeg/metadata_iptc.jpg` - IPTC metadata records included

**ICC Profile Individual**

- `jpeg/icc_none.jpg` - No color profile embedded
- `jpeg/icc_srgb.jpg` - Standard sRGB color profile
- `jpeg/icc_adobergb.jpg` - Adobe RGB wide gamut profile

**EXIF Orientation Individual**

- `jpeg/orientation_1.jpg` - Normal orientation (Top-left), standard view
- `jpeg/orientation_3.jpg` - Rotated 180 degrees (Bottom-right), upside down
- `jpeg/orientation_6.jpg` - Rotated 90 degrees clockwise (Right-top), portrait to landscape
- `jpeg/orientation_8.jpg` - Rotated 90 degrees counter-clockwise (Left-bottom), landscape to portrait

**DPI/Resolution Individual**

- `jpeg/dpi_jfif_units0.jpg` - JFIF units:0 (aspect ratio only, no absolute DPI)
- `jpeg/dpi_jfif_72dpi.jpg` - JFIF units:1 with 72 DPI (web standard)
- `jpeg/dpi_jfif_200dpi.jpg` - JFIF units:1 with 200 DPI (print quality)
- `jpeg/dpi_exif_72dpi.jpg` - EXIF specified 72 DPI (no JFIF resolution)
- `jpeg/dpi_exif_200dpi.jpg` - EXIF specified 200 DPI (no JFIF resolution)

#### Critical Combinations

**CMYK + High Compression**

- `jpeg/critical_cmyk_lowquality.jpg` - CMYK colorspace with aggressive compression, quality 30

**Progressive + Rich Metadata**

- `jpeg/critical_progressive_fullmeta.jpg` - Progressive encoding with complete EXIF and GPS data

**Thumbnail + Progressive**

- `jpeg/critical_thumbnail_progressive.jpg` - Progressive JPEG with embedded thumbnail, potential compatibility issues

**Orientation + Metadata**

- `jpeg/critical_orientation_metadata.jpg` - Rotated orientation with complex metadata, potential processing conflicts

**JFIF + EXIF DPI Conflict**

- `jpeg/critical_jfif_exif_dpi.jpg` - JFIF units:1 72 DPI with EXIF 200 DPI, conflicting resolution specifications

**XMP + IPTC Conflict**

- `jpeg/critical_xmp_iptc_conflict.jpg` - XMP and IPTC metadata with conflicting information, potential parsing issues

**XMP Complex Metadata**

- `jpeg/critical_xmp_complex.jpg` - Complex nested XMP structures with Dublin Core and custom namespaces

### PNG Variations

#### Single-Choice Factors

**Color Type**

- `png/colortype_grayscale.png` - 8-bit grayscale, single channel
- `png/colortype_palette.png` - 8-bit indexed color with palette
- `png/colortype_rgb.png` - 24-bit RGB true color
- `png/colortype_rgba.png` - 32-bit RGBA with alpha channel
- `png/colortype_grayscale_alpha.png` - 16-bit grayscale with alpha

**Interlacing**

- `png/interlace_none.png` - Standard sequential PNG
- `png/interlace_adam7.png` - Adam7 interlaced for progressive display

#### Numerical Factors

**Color Depth**

- `png/depth_1bit.png` - 1-bit monochrome bitmap
- `png/depth_8bit.png` - 8-bit per channel standard
- `png/depth_16bit.png` - 16-bit per channel high precision

**Compression Level**

- `png/compression_0.png` - No compression, fastest processing
- `png/compression_6.png` - Default compression level
- `png/compression_9.png` - Maximum compression, smallest file size

**Transparency Level (RGBA)**

- `png/alpha_opaque.png` - Fully opaque, alpha 255 throughout
- `png/alpha_semitransparent.png` - Mixed transparency, alpha 128 regions
- `png/alpha_transparent.png` - Areas with full transparency, alpha 0

#### Multi-Choice Factors (Individual)

**Filter Type Individual**

- `png/filter_none.png` - No filtering applied
- `png/filter_sub.png` - Sub filter for horizontal prediction
- `png/filter_up.png` - Up filter for vertical prediction
- `png/filter_average.png` - Average filter combining horizontal and vertical
- `png/filter_paeth.png` - Paeth predictor filter

**Metadata Chunk Individual**

- `png/metadata_none.png` - No text metadata chunks
- `png/metadata_text.png` - Simple text chunks included
- `png/metadata_compressed.png` - Compressed text chunks with deflate
- `png/metadata_international.png` - International text with UTF-8 encoding

**Auxiliary Chunk Individual**

- `png/chunk_gamma.png` - Gamma correction chunk included
- `png/chunk_background.png` - Background color chunk specified
- `png/chunk_transparency.png` - Transparency chunk for non-alpha images

#### Critical Combinations

**High Color Depth + Palette Conversion**

- `png/critical_16bit_palette.png` - 16-bit image forced to palette mode, major color loss

**Transparency + Color Space Conversion**

- `png/critical_alpha_grayscale.png` - RGBA converted to grayscale with alpha, color information lost

**Maximum Compression + Complex Filter**

- `png/critical_maxcompression_paeth.png` - Maximum compression with Paeth filter, processing intensive

**Interlacing + High Resolution**

- `png/critical_interlace_highres.png` - Adam7 interlacing on large image, memory intensive decoding

### GIF Variations

#### Single-Choice Factors

**Frame Count**
- `gif/single_frame.gif` - Single frame GIF (static image)
- `gif/multi_frame.gif` - Multi-frame animation (10 frames)

**Optimization**
- `gif/unoptimized.gif` - No frame optimization
- `gif/optimized.gif` - Frame difference optimization enabled

**Loop Count**
- `gif/no_loop.gif` - Single playback (loop count 1)
- `gif/infinite_loop.gif` - Infinite loop animation

#### Numerical Factors

**Frame Rate**
- `gif/slow_5fps.gif` - Slow animation (5 FPS, 200ms per frame)
- `gif/normal_10fps.gif` - Normal speed (10 FPS, 100ms per frame)
- `gif/fast_25fps.gif` - Fast animation (25 FPS, 40ms per frame)

**Palette Size**
- `gif/2colors.gif` - Minimal 2-color palette
- `gif/16colors.gif` - Limited 16-color palette
- `gif/256colors.gif` - Full 256-color palette

#### Multi-Choice Factors (Individual)

**Dithering Type**
- `gif/no_dither.gif` - No dithering applied
- `gif/floyd_steinberg.gif` - Floyd-Steinberg dithering
- `gif/ordered_dither.gif` - Ordered dithering pattern

**Critical Combinations**

**High Frame Rate + Limited Palette**
- `gif/critical_fast_2colors.gif` - 25 FPS with 2-color palette, extreme compression

**Many Frames + Small Palette + Dithering**
- `gif/critical_25frames_16colors_dither.gif` - Complex animation with heavy palette constraints

**Optimization + Complex Animation**
- `gif/critical_optimized_complex.gif` - Frame optimization with complex scene changes

## Critical Factor Combinations to Avoid

### Problematic Combinations (Require Special Attention)

1. **JPEG: CMYK + High Compression**
   - Issue: CMYK 4-channel format becomes unstable with high compression
   - Color gamut clipping and subsampling interaction problems
   - Recommendation: Test CMYK only with quality 70 or higher

2. **PNG: High Color Depth + Palette Conversion**
   - Issue: 48-bit to 8-bit palette conversion causes massive information loss
   - Color quantization algorithm variations and dithering effects
   - Recommendation: Test palette conversion only from 16-bit or lower

3. **Transparency + Color Space Conversion**
   - Issue: Alpha premultiplied colors in color space conversion
   - Transparent region color information changes
   - Recommendation: Limit to RGB → Grayscale only

4. **Progressive JPEG + Metadata**
   - Issue: EXIF placement in Progressive format
   - Metadata position/order changes and viewer compatibility issues

5. **JPEG: Exif Orientation + Complex Processing**
   - Issue: Image rotation through EXIF orientation tag can interfere with other image processing
   - Different software handles orientation differently (some rotate pixels, others just set metadata)
   - Recommendation: Test orientation handling in target environments thoroughly

6. **GIF: High Frame Rate + Small Palette**
   - Issue: Fast animation with limited colors causes severe dithering artifacts
   - Temporal coherence loss and flickering effects
   - Recommendation: Use larger palettes (64+ colors) for frame rates above 15 FPS

7. **GIF: Many Frames + Optimization**
   - Issue: Frame difference optimization with complex scenes
   - Can produce larger files than unoptimized versions
   - Recommendation: Test optimization benefit on a per-case basis

### Safe Combinations (Can Be Simplified)

1. **Similar Parameter Variations**: Quality steps can be reduced (30, 70 instead of 10, 30, 50, 70, 90)
2. **Independent Factors**: Compression level × color depth (PNG compression is independent of color depth)
3. **Metadata presence × quality settings**: No mutual influence

## Toolkit Command Structure

### Command 1: Original Image Generation and Testing

```bash
python toolkit.py generate-original [--test-compliance] [--output-dir OUTPUT]
```

- Generate ideal JPEG, PNG, and GIF source images
- Optionally test if generated images meet specifications
- Validate color spaces, bit depths, transparency, metadata presence, animation properties

### Command 2: Variation Generation and Testing  

```bash
python toolkit.py generate-variations [--source-dir SOURCE] [--output-dir OUTPUT] [--test-compliance]
```

- Generate all specified format variations from source images
- Create directory structure: `output/jpeg/`, `output/png/`, `output/gif/`, `output/webp/`, and `output/avif/`
- **Generate machine-readable index file: `output/index.json`**
- Optionally validate that each variation meets its requirements
- Test file format compliance and parameter verification

**Output Structure:**

```
output/
├── index.json              # Machine-readable metadata (103 entries)
├── test_original.jpg       # JPEG source image (640x480)
├── test_original.png       # PNG source image (480x480)
├── test_original.gif       # GIF source animation (200x200, 10 frames)
├── jpeg/                   # 36 JPEG variations (29 + 7 critical)
│   ├── colorspace_rgb.jpg
│   ├── quality_80.jpg
│   ├── orientation_6.jpg
│   ├── dpi_jfif_72dpi.jpg
│   ├── metadata_xmp.jpg
│   ├── metadata_iptc.jpg
│   └── ...
├── png/                    # 32 PNG variations (26 + 4 critical)
│   ├── colortype_rgba.png
│   ├── depth_16bit.png
│   └── ...
├── gif/                    # 21 GIF variations (18 + 3 critical)
│   ├── fps_fast.gif
│   ├── palette_2colors.gif
│   └── ...
├── webp/                   # 3 WebP variations (lossy, lossless, animation)
│   ├── lossy/original.webp
│   ├── lossless/original.webp
│   └── animation/original.webp
└── avif/                   # 3 AVIF variations (lossy, lossless, animation)
    ├── lossy/original.avif
    ├── lossless/original.avif
    └── animation/original.avif
```

### Command 3: Image Comparison

```bash
python toolkit.py compare-directories DIR_A DIR_B [--output-format {table,json,csv}] [--output-file FILE]
```

- Compare identical filenames across two directories
- Analyze: file size, resolution, PSNR(min), SSIM(min), frame count, frame rate
- **GIF Animation Support**: Frame-by-frame comparison with worst-frame quality assessment
- Report files present in A but not B, and vice versa
- Support multiple output formats for integration

### Command 4: Variation Validation

```bash
python toolkit.py validate-variations [--output-dir OUTPUT] [--report-file FILE]
```

- Validate all generated variations against their specifications
- **Comprehensive format support**: JPEG, PNG, GIF, WebP, and AVIF
- **Advanced validation features**:
  - WebP: Native PIL support for lossy/lossless/animation validation
  - AVIF: ImageMagick fallback validation when PIL support unavailable
  - Format-specific property validation (quality, compression, metadata)
  - Animation frame counting and format verification
- Generate detailed validation reports in JSON or text format
- **Robust error handling**: Graceful fallback for format-specific limitations

### Command 5: Testing and Validation (pytest-based)

```bash
# Run all tests
pytest

# Test original image generation
pytest tests/test_original_generation.py

# Test variation generation and validation
pytest tests/test_variation_generation.py

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

- **pytest-based test suite** for comprehensive validation
- Automated CI/CD integration with GitHub Actions  
- Test original image generation compliance
- Test variation generation and specification adherence
- **100% specification compliance verification through tests**

## Quality Validation Requirements

### Original Image Testing

- **JPEG Requirements Check**:
  - Color space is RGB (sRGB)
  - Quality level ≥ 95
  - Subsampling is 4:4:4
  - EXIF metadata presence
  - Orientation tag verification
  - Content diversity (frequency analysis)

- **PNG Requirements Check**:
  - Color type is RGBA (32-bit)
  - Alpha channel variation (transparency gradient)
  - No palette indexing
  - Compression level verification
  - Content elements presence (shapes, text, transparency)

- **GIF Requirements Check**:
  - Animation properties (frame count, frame rate)
  - Palette size and dithering settings
  - Loop count and optimization settings
  - Content elements presence (motion, color changes, text)

### Variation Testing

- **Format Compliance**: Each generated file opens correctly in standard libraries
- **Parameter Verification**: Image properties match intended specifications
- **Metadata Validation**: EXIF/chunk data matches requirements
- **File Size Reasonableness**: No unexpectedly large or corrupted files

### Comparison Metrics

- **File Size**: Byte-level comparison
- **Resolution**: Width × height verification
- **PSNR Calculation**: Peak Signal-to-Noise Ratio for quality assessment (minimum values for animations)
- **Structural Similarity**: SSIM index calculation (minimum values for animations)
- **Animation Metrics**: Frame count, frame rate (FPS), frame-by-frame quality analysis
- **File Presence Matrix**: Complete directory diff analysis

## Error Handling Requirements

### Generation Failures

- ImageMagick command execution failures
- Unsupported format conversion attempts
- Memory limitations with large images
- Invalid parameter combinations

### Validation Failures

- Source image specification non-compliance
- Variation generation parameter mismatches
- File corruption detection
- Metadata parsing errors

### Comparison Failures

- Missing file handling
- Format incompatibility (cannot calculate PSNR)
- Permission/access issues
- Memory constraints for large image comparisons

## Output and Reporting

### Generation Reports

- Success/failure status for each variation
- File size and processing time statistics
- Compliance test results summary
- Warning messages for critical combinations
- **Machine-readable index file (`index.json`)** for automated processing

### Machine-Readable Index Format

The `output/index.json` file contains comprehensive metadata for all generated images:

```json
[
  {
    "format": "jpeg|png|gif",
    "path": "relative/file/path",
    "jp": "日本語での説明",
    "en": "English description"
  }
]
```

#### Index File Features

- **Total entries**: 87 items (3 originals + 84 variations)
- **Format identification**: "jpeg", "png", or "gif"
- **Relative paths**: From output directory root
- **Bilingual descriptions**: Japanese and English explanations
- **UTF-8 encoding**: Full Unicode support for international text
- **Machine-friendly**: JSON format for easy parsing and automation

#### Index File Usage Examples

```bash
# Extract all JPEG variations
jq '.[] | select(.format == "jpeg")' output/index.json

# Find quality-related variations
jq '.[] | select(.path | contains("quality"))' output/index.json

# Get Japanese descriptions for transparency features
jq '.[] | select(.jp | contains("透明"))' output/index.json

# Extract all GIF animations
jq '.[] | select(.format == "gif")' output/index.json

# Find frame rate related variations
jq '.[] | select(.path | contains("fps"))' output/index.json
```

### Comparison Reports

- Tabular format showing side-by-side metrics
- File difference summaries (present/missing)
- Quality degradation analysis (PSNR trends)
- Processing performance metrics

### Validation Reports

- 100% specification compliance verification
- Detailed property analysis using ImageMagick
- JSON and text format output options
- Per-variation test results with pass/fail status

### Logging Requirements

- Detailed command execution logs
- Error stack traces for debugging
- Progress indicators for long operations
- Configurable verbosity levels

## Performance Considerations

### Optimization Strategies

- Parallel processing for independent variations
- Memory-efficient large image handling
- Incremental processing with resume capability
- Caching for repeated operations

### Resource Management

- Memory usage monitoring and limits
- Temporary file cleanup
- Process pool management for parallelization
- Disk space validation before operations

## Integration Requirements

### External Tool Dependencies

- **ImageMagick**: Version compatibility and feature verification (required for variations)
- **ImageMagick `identify`**: Accurate property detection for validation (required for 100% compliance)
- FFmpeg: Installation and PATH availability (optional)
- ExifTool: Optional metadata enhancement
- System libraries: libpng, libjpeg verification

### Python Environment

- Virtual environment setup recommendations
- Dependency version pinning
- Cross-platform compatibility (Windows, macOS, Linux)
- Package installation verification scripts

### Enhanced Validation System

- **16-bit PNG Generation**: OpenCV-based true 16-bit depth creation with sub-pixel noise
- **Accurate Property Detection**: ImageMagick `identify` command integration
- **100% Compliance Achievement**: All 90 variations pass specification requirements
- **Bilingual Documentation**: Japanese and English descriptions for international use

### Testing and CI/CD Integration

- **pytest-based Test Suite**: Comprehensive test coverage for all functionality
- **GitHub Actions CI**: Automated testing on push/PR events using Python 3.12
- **Dependency Management**: Automated system dependency installation (ImageMagick, etc.)
- **Coverage Reporting**: Test coverage tracking and reporting
- **Integration Testing**: End-to-end CLI command validation

**Test Categories:**
- **Original Image Generation Tests**: Specification compliance verification
- **Variation Generation Tests**: All format variations and index.json generation
- **Validation Tests**: Converted from `validate-variations` subcommand to pytest
- **Property Verification Tests**: Image format, resolution, metadata validation

**GitHub Workflow Debugging:**
- **Local debugging**: Use `wrkflw run -v .github/workflows/ci.yml` to debug workflow locally
- **Comprehensive CI**: Includes environment setup, dependency installation, test execution, and artifact archiving
- **Coverage Integration**: Automated coverage reporting with Codecov

### Automation and Workflow Integration

- **Machine-readable index**: JSON format for automated pipeline integration
- **Comprehensive validation**: Zero-failure specification compliance through tests
- **Multi-format reporting**: JSON, CSV, and tabular outputs for different use cases
- **Command-line interface**: Full automation support with detailed progress reporting
- **Continuous Integration**: Automated quality assurance on code changes

This comprehensive specification provides the foundation for developing a robust image processing toolkit that addresses all identified requirements for JPEG, PNG, and GIF format variation testing, with enhanced validation capabilities, animation support, automated testing, and CI/CD integration.
