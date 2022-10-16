"""
Application Controller
"""

from importlib import import_module
import json

from src.publishers.abstract_bot import AbstractBot
from src.publishers.subito_it.publisher_bot import PublisherBot

from .datasources.abstract_datasource import AbstractDataSource

class Controller:
    """Controller"""
    datasource: AbstractDataSource = None

    publishers: list = []

    def __init__(self, datasource: AbstractDataSource, publishers: list):
        self.datasource = datasource
        self.publishers = publishers

    @classmethod
    def create(cls, config_path: str):
        """create application from config file"""
        with open(config_path, "r", encoding="utf8") as file:
            config = json.load(file)

        dependency = config["datasource"]
        datasource: AbstractDataSource = import_module(
            f'src.datasources.{dependency["name"]}'
        ).DataSource(**dependency["args"])

        publishers = []
        for _, dependency in enumerate(config["publishers"], start = 0):
            publisher = import_module(
                f'src.publishers.{dependency["name"]}.publisher_bot'
            ).PublisherBot(**dependency["args"])
            publishers.append(publisher)

        return cls(datasource, publishers)

    def list_ads(self):
        """list ads"""
        ads_list = self.datasource.list()
        for i, ad_json in enumerate(ads_list, start = 1):
            self.__print_ad_json(i, ad_json)

    def publish(self):
        """publish ads"""
        ads_list: list[dict]
        publisher: AbstractBot

        ads_list = self.datasource.list()
        for publisher in self.publishers:
            for i, ad_json in enumerate(ads_list, start = 1):
                self.__print_ad_json(i, ad_json)
                publisher.publish(ad_json)

    @staticmethod
    def __print_ad_json(i: int, data: dict):
        print(f"{i:2d}: {data['ad_title']:60s} € {data['item_price']:2d} (+ {data['shipping']:2d})")
