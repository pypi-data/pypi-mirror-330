import os
import sys
import click
from colorama import init, Fore, Style
from tabulate import tabulate
from typing import Dict, Set, List, Tuple
from .scanner import (
    get_installed_packages,
    find_imports_in_directory,
    get_package_size,
    format_size,
    get_project_requirements
)

# Initialize colorama for Windows support
init()

def print_header():
    """Print a stylish header for the tool."""
    header = """
╔═══════════════════════════════════════╗
║          📦 PIP-CLEANUP 📦            ║
║    Find and remove unused packages    ║
╚═══════════════════════════════════════╝
    """
    click.echo(Fore.CYAN + header + Style.RESET_ALL)

def get_unused_packages(root_dir: str) -> List[Tuple[str, str, str]]:
    """
    Get a list of unused packages with their versions and sizes.
    Returns a list of tuples (package_name, version, size).
    """
    click.echo(Fore.YELLOW + "\n🔍 Scanning for installed packages..." + Style.RESET_ALL)
    installed_packages = get_installed_packages()
    
    click.echo(Fore.YELLOW + "🔍 Scanning for imports in your code..." + Style.RESET_ALL)
    used_packages = find_imports_in_directory(root_dir)
    
    click.echo(Fore.YELLOW + "🔍 Checking project requirements..." + Style.RESET_ALL)
    required_packages = get_project_requirements(root_dir)
    
    # Get unused packages with their details
    unused_packages = []
    essential_packages = {'pip', 'setuptools', 'wheel', 'pip-cleanup'}
    
    for package, version in installed_packages.items():
        # Skip if package is:
        # 1. Being used in code
        # 2. Listed in requirements
        # 3. An essential package
        if (package not in used_packages and 
            package not in required_packages and 
            package not in essential_packages):
            size = get_package_size(package)
            size_str = format_size(size) if size else "Unknown"
            unused_packages.append((package, version, size_str))
    
    return sorted(unused_packages, key=lambda x: x[0].lower())

def display_packages(packages: List[Tuple[str, str, str]]):
    """Display packages in a formatted table."""
    if not packages:
        click.echo(Fore.GREEN + "\n✨ No unused packages found!" + Style.RESET_ALL)
        return
    
    headers = ["#", "Package", "Version", "Size"]
    table_data = [
        [idx + 1, Fore.CYAN + pkg + Style.RESET_ALL, ver, size]
        for idx, (pkg, ver, size) in enumerate(packages)
    ]
    
    click.echo("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))

def confirm_deletion(packages: List[Tuple[str, str, str]]) -> List[str]:
    """
    Let user select packages to uninstall.
    Returns a list of package names to uninstall.
    """
    while True:
        click.echo("\nEnter package numbers to uninstall (comma-separated), 'all' to select all, or 'q' to quit:")
        choice = click.prompt("→", type=str).strip().lower()
        
        if choice == 'q':
            return []
        
        if choice == 'all':
            return [pkg[0] for pkg in packages]
        
        try:
            indices = [int(idx.strip()) - 1 for idx in choice.split(",") if idx.strip()]
            selected = []
            for idx in indices:
                if 0 <= idx < len(packages):
                    selected.append(packages[idx][0])
                else:
                    click.echo(Fore.RED + f"Invalid number: {idx + 1}" + Style.RESET_ALL)
                    break
            else:
                return selected
        except ValueError:
            click.echo(Fore.RED + "Invalid input. Please enter numbers separated by commas." + Style.RESET_ALL)

def uninstall_packages(packages: List[str]):
    """Uninstall the selected packages."""
    if not packages:
        return
    
    click.echo("\n" + Fore.YELLOW + "🗑️  Uninstalling packages..." + Style.RESET_ALL)
    for package in packages:
        try:
            click.echo(f"Removing {Fore.CYAN}{package}{Style.RESET_ALL}...")
            os.system(f"{sys.executable} -m pip uninstall -y {package}")
        except Exception as e:
            click.echo(Fore.RED + f"Error uninstalling {package}: {e}" + Style.RESET_ALL)
    
    click.echo(Fore.GREEN + "\n✨ Uninstallation complete!" + Style.RESET_ALL)

@click.command()
@click.option('--path', '-p', default=".",
              help="Directory to scan for Python files (default: current directory)")
def main(path: str):
    """Find and remove unused pip packages in your Python projects."""
    print_header()
    
    # Validate directory
    if not os.path.isdir(path):
        click.echo(Fore.RED + f"Error: Directory '{path}' does not exist." + Style.RESET_ALL)
        sys.exit(1)
    
    # Get and display unused packages
    unused_packages = get_unused_packages(path)
    display_packages(unused_packages)
    
    if unused_packages:
        # Get user selection and uninstall
        to_uninstall = confirm_deletion(unused_packages)
        if to_uninstall:
            uninstall_packages(to_uninstall)

if __name__ == "__main__":
    main() 