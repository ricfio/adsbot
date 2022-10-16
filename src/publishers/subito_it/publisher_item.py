"""adsbot"""

class PublisherItem:
    """subito.it publisher bot"""

    ad_category: list
    ad_type: str
    ad_title: str
    ad_description: str
    item_brand: str
    item_condition: str
    item_images: list
    item_price: str
    delivery_town: str
    shipping: bool|int
    author_type: int
    author_name: str
    author_phone: str

    def __init__(
        self,
        ad_category: list = [],
        ad_type: str = 's',
        ad_title: str = None,
        ad_description: str = None,
        item_brand: str = None,
        item_condition: str = None,
        item_images: list = [],
        item_price: str = None,
        delivery_town: str = None,
        shipping: bool|int = False,
        author_type: int = 0,
        author_name: str = None,
        author_phone: str = None,
    ):
        super().__init__()
        self.ad_category = ad_category
        self.ad_type = ad_type
        self.ad_title = ad_title
        self.ad_description = ad_description.lstrip()
        self.item_brand = item_brand
        self.item_condition = item_condition
        self.item_images = item_images
        self.item_price = item_price
        self.delivery_town = delivery_town
        self.shipping = shipping
        self.author_type = author_type
        self.author_name = author_name
        self.author_phone = author_phone.replace(" ", "") if author_phone else None
        self.__validate()

    def __validate(self):
        self.__validate_ad_category(self.ad_category)
        self.__validate_item_condition(self.item_condition)

    @staticmethod
    def __validate_ad_category(ad_category: str):
        if len(ad_category)>0:
            value = ad_category[0]
            if value and value not in [
                'Auto',
                'Tutto per i bambini',
                'Abbigliamento e Accessori',
                'Arredamento e Casalinghi',
                'Informatica',
                'Audio/Video',
                'Collezionismo',
            ]:
                raise Exception(f"unknown category '{value}'")

    @staticmethod
    def __validate_item_condition(condition: str):
        if condition:
            match condition:
                case 'Come nuovo - perfetto o ricondizionato':
                    return
                case 'Nuovo - mai usato in confezione originale':
                    pass
                case 'Ottimo - poco usato e ben conservato':
                    pass
                case 'Buono - usato ma ben conservato':
                    pass
                case 'Danneggiato - usato con parti guaste':
                    pass
                case unknown:
                    raise Exception(f"unknown condition '{unknown}'")
