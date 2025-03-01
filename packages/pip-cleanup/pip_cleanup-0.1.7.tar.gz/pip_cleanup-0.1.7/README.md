# pip-cleanup 📦

A Python tool to clean up unused pip packages from your Python environment.

## Features

- Scans your Python project for imported packages
- Compares against installed packages
- Identifies unused dependencies
- Interactive removal of unused packages
- Generates requirements.txt with only used packages
- Supports JSON output for automation
- Configurable directory exclusions and package ignores

## Installation

```bash
pip install pip-cleanup
```

## Usage

1. Navigate to your Python project directory or activated environment

2. Run pip-cleanup:

```bash
pip-cleanup
```

### Available Options

```bash
# Show help message and available options
pip-cleanup --help

# Check version (any of these work)
pip-cleanup -v
pip-cleanup -V
pip-cleanup --version

# Scan a specific directory
pip-cleanup --path /path/to/project
pip-cleanup -p /path/to/project

# Exclude directories from scanning
pip-cleanup --exclude tests --exclude docs
pip-cleanup -e tests -e docs

# Ignore specific packages
pip-cleanup --ignore pytest --ignore black
pip-cleanup -i pytest -i black

# Generate requirements.txt with only used packages
pip-cleanup --requirements
pip-cleanup -r

# Output in JSON format (useful for scripts)
pip-cleanup --json

# Disable colored output
pip-cleanup --no-color

# Suppress non-essential output
pip-cleanup --quiet
pip-cleanup -q
```

### How It Works

1. **Project Scanning**: The tool scans your Python files for import statements
2. **Package Analysis**: Compares found imports against installed packages
3. **Smart Detection**: 
   - Handles both direct imports (import numpy) and from imports (from PIL import Image)
   - Recognizes common package aliases (e.g., PIL -> pillow)
   - Excludes standard library packages
4. **Interactive Cleanup**: Lets you choose which packages to remove
5. **Requirements Generation**: Can create requirements.txt with only used packages

## Example Output

```bash
$ pip-cleanup

╔═══════════════════════════════════════╗
║          📦 PIP-CLEANUP 📦            ║
║    Find and remove unused packages    ║
╚═══════════════════════════════════════╝

🔍 Scanning for installed packages...
🔍 Scanning for imports in your code...

Found unused packages:
#  Package    Version  Size
1  package1   1.2.3    5.2MB
2  package2   0.4.2    1.1MB
3  package3   2.0.0    3.4MB

Enter package numbers to uninstall (comma-separated), 'all' to select all, or 'q' to quit:
```

## Notes

- Essential packages (pip, setuptools, wheel) are automatically excluded
- The tool respects your project's requirements.txt and setup.py dependencies
- Virtual environment friendly - works with both global and virtual environments
- Use --exclude to skip test directories or other non-relevant code
- Use --ignore to keep packages that might be used indirectly
- Use --json for integration with other tools or scripts
- Use --requirements to update your requirements.txt automatically

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

MIT License