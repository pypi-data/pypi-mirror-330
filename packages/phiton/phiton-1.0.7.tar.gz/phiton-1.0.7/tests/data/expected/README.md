# Expected Output Files

This directory contains expected output files for testing Phiton conversion.

## File Naming Convention

Files are named according to the following convention:

- `{source_file_name}_level{compression_level}.phi`

For example:
- `simple_level1.phi`: Expected output for `simple.py` with compression level 1
- `simple_level5.phi`: Expected output for `simple.py` with compression level 5

## Adding New Expected Files

When adding new test cases:

1. Create a Python file in the parent directory
2. Run Phiton conversion on the file with the desired compression level
3. Save the output to this directory with the appropriate naming convention
4. Update the tests to use the new expected output file

## Updating Expected Files

If the Phiton conversion algorithm changes, the expected output files may need to be updated. To update them:

1. Run Phiton conversion on the source files with the desired compression levels
2. Compare the output with the existing expected files
3. Update the expected files if the changes are intentional 