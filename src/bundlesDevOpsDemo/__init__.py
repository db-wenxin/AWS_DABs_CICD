__version__ = "0.0.1"

# Import main module and expose it as a module
from . import main
# Also import the main function from main module as a package-level entry point
from .main import main as _main_func

# Assign main function to package-level main name to support as an entry point
main = _main_func
