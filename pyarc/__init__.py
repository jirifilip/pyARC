try:
    import fim
except Exception:
    raise Exception("Before using pyARC, the fim package must be installed first." + 
    " For installation guide, please refer to http://www.borgelt.net/pyfim.html or https://pyfim.readthedocs.io/en/latest/source/install.html")

from .CBA import *
from .data_structures import TransactionDB