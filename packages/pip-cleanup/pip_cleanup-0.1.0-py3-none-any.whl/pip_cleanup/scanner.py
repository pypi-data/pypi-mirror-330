import os
import subprocess
import ast
from typing import Set, Dict, Optional, List
import pkg_resources
import sys
from pathlib import Path

def get_project_requirements(root_dir: str) -> Set[str]:
    """
    Get required packages from requirements.txt, setup.py, or pyproject.toml
    Returns a set of package names that are declared as requirements.
    """
    requirements = set()
    
    # Check requirements.txt
    req_files = ['requirements.txt', 'requirements/base.txt', 'requirements/prod.txt']
    for req_file in req_files:
        req_path = os.path.join(root_dir, req_file)
        if os.path.exists(req_path):
            try:
                with open(req_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Remove version specifiers
                            package = line.split('==')[0].split('>=')[0].split('<=')[0].split('~=')[0].strip()
                            requirements.add(package.lower())
            except Exception as e:
                print(f"\nWarning: Error reading {req_file}: {e}", file=sys.stderr)
    
    # Check setup.py
    setup_path = os.path.join(root_dir, 'setup.py')
    if os.path.exists(setup_path):
        try:
            with open(setup_path, 'r') as f:
                content = f.read()
                # Simple parsing for install_requires
                if 'install_requires' in content:
                    # Extract packages from install_requires list
                    for line in content.split('install_requires')[1].split('[')[1].split(']')[0].split(','):
                        package = line.strip().strip('"\'').split('>=')[0].split('==')[0].strip()
                        if package:
                            requirements.add(package.lower())
        except Exception as e:
            print(f"\nWarning: Error reading setup.py: {e}", file=sys.stderr)
    
    return requirements

def get_installed_packages() -> Dict[str, str]:
    """
    Get a list of installed packages using pkg_resources.
    Returns a dictionary of package names and their versions.
    """
    packages = {}
    for dist in pkg_resources.working_set:
        packages[dist.key.lower()] = dist.version
    return packages

def find_imports_in_file(filepath: str) -> Set[str]:
    """
    Find all imports in a single Python file.
    Returns a set of imported module names.
    """
    imports = set()
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            tree = ast.parse(file.read(), filename=filepath)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split(".")[0].lower())
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0].lower())
    except Exception as e:
        print(f"\nWarning: Error parsing {filepath}: {e}", file=sys.stderr)
    return imports

def find_imports_in_directory(root_dir: str, exclude_dirs: Optional[Set[str]] = None) -> Set[str]:
    """
    Recursively find all imports in Python files under the given root directory.
    Returns a set of imported module names.
    """
    if exclude_dirs is None:
        exclude_dirs = {'.git', '.venv', 'venv', '__pycache__', 'env', '.env'}
    
    imports = set()
    root_path = Path(root_dir)
    
    for filepath in root_path.rglob("*.py"):
        # Skip excluded directories
        if any(part in exclude_dirs for part in filepath.parts):
            continue
        
        imports.update(find_imports_in_file(str(filepath)))
    
    # Add some common package name mappings
    package_mappings = {
        'PIL': 'pillow',
        'cv2': 'opencv-python',
        'sklearn': 'scikit-learn',
        'yaml': 'pyyaml',
    }
    
    # Apply mappings
    mapped_imports = set()
    for imp in imports:
        mapped_imports.add(package_mappings.get(imp, imp))
    
    return mapped_imports

def get_package_size(package_name: str) -> Optional[int]:
    """
    Get the size of an installed package in bytes.
    Returns None if the package size cannot be determined.
    """
    try:
        dist = pkg_resources.get_distribution(package_name)
        if dist.location:
            package_path = os.path.join(dist.location, dist.key)
            if os.path.exists(package_path):
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(package_path):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        total_size += os.path.getsize(fp)
                return total_size
    except Exception:
        pass
    return None

def format_size(size_in_bytes: int) -> str:
    """
    Format a size in bytes to a human-readable string.
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.1f}{unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.1f}GB" 