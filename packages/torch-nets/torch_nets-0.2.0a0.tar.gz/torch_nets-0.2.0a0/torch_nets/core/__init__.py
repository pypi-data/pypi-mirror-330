
__module_name__ = "__init__.py"
__doc__ = """ __init__.py module for the API core."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# -- import network modules: -------------------------------------------------------------

from . import config

from ._layer_builder import LayerBuilder
from ._power_space import power_space