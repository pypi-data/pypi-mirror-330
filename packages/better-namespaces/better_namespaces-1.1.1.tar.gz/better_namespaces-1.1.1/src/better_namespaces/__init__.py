# read version from installed package
from importlib.metadata import version
__version__ = version(__name__)

# populate package namespace
from better_namespaces.context_group import NamespaceGroup