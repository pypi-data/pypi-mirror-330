# Publishing to PyPI

This document outlines the steps to build and publish the WCGW package to PyPI.

## Prerequisites

- Python 3.11 or higher
- Build tools: `pip install -U build twine`
- PyPI account with appropriate permissions

## Building the Package

1. Update version number in `pyproject.toml`
2. Make sure all changes are documented in `CHANGELOG.md`
3. Ensure all tests pass:

   ```
   python -m pytest
   ```

4. Build the package:

   ```
   python -m build
   ```

   This will create distribution files in the `dist/` directory.

5. Verify the build:

   ```
   twine check dist/*
   ```

## Testing the Package

Before uploading to PyPI, it's a good idea to test the package on TestPyPI:

1. Upload to TestPyPI:

   ```
   twine upload --repository testpypi dist/*
   ```

2. Install from TestPyPI in a clean environment:

   ```
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ wcgw
   ```

3. Test basic functionality.

## Publishing to PyPI

Once you've verified the package works correctly:

1. Upload to PyPI:

   ```
   twine upload dist/*
   ```

2. Verify the package is available:

   ```
   pip install wcgw
   ```

## Platform-Specific Considerations

### Windows

- Ensure the package installs and works correctly on Windows.
- Test with both PowerShell and Command Prompt.
- Verify the background process management system works as expected.

### macOS/Linux

- Test with both Bash and Zsh shells.
- Verify screen functionality for terminal attachment.

## Post-Release

1. Tag the release in Git:

   ```
   git tag -a v3.1.0 -m "Windows compatibility release"
   git push origin v3.1.0
   ```

2. Create a GitHub release with release notes from the changelog.

3. Announce the release in appropriate channels.