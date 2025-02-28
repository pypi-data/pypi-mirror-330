import sqlalchemy as sa
from distutils.version import StrictVersion as V

# from packaging import version as V

SA_VERSION = V(sa.__version__)

SA_1_1 = V("1.1a0")
