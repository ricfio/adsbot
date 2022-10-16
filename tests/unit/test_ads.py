"""
test ads
"""

from src.domain.ad_item import AdItem

class TestAda:
    """test ads"""

    def test_build(self):
        """Build AdItem"""
        ad_item = AdItem(
            ad_category = ['category'],
            ad_title = 'title',
            ad_description = 'description',
        )
        assert isinstance(ad_item, AdItem)
