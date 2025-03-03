# TODO

- [x] Add/update `dev` and `test` extras to `pyproject.toml`, 
- [x] Add/update an `all` extra that includes all dependencies
- [x] clean up `tests` folder
- [x] clean up `src/phiton/` folder, remove unused/unneeded files.

## Code Quality Tasks

- [ ] Fix linting issues:
  - [ ] Fix shebang issues (EXE001) - make files executable or remove shebangs
  - [ ] Update deprecated typing imports (UP035) - replace `typing.Dict` with `dict`, etc.
  - [ ] Fix module level imports not at top of file (E402)
  - [ ] Fix boolean-typed positional arguments (FBT001, FBT002) - make them keyword-only
  - [ ] Refactor complex functions (C901) - break down functions with complexity > 10
  - [ ] Fix functions with too many arguments (PLR0913)
  - [ ] Fix functions with too many branches (PLR0912)
  - [ ] Fix functions with too many statements (PLR0915)
  - [ ] Fix functions with too many return statements (PLR0911)
  - [ ] Fix blind exception catching (BLE001) - specify exception types
  - [ ] Fix shadowing of built-in names (A001) - rename variables like `iter` and `type`
  - [ ] Fix unnecessary `elif` after `return` statements (RET505)
  - [x] Add `__init__.py` to tests directory to fix implicit namespace package issues (INP001)
  - [ ] Fix variable naming conventions (N806) - use lowercase for variables

## Test Improvements

- [x] Fix pytest configuration:
  - [x] Resolve the conflict between pytest.ini and pyproject.toml pytest configuration
  - [x] Fix the `--cov=phiton` argument (should be `--cov=src/phiton`)

- [ ] Fix test failures:
  - [x] Fix indentation error in test_optimize_imports
  - [ ] Fix test_config_level_range - level validation issue
  - [ ] Fix test_compress_simple_level1 and test_compress_simple_level5 - expected output mismatch
  - [ ] Fix test_compression_levels - level 4 produces larger output than level 3
  - [ ] Fix test_config_options - comment settings not affecting output

## Feature Enhancements

- [ ] Implement decompression functionality (Phiton to Python)
- [ ] Add support for more complex patterns
- [ ] Add support for custom pattern definitions
- [ ] Create a web interface for online conversion

## Documentation

- [ ] Add more examples to README.md
- [ ] Create detailed API documentation
- [ ] Add contributing guidelines

## Completed Tasks

- Added comprehensive dependencies to `dev` and `test` extras in `pyproject.toml`
- Created an `all` extra that includes all dependencies
- Removed redundant requirements.txt from tests folder
- Moved test files (test1.py, test2.py, test_refactored.py, test1.phi) to tests directory
- Created examples directory and moved example files (example.py, example.phi) there
- Removed .DS_Store files
- Added `__init__.py` to tests directory to fix implicit namespace package issues
- Removed redundant pytest.ini file since the configuration is already in pyproject.toml
- Verified that the coverage configuration in pyproject.toml is correct
- Fixed indentation error in test_optimize_imports