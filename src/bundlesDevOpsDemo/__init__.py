__version__ = "0.0.1"

# Direct alias for the main module to support both import patterns
import sys
from . import main as _temp_main_module

# Replace main function reference with module reference
# This is critical for the DLT pipeline which uses main.get_taxis()
sys.modules[__name__].main = _temp_main_module

# Also expose entry point function for Databricks jobs
def main():
    return _temp_main_module.main()
