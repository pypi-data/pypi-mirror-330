# pip-cleanup 📦

A Python tool to clean up unused pip packages from your Python environment.

## Features

- Scans your Python project for imported packages
- Compares against installed packages
- Identifies unused dependencies
- Interactive removal of unused packages

## Installation

```bash
pip install pip-cleanup
```

## Usage

1. Navigate to your Python project directory

2. Run pip-cleanup:

```bash
pip-cleanup
```

Or specify a custom path:

```bash
pip-cleanup --path /path/to/project
```

## Example Output

```bash
$ pip-cleanup

╔═════════════════════════════════╗
║             📦 PIP-CLEANUP 📦             ║
╚═════════════════════════════════╝

Scanning project...
Found unused packages:
- package1
- package2
- package3

Would you like to remove these packages? [y/N]
```

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

## License

MIT License