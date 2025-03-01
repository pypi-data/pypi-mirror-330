
__module_name__ = "_power_space.py"
__doc__ = """power space function for encoder / decoder formulation."""
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# -- import packages: --------------------------------------------------------------------
from itertools import groupby
from typing import Union, Any
import numpy as np


# -- Supporting functions: ---------------------------------------------------------------
def power_space(start: int, stop: int, n: int, power: Union[int, float]):
    """
    Return integered-powered space.

    Parameters:
    -----------
    start
        first term of the power-space array.
        type: int

    stop
        final term of the power-space array.
        type: int

    n
        type: int
        length of array to be created

    power
        type: Union[int, float]
        power at which the space should decay / expand.

    Returns:
    --------
    power-spaced array
        type: np.ndarray
    """
    start_ = np.power(start, 1 / float(power))
    stop_  = np.power(stop, 1 / float(power))

    pspace = np.power(np.linspace(start_, stop_, num=n), power).astype(int)
    pspace[0], pspace[-1] = start, stop
    
    return pspace