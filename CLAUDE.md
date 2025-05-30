# Image Processing Toolkit Requirements

## Project Overview

This project aims to develop a Python-based image processing toolkit for generating and testing various image format variations, specifically focusing on JPEG and PNG formats. The toolkit will be used to create comprehensive test datasets for image conversion library development.

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

## Core Functionality

The toolkit consists of three main components:

### 1. Original Image Generation and Testing
Generate ideal source images that meet specific requirements for comprehensive format variation testing.

### 2. Variation Generation and Testing
Create all specified format variations from source images and validate they meet requirements.

### 3. Image Comparison
Compare identical images across different directories, analyzing file size, resolution, PSNR, and file presence/absence.

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

**Note**: For complete source code implementation of the image generation functions described below, refer to `generation.md` which contains the full Python code with detailed explanations and usage instructions.

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

**ICC Profile Individual**
- `jpeg/icc_none.jpg` - No color profile embedded
- `jpeg/icc_srgb.jpg` - Standard sRGB color profile
- `jpeg/icc_adobergb.jpg` - Adobe RGB wide gamut profile

#### Critical Combinations

**CMYK + High Compression**
- `jpeg/critical_cmyk_lowquality.jpg` - CMYK colorspace with aggressive compression, quality 30

**Progressive + Rich Metadata**
- `jpeg/critical_progressive_fullmeta.jpg` - Progressive encoding with complete EXIF and GPS data

**Thumbnail + Progressive**
- `jpeg/critical_thumbnail_progressive.jpg` - Progressive JPEG with embedded thumbnail, potential compatibility issues

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

### Safe Combinations (Can Be Simplified)

1. **Similar Parameter Variations**: Quality steps can be reduced (30, 70 instead of 10, 30, 50, 70, 90)
2. **Independent Factors**: Compression level × color depth (PNG compression is independent of color depth)
3. **Metadata presence × quality settings**: No mutual influence

## Toolkit Command Structure

### Command 1: Original Image Generation and Testing
```bash
python toolkit.py generate-original [--test-compliance]
```
- Generate ideal JPEG and PNG source images
- Optionally test if generated images meet specifications
- Validate color spaces, bit depths, transparency, metadata presence

### Command 2: Variation Generation and Testing  
```bash
python toolkit.py generate-variations [--source-dir SOURCE] [--output-dir OUTPUT] [--test-compliance]
```
- Generate all specified format variations from source images
- Create directory structure: `output/jpeg/` and `output/png/`
- Optionally validate that each variation meets its requirements
- Test file format compliance and parameter verification

### Command 3: Image Comparison
```bash
python toolkit.py compare-directories DIR_A DIR_B [--output-format {table,json,csv}]
```
- Compare identical filenames across two directories
- Analyze: file size, resolution, PSNR values
- Report files present in A but not B, and vice versa
- Support multiple output formats for integration

## Quality Validation Requirements

### Original Image Testing
- **JPEG Requirements Check**:
  - Color space is RGB (sRGB)
  - Quality level ≥ 95
  - Subsampling is 4:4:4
  - EXIF metadata presence
  - Content diversity (frequency analysis)

- **PNG Requirements Check**:
  - Color type is RGBA (32-bit)
  - Alpha channel variation (transparency gradient)
  - No palette indexing
  - Compression level verification
  - Content elements presence (shapes, text, transparency)

### Variation Testing
- **Format Compliance**: Each generated file opens correctly in standard libraries
- **Parameter Verification**: Image properties match intended specifications
- **Metadata Validation**: EXIF/chunk data matches requirements
- **File Size Reasonableness**: No unexpectedly large or corrupted files

### Comparison Metrics
- **File Size**: Byte-level comparison
- **Resolution**: Width × height verification
- **PSNR Calculation**: Peak Signal-to-Noise Ratio for quality assessment
- **Structural Similarity**: Optional SSIM index calculation
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

### Comparison Reports
- Tabular format showing side-by-side metrics
- File difference summaries (present/missing)
- Quality degradation analysis (PSNR trends)
- Processing performance metrics

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
- ImageMagick: Version compatibility and feature verification
- FFmpeg: Installation and PATH availability
- ExifTool: Optional metadata enhancement
- System libraries: libpng, libjpeg verification

### Python Environment
- Virtual environment setup recommendations
- Dependency version pinning
- Cross-platform compatibility (Windows, macOS, Linux)
- Package installation verification scripts

This comprehensive specification provides the foundation for developing a robust image processing toolkit that addresses all identified requirements for JPEG and PNG format variation testing.
