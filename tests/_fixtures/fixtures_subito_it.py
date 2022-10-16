"""
fixtures subito_it
"""

import pytest

from src.datasources.json_file_reader import DataSource

from src.publishers.subito_it.publisher_bot import PublisherBot
from src.publishers.subito_it.publisher_item import PublisherItem

env='test'
ADLIST_DATA_PATH = f'./data/{env}/ads_subito_it.json'
IMAGES_BASE_PATH = f'./data/{env}/images'
subito_it_ads = DataSource(ADLIST_DATA_PATH, IMAGES_BASE_PATH).list()

@pytest.fixture()
#@pytest.fixture(scope="module")
def bot():
    """yield PublisherBot (subito_it)"""
    publisher_bot = PublisherBot()
    publisher_bot.login()
    yield publisher_bot

@pytest.fixture(scope="module", params=subito_it_ads)
def ads_json_subito_it(request):
    """yield PublisherItem (subito_it)"""
    yield request.param
