"""abstract publisher item"""
from abc import ABC

from ..domain.ad_item import AdItem

class AbstractItem(ABC):
    """abstract publisher item"""

    @classmethod
    def build(cls, item: AdItem):
        """build publisher item from master item"""
        return cls()
