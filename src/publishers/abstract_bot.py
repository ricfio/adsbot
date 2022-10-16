"""abstract publisher bot"""
from abc import ABC, abstractmethod

from src.services.browser import Browser

class AbstractBot(ABC):
    """abstract publisher bot"""

    _browser: Browser

    def __init__(self):
        super().__init__()
        self._browser = None

    def get_browser(self) -> Browser:
        """build browser"""
        if self._browser is None:
            self._browser = Browser()

        return self._browser

    @abstractmethod
    def login(self) -> bool:
        """user login"""

    @abstractmethod
    def publish(self, ad_json: dict, submit: bool = True) -> bool:
        """publish ad"""
