# Guide for Publishing wcgw-agent 3.1.0 to PyPI

This document outlines the steps to publish the Windows-compatible version of wcgw-agent to PyPI.

## Prerequisites

- PyPI account with appropriate permissions
- Build tools already installed (`build` and `twine`)
- Token for authentication with PyPI

## Completed Steps

- ✅ Updated version number in `pyproject.toml` to 3.1.0
- ✅ Updated CHANGELOG.md with Windows compatibility changes
- ✅ Modified project metadata to include Windows classifiers
- ✅ Built the distribution packages with `python -m build`
- ✅ Verified the packages with `twine check dist/*`

## Next Steps for PyPI Upload

1. **Tag the Git Release**

   ```bash
   git add .
   git commit -m "Prepare 3.1.0 release of wcgw-agent with Windows compatibility"
   git tag -a v3.1.0 -m "Windows compatibility release for wcgw-agent"
   git push origin v3.1.0
   ```

2. **Upload to PyPI**

   Use one of these authentication methods:

   **Option A: Upload with PyPI token**
   ```bash
   twine upload --username "__token__" --password "your-pypi-token" dist/*
   ```

   **Option B: Create a .pypirc file**
   
   Create/edit `~/.pypirc`:
   ```
   [distutils]
   index-servers =
       pypi

   [pypi]
   username = __token__
   password = your-pypi-token
   ```

   Then upload:
   ```bash
   twine upload dist/*
   ```

3. **Verify Installation**

   Test the installation from PyPI:
   ```bash
   pip install --upgrade wcgw-agent
   ```

   Verify the version:
   ```bash
   pip show wcgw-agent
   ```

## Post-Release

1. **Create GitHub Release**

   - Go to Releases on GitHub
   - Create a new release using tag v3.1.0
   - Copy release notes from CHANGELOG.md
   - Publish the release

2. **Announce the Release**

   - Document where and how to announce the new Windows-compatible version

## Troubleshooting

If you encounter authentication issues:

- Verify your PyPI token has the correct scope (upload)
- Try using a .pypirc file instead of command-line credentials
- Check the token expiration date

If upload fails:

- Check if another package with the same name and version exists
- Verify you have proper permissions for the package

## Windows-Specific Notes

The 3.1.0 release includes these key Windows compatibility features:

- Platform abstraction layer for OS detection
- Windows shell handler implementation
- Windows background process management 
- Fixed path handling for Windows
- Terminal attachment mechanisms for interactive usage

These changes ensure the package works seamlessly across Windows, Linux, and macOS platforms.