"""
Unit Test > Browser
"""

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src.services.browser import Browser

@pytest.fixture(scope="module")
def browser() -> Browser:
    browser = Browser()
    # Load "Demo Sign-Up Selenium Automation Practice Form"
    browser.get("https://www.techlistic.com/p/selenium-practice-form.html")
    # Accepts all cookies
    browser.get_element(By.ID, "ez-accept-all").click()
    yield browser

class TestBrowser:

    def test_write_text_immediate(self, browser: Browser):
        browser.write_text(By.NAME, "firstname", "Riccardo")
        assert "Riccardo" == browser.find_element(By.NAME, "firstname").get_attribute("value")

    def test_write_text_with_timeout(self, browser: Browser):
        browser.write_text(By.NAME, "lastname", "Fiorenza", 5)
        assert "Fiorenza" == browser.find_element(By.NAME, "lastname").get_attribute("value")

    def test_select_radio(self, browser: Browser):
        css_selector = f"input[name='sex'][value='Male']"
        browser.select_radio(By.CSS_SELECTOR, css_selector)
        assert True  is browser.find_element(By.ID, "sex-0").is_selected()
        assert False is browser.find_element(By.ID, "sex-1").is_selected()

        css_selector = f"input[name='exp'][value='7']"
        browser.select_radio(By.CSS_SELECTOR, css_selector)
        assert False is browser.find_element(By.ID, "exp-0").is_selected()
        assert False is browser.find_element(By.ID, "exp-1").is_selected()
        assert False is browser.find_element(By.ID, "exp-2").is_selected()
        assert False is browser.find_element(By.ID, "exp-3").is_selected()
        assert False is browser.find_element(By.ID, "exp-4").is_selected()
        assert False is browser.find_element(By.ID, "exp-5").is_selected()
        assert True  is browser.find_element(By.ID, "exp-6").is_selected()

    @pytest.mark.skip(reason="to implement")
    def test_select_date(self, browser: Browser):
        browser.get_element(By.ID, "datepicker")
        assert False

    def test_select_checkbox(self, browser: Browser):
        browser.select_checkbox(By.CSS_SELECTOR, f"input[name='profession'][value='Automation Tester']")
        assert False is browser.find_element(By.ID, "profession-0").is_selected()
        assert True  is browser.find_element(By.ID, "profession-1").is_selected()

        browser.select_checkbox(By.ID, "tool-0")
        browser.select_checkbox(By.ID, "tool-2")
        assert True  is browser.find_element(By.ID, "tool-0").is_selected()
        assert False is browser.find_element(By.ID, "tool-1").is_selected()
        assert True  is browser.find_element(By.ID, "tool-2").is_selected()

    def test_select_option_by_text(self, browser: Browser):
        browser.select_option_by_text(By.NAME, "continents", "Europe")
        select = browser.find_element(By.NAME, "continents")
        assert "Europe" == Select(select).first_selected_option.get_attribute('value')


    def test_upload_file(self, browser: Browser):
        try:
            browser.upload_files(By.ID, 'photo', ['./data/test/images/lettore-divx/lettore-divx-01.jpg'])
        except Exception as exception:
            assert False, f"file uploading raised exception '{exception}'"
