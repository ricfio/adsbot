"""
Browser (with shortcuts added)
"""

import os

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

from .browsers.google_chrome import GoogleChrome

class Browser(GoogleChrome):
    """Browser (with shortcuts added)"""

    def __wait_for_element(
        self,
        by: By,
        tag: str,
        timeout: float = 5,
        raise_exception: bool = True,
    ):
        """wait for dom element"""
        element = WebDriverWait(self, timeout).until(
            expected_conditions.presence_of_element_located((by, tag))
        )
        if element is None and raise_exception:
            raise Exception(f"cannot found element by {by}: '{tag}'")
        return element

    def get_element(
        self,
        by: By,
        tag: str,
        timeout: float = 0,
        raise_exception: bool = True,
    ):
        """get dom element"""
        element = None
        if timeout == 0:
            try:
                element = self.find_element(by, tag)
            except NoSuchElementException as exception:
                if raise_exception:
                    raise exception
        else:
            element = self.__wait_for_element(by, tag, timeout, raise_exception)
        return element

    def get_inner_html(
        self,
        by: By,
        tag: str,
        timeout: float = 0,
        raise_exception: bool = True,
    ) -> str:
        """get dom element inner html"""
        element = self.get_element(by, tag, timeout, raise_exception)
        if element:
            return element.get_attribute('innerHTML')
        return None

    def click_element(
        self,
        by: By,
        tag: str,
        timeout: float = 0,
        perform: bool = True,
    ):
        """click on dom element"""
        element = self.get_element(by, tag, timeout)
        if element:
            action_chains = ActionChains(self).move_to_element(element).click()
            if perform:
                action_chains.perform()

    def write_text(
        self,
        by: By,
        tag: str,
        text: str,
        timeout: float = 0,
        raise_exception: bool = True,
    ):
        """write text in an <input> tag (<input type="text" value="...">)"""
        element = self.get_element(by, tag, timeout, raise_exception)
        if element:
            element.clear()
            element.send_keys(text)
        return element

    def select_option_by_text(
        self,
        by: By,
        tag: str,
        text: str,
        timeout: float = 0,
        raise_exception: bool = True,
    ):
        """select a specific <option> by text (<option>...</option>)"""
        element = self.get_element(by, tag, timeout, raise_exception)
        if element:
            Select(element).select_by_visible_text(text)

    def select_option_by_value(
        self,
        by: By,
        tag: str,
        value: str,
        timeout: float = 0,
    ):
        """select a specific <option> by value (<option value="...">text</option>)"""
        element = self.get_element(by, tag, timeout)
        if element:
            Select(element).select_by_value(value)

    def select_radio(
        self,
        by: By,
        tag: str,
        timeout: float = 0,
    ):
        """select a specific <input type="radio"> (<input type="radio" checked="...">)"""
        element = self.get_element(by, tag, timeout)
        if element:
            ActionChains(self).move_to_element(element).click().perform()

    def select_checkbox(
        self,
        by: By,
        tag: str,
        timeout: float = 0,
    ):
        """select a specific <input type="checkbox"> (<input type="checkbox" checked="...">)"""
        self.click_element(by, tag, timeout)

    def upload_files(
        self,
        by: By,
        tag: str,
        paths: list[str],
        timeout: float = 0,
    ):
        """upload files"""
        element = self.get_element(by, tag, timeout, raise_exception=True)
        if element:
            # transform relative path list in absolute path list
            upload_paths = list(map(os.path.abspath, paths))
            element.send_keys("\n".join(upload_paths))
