# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Refactored codebase into a proper module structure
- Created `ConversionConfig` dataclass for configuration
- Added multiple compression levels (1-5)
- Added comprehensive CLI with preview functionality
- Added detailed compression statistics
- Added proper documentation
- Added test files
- Added comprehensive dependency management with dev, test, and all extras
- Created examples directory for example files
- Added `__init__.py` to tests directory to fix namespace package issues

### Changed

- Improved compression algorithm with enhanced symbol substitution
- Optimized imports handling
- Added pattern recognition for common code patterns
- Enhanced final optimization pass
- Reorganized project structure with proper src, tests, and examples directories
- Consolidated pytest configuration in pyproject.toml

### Fixed

- Fixed import issues
- Fixed type hints in CLI statistics
- Fixed indentation error in test_optimize_imports
- Removed redundant configuration files
- Cleaned up unused and unneeded files

## [0.0.post1] - 2025-03-02

### Added

- Initial version with basic functionality
- Python to Phiton conversion
- Symbol mappings
- Basic CLI 
