"""json http client"""

import requests

from src.datasources.abstract_datasource import AbstractDataSource

class DataSource(AbstractDataSource):
    """json http client"""
    index = 0
    items = []

    def __init__(self, adlist_json_url: str, images_base_path: str = ''):
        response = requests.get(adlist_json_url)
        response_code = response.status_code
        content_type = response.headers['Content-Type']
        if (response.status_code != 200):
            raise Exception(f'Invalid HTTP-Code ({response_code}) at {adlist_json_url}')
        if (response.headers['Content-Type'] != 'application/json; charset=utf-8'):
            raise Exception(f'Invalid Content-Type ({content_type}) at {adlist_json_url}')
        self.items = response.json()
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
