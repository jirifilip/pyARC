import sys
import importlib.util

package_name = 'fim'

spec = importlib.util.find_spec(package_name)
if spec is None:
    raise Exception("Before using pyARC, the 'fim' package must be installed first. For installation guide, please refer to http://www.borgelt.net/pyfim.html.")

from .cba import CBA
from .data_structures import TransactionDB