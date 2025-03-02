"""
Provider registry and base classes
"""
import importlib
import pkgutil
from pathlib import Path
from .base import Provider, get_provider  # noqa: F401
import warnings

# Suppress Pydantic warning about built-in function types
warnings.filterwarnings("ignore", message=".*is not a Python type.*")

# Automatically import all modules in the providers package
package_dir = Path(__file__).resolve().parent
for (_, module_name, _) in pkgutil.iter_modules([str(package_dir)]):
    # Skip importing base module since it's already imported
    if module_name != 'base':
        importlib.import_module(f"{__package__}.{module_name}")

__all__ = ["Provider", "get_provider"]