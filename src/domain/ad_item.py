"""
AdItem
"""

class AdItem:
    """AdItem"""
    ad_category: list
    ad_title: str
    ad_description: str
    item_brand: str
    item_condition: str
    item_images: list
    item_price: str
    delivery_place: str
    shipping: None
    author_name: str
    author_email: str
    author_phone: str

    def __init__(
        self,
        ad_category: list = None,
        ad_title: str = None,
        ad_description: str = None,
        item_brand: str = None,
        item_condition: str = None,
        item_images: list = None,
        item_price: str = None,
        delivery_place: str = None,
        shipping: None = None,
        author_name: str = None,
        author_email: str = None,
        author_phone: str = None,
    ):
        super().__init__()
        self.ad_category = ad_category
        self.ad_title = ad_title
        self.ad_description = ad_description.lstrip()
        self.item_brand = item_brand
        self.item_condition = item_condition
        self.item_images = item_images
        self.item_price = item_price
        self.delivery_place = delivery_place
        self.shipping = shipping
        self.author_name = author_name
        self.author_email = author_email
        self.author_phone = author_phone.replace(" ", "") if author_phone else None

    @classmethod
    def build(cls, json):
        """build object from JSON"""
        return cls(**json)
