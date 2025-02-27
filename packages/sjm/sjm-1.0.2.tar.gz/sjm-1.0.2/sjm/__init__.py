import logging
import pkg_resources  # Helps fetch metadata from installed package

try:
    __version__ = pkg_resources.get_distribution("sjm").version
    __author__ = pkg_resources.get_distribution("sjm").metadata["Author"]
    __email__ = pkg_resources.get_distribution("sjm").metadata["Author-email"]
except pkg_resources.DistributionNotFound:
    __version__ = "unknown"
    __author__ = "unknown"
    __email__ = "unknown"

# Setup logging
logging.basicConfig(level=logging.INFO)

def version():
    """Return the installed version of SJM."""
    return f"SJM version {__version__}"

# Print version on import (optional)
logging.info(f"SJM package (v{__version__}) initialized")

