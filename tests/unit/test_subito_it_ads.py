"""
test subito_it ads
"""

import os.path

from src.publishers.subito_it.publisher_item import PublisherItem

class TestSubitoItAds:
    """test subito_it ads"""

    def test_build_ads_subito_it(self, ads_json_subito_it: dict):
        """build ads subito_it"""
        item = PublisherItem(**ads_json_subito_it)
        assert isinstance(item, PublisherItem)

        if item.item_images:
            for path in item.item_images:
                assert os.path.isfile(path), f"image not found: {path}"
