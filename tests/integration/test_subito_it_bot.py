"""
test subito_it bot
"""

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.publishers.subito_it.publisher_bot import PublisherBot

class TestSubitoIt:
    """test publisher subito_it"""

    def test_publish(self, bot: PublisherBot, ads_json_subito_it: dict):
        """test publish ad item"""
        data = bot.publish(ads_json_subito_it, False)

        browser = bot.get_browser()

        btn_confirm = browser.get_element(By.ID, 'btnConfirm', 10)
        assert isinstance(btn_confirm, WebElement), "confirm button not found"

        actual_btn_text = browser.get_inner_html(By.ID, 'btnConfirm')
        assert actual_btn_text == 'Inserisci annuncio', "confirm button text unmatching"

        actual_ad_title = browser.get_inner_html(By.ID, 'prev_subject')
        assert actual_ad_title == data.ad_title[:50].strip() , "ad title unmatching"

        actual_ad_descr = browser.get_inner_html(By.ID, 'prev_body')
        assert actual_ad_descr == data.ad_description, "ad description unmatching"

        actual_ad_price = browser.get_inner_html(By.ID, 'prev_price')
        assert actual_ad_price == f"{data.item_price} €", "item price unmatching"
