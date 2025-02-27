try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata
from .client import IPFClient

__version__ = metadata.version("mini_ipfabric")

__all__ = ["IPFClient"]
