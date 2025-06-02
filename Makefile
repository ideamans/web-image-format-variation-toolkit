# Image Processing Toolkit Makefile

.PHONY: help install test test-original test-variations test-all clean lint format check-deps output

help:
	@echo "Available commands:"
	@echo "  install       Install dependencies"
	@echo "  test          Run all tests"
	@echo "  test-original Run original image generation tests"
	@echo "  test-variations Run variation generation and validation tests"
	@echo "  test-all      Run all tests with coverage"
	@echo "  output        Run tests and generate complete output"
	@echo "  clean         Clean up temporary files"
	@echo "  lint          Run code linting"
	@echo "  format        Format code with black"
	@echo "  check-deps    Check system dependencies"

install:
	pip install -r requirements.txt

check-deps:
	@echo "Checking system dependencies..."
	@python -c "import PIL; print(f'✓ Pillow {PIL.__version__}')" || echo "✗ Pillow not installed"
	@python -c "import cv2; print(f'✓ OpenCV {cv2.__version__}')" || echo "✗ OpenCV not installed"
	@python -c "import numpy; print(f'✓ NumPy {numpy.__version__}')" || echo "✗ NumPy not installed"
	@python -c "import piexif; print('✓ piexif')" || echo "✗ piexif not installed"
	@python -c "import noise; print('✓ noise')" || echo "✗ noise not installed"
	@magick -version > /dev/null 2>&1 && echo "✓ ImageMagick (magick)" || convert -version > /dev/null 2>&1 && echo "✓ ImageMagick (convert)" || echo "✗ ImageMagick not found"

test-original:
	pytest tests/test_original_generation.py -v

test-variations:
	pytest tests/test_variation_generation.py -v

test-detailed:
	pytest tests/test_detailed_validation.py -v

test:
	pytest tests/ -v

test-all:
	pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v

clean:
	rm -rf output/
	rm -rf test_output/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

lint:
	flake8 src/ tests/ toolkit.py --max-line-length=100 --ignore=E203,W503

format:
	black src/ tests/ toolkit.py --line-length=100

# Integration tests
integration-test:
	@echo "Running integration tests..."
	python toolkit.py generate-original --output-dir test_output --test-compliance
	python toolkit.py generate-variations --source-dir test_output --output-dir test_output
	@echo "✓ Integration tests passed"

# Development workflow
dev-setup: install check-deps
	@echo "Development environment setup complete"

dev-test: clean test-all integration-test
	@echo "Full development test suite completed"

# Production output generation
output:
	@echo "Starting production output generation..."
	@echo "Step 1: Running all tests..."
	pytest tests/ -v
	@echo "Step 2: Tests passed! Generating original images..."
	python toolkit.py generate-original --output-dir output
	@echo "Step 3: Generating variations..."
	python toolkit.py generate-variations --source-dir output --output-dir output
	@echo "✓ Complete output generation finished successfully!"
	@echo "Generated files are in the 'output/' directory"