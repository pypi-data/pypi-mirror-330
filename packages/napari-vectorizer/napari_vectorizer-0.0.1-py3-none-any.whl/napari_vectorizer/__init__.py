try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"
from ._widget import (
    label_vectorization_widget,
)

__all__ = (
    "label_vectorization_widget",
)
