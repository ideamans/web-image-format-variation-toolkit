"""
Image variation validation module.

This module validates that generated image variations meet their specified requirements
according to the specifications in CLAUDE.md.
"""

import json
from pathlib import Path
from .validators.jpeg import JpegValidator, ValidationResult
from .validators.png import PngValidator
from .validators.gif import GifValidator


def validate_all_variations(output_dir="output"):
    """
    Validate all generated variations against their specifications.
    
    Args:
        output_dir (str): Directory containing generated variations
        
    Returns:
        dict: Validation results summary
    """
    output_path = Path(output_dir)
    jpeg_dir = output_path / "jpeg"
    png_dir = output_path / "png"
    gif_dir = output_path / "gif"
    
    results = {
        'total_tested': 0,
        'total_passed': 0,
        'total_failed': 0,
        'jpeg_results': [],
        'png_results': [],
        'gif_results': [],
        'summary': {}
    }
    
    print("Validating image variations against specifications...")
    print("=" * 60)
    
    # Validate JPEG variations
    if jpeg_dir.exists():
        jpeg_results = JpegValidator.validate_variations(jpeg_dir)
        results['jpeg_results'] = jpeg_results
        
        jpeg_passed = sum(1 for r in jpeg_results if r.passed)
        jpeg_failed = len(jpeg_results) - jpeg_passed
        
        print(f"\nJPEG Variations: {jpeg_passed}/{len(jpeg_results)} passed")
        results['summary']['jpeg'] = {'passed': jpeg_passed, 'failed': jpeg_failed, 'total': len(jpeg_results)}
    
    # Validate PNG variations
    if png_dir.exists():
        png_results = PngValidator.validate_variations(png_dir)
        results['png_results'] = png_results
        
        png_passed = sum(1 for r in png_results if r.passed)
        png_failed = len(png_results) - png_passed
        
        print(f"PNG Variations: {png_passed}/{len(png_results)} passed")
        results['summary']['png'] = {'passed': png_passed, 'failed': png_failed, 'total': len(png_results)}
    
    # Validate GIF variations
    if gif_dir.exists():
        gif_results = GifValidator.validate_variations(gif_dir)
        results['gif_results'] = gif_results
        
        gif_passed = sum(1 for r in gif_results if r.passed)
        gif_failed = len(gif_results) - gif_passed
        
        print(f"GIF Variations: {gif_passed}/{len(gif_results)} passed")
        results['summary']['gif'] = {'passed': gif_passed, 'failed': gif_failed, 'total': len(gif_results)}
    
    # Overall summary
    total_tested = len(results['jpeg_results']) + len(results['png_results']) + len(results['gif_results'])
    total_passed = sum(1 for r in results['jpeg_results'] + results['png_results'] + results['gif_results'] if r.passed)
    total_failed = total_tested - total_passed
    
    results['total_tested'] = total_tested
    results['total_passed'] = total_passed
    results['total_failed'] = total_failed
    
    print(f"\nOVERALL SUMMARY:")
    print(f"Total tested: {total_tested}")
    print(f"Total passed: {total_passed}")
    print(f"Total failed: {total_failed}")
    print(f"Success rate: {(total_passed/total_tested*100):.1f}%" if total_tested > 0 else "No tests")
    
    # Print failed tests
    failed_results = [r for r in results['jpeg_results'] + results['png_results'] + results['gif_results'] if not r.passed]
    if failed_results:
        print(f"\nFAILED TESTS ({len(failed_results)}):")
        print("-" * 40)
        for result in failed_results:
            print(f"❌ {result.filename}")
            for error in result.errors:
                print(f"   {error}")
    
    return results


def save_validation_report(results, output_file):
    """Save validation results to a file."""
    if output_file.endswith('.json'):
        # Convert results to JSON-serializable format
        json_data = {
            'summary': {
                'total_tested': results['total_tested'],
                'total_passed': results['total_passed'],
                'total_failed': results['total_failed'],
                'success_rate': (results['total_passed'] / results['total_tested'] * 100) if results['total_tested'] > 0 else 0
            },
            'category_summary': results['summary'],
            'detailed_results': {
                'jpeg': [r.to_dict() for r in results['jpeg_results']],
                'png': [r.to_dict() for r in results['png_results']],
                'gif': [r.to_dict() for r in results['gif_results']]
            }
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    else:
        # Text format report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("IMAGE VARIATION VALIDATION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total tested: {results['total_tested']}\n")
            f.write(f"Total passed: {results['total_passed']}\n")
            f.write(f"Total failed: {results['total_failed']}\n")
            f.write(f"Success rate: {(results['total_passed']/results['total_tested']*100):.1f}%\n\n")
            
            # Failed tests
            failed_results = [r for r in results['jpeg_results'] + results['png_results'] + results['gif_results'] if not r.passed]
            if failed_results:
                f.write(f"FAILED TESTS ({len(failed_results)}):\n")
                f.write("-" * 30 + "\n")
                for result in failed_results:
                    f.write(f"❌ {result.filename}\n")
                    for error in result.errors:
                        f.write(f"   {error}\n")
                    f.write("\n")
    
    print(f"Validation report saved to: {output_file}")


# Legacy function names for backward compatibility
def validate_jpeg_variations(jpeg_dir):
    """Legacy function - use JpegValidator.validate_variations instead."""
    return JpegValidator.validate_variations(jpeg_dir)


def validate_png_variations(png_dir):
    """Legacy function - use PngValidator.validate_variations instead."""
    return PngValidator.validate_variations(png_dir)


def validate_gif_variations(gif_dir):
    """Legacy function - use GifValidator.validate_variations instead."""
    return GifValidator.validate_variations(gif_dir)


if __name__ == "__main__":
    # Run validation if called directly
    results = validate_all_variations()
    save_validation_report(results, "validation_report.json")