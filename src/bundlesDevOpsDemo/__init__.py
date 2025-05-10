__version__ = "0.0.1"

# Import everything from main module
from .main import *

# Create a special get_taxis function directly in the main object
# This is a hack to support the DLT pipeline which uses main.get_taxis()
def get_taxis(spark):
    from .main import get_taxis as original_get_taxis
    return original_get_taxis(spark)

# Add the get_taxis function to the main function as an attribute
main.get_taxis = get_taxis
