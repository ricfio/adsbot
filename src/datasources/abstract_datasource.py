"""
abstract datasource
"""
from abc import ABC, abstractmethod

class AbstractDataSource(ABC):
    """abstract datasource"""

    @abstractmethod
    def list(self, offset: int = None, limit: int = None):
        """Return items"""

    @abstractmethod
    def reset(self):
        """Reset items pointer"""

    @abstractmethod
    def next(self):
        """Get next item"""
