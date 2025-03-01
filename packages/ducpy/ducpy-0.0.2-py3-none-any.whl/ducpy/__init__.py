"""Main module for duc_py package.

Import usage examples:
    import duc_py as duc
    
    # Access modules directly:
    duc.classes.SomeClass
    duc.parse.parse_function
    duc.serialize.serialize_function
    duc.utils.some_utility
    
    # Access types directly:
    point = duc.Point(x=10, y=20)
"""

# Import from Duc
from . import Duc

# Import modules for direct access
from . import utils
from . import parse
from . import serialize
from . import classes
from . import tests
