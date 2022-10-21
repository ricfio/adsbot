"""json file reader"""

import json
from genericpath import exists
from tkinter.messagebox import NO

from src.datasources.abstract_datasource import AbstractDataSource

class DataSource(AbstractDataSource):
    """json file reader"""
    index = 0
    items = []

    def __init__(self, adlist_json_path: str, images_base_path: str = ''):
        if exists(adlist_json_path):
            with open(adlist_json_path, "r", encoding="utf8") as file:
                self.items = json.load(file)
            # add images_base_path as prefix for all images path
            for i, item in enumerate(self.items, start = 0):
                item_images = item.get('item_images', [])
                for j, image_file_path in enumerate(item_images, start = 0):
                    self.items[i]['item_images'][j] = f"{images_base_path}/{image_file_path}"

    def list(self, offset: int = None, limit: int = None) -> list:
        """Return items"""
        items = self.items
        if offset is not None and limit is not None:
            items = items[offset:offset+limit]
        elif offset is not None:
            items = items[offset:]
        elif limit is not None:
            items = items[:limit]

        return items

    def reset(self):
        """Reset items pointer"""
        self.index = 0

    def next(self):
        """Get next item"""
        item = None
        if self.index < len(self.items):
            item = self.items[self.index]
            self.index += 1

        return item
