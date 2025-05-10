__version__ = "0.0.1"

# Import and expose main module
from . import main as main_module

# For entry point compatibility
main = main_module.main
