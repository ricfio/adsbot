"""
publisher bot: subito_it
"""

import os

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.exceptions.config_exception import ConfigException
from src.publishers.abstract_bot import AbstractBot
from src.publishers.subito_it.publisher_item import PublisherItem

class PublisherBot(AbstractBot):
    """publisher bot: subito_it"""

    __URL_LOGIN = 'https://areariservata.subito.it/login_form'
    __URL_LOGOUT = 'https://areariservata.subito.it/logout'
    __URL_PUBLISH = 'https://www2.subito.it/aif#insert'
    __MAX_IMAGES = 6

    __username = None
    __password = None

    __logged = False

    def __init__(self):
        super().__init__()
        self.__username = os.getenv('SUBITO_USERNAME', '')
        self.__password = os.getenv('SUBITO_PASSWORD', '')

    def login(self) -> bool:
        """do login"""
        if not self.__logged:
            if len(self.__username) == 0:
                raise ConfigException('missing username (see SUBITO_USERNAME in .env files)')
            if len(self.__password) == 0:
                raise ConfigException('missing password (set SUBITO_PASSWORD in .env files)')
            browser = self.get_browser()
            # go login page
            browser.get(self.__URL_LOGIN)
            # accept cookies (if dialog is present)
            accept_cookies = browser.get_element(
                By.ID,
                'didomi-notice-agree-button',
                timeout=0,
                raise_exception=False,
            )
            if accept_cookies:
                accept_cookies.click()
            # insert username
            browser.write_text(By.ID, 'username', self.__username)
            # insert password
            browser.write_text(By.ID, 'password', self.__password)
            # submit login
            browser.get_element(By.CSS_SELECTOR, "button[type='submit']").send_keys(Keys.RETURN)
            # wait until login is completed (wait for logout link)
            logout_link = browser.get_element(By.CSS_SELECTOR, f"a[href='{self.__URL_LOGOUT}']", 20)
            self.__logged = (logout_link is not None)

        return self.__logged

    def logout(self) -> bool:
        """do logout"""
        if self.__logged:
            browser = self.get_browser()
            # go logout page
            browser.get(self.__URL_LOGOUT)
            # wait until logout is completed (wait for login button showing is completed)
            login_button = browser.get_element(By.CSS_SELECTOR, "button[type='submit'] > span", 20)
            if 'Accedi' == login_button.get_attribute('innerHTML'):
                self.__logged = False
        
        return not self.__logged

    def publish(self, ad_json: dict, submit: bool = True) -> PublisherItem:
        """publish classified ad"""
        data = PublisherItem(**ad_json)
        self.__publish_start()
        self.__publish_select_ad_category_1st(data.ad_category)
        self.__publish_select_ad_type(data.ad_type)
        self.__publish_select_ad_category_sub(data.ad_category)
        self.__publish_select_item_condition(data.item_condition)
        self.__publish_upload_item_images(data.item_images)
        self.__publish_write_ad_title(data.ad_title)
        self.__publish_write_ad_description(data.ad_description)
        self.__publish_write_item_price(data.item_price)
        self.__publish_compile_shipping(data.shipping)
        self.__publish_write_delivery_town(data.delivery_town)
        self.__publish_compile_author(data.author_type, data.author_name, data.author_phone)
        self.__publish_submit(submit)
        return data

    def __publish_start(self):
        """start publishing"""
        if self.login() is False:
            raise Exception('login has failed but it is required to publish')

        browser = self.get_browser()
        browser.get(self.__URL_PUBLISH)

    def __publish_select_ad_category_1st(self, ad_category: list):
        """select the main category"""
        browser = self.get_browser()
        browser.select_option_by_text(By.NAME, 'category', ad_category[0])

    def __publish_select_ad_type(self, ad_type: str):
        """select the ad type (offer/wanted)"""
        # Tipo annuncio (In vendita / Cercasi)
        if ad_type:
            browser = self.get_browser()
            browser.select_radio(By.CSS_SELECTOR, f"input[name='type'][value='{ad_type}']")

    def __publish_select_ad_category_sub(self, ad_category: list):
        """select the sub categories"""
        browser = self.get_browser()
        # Sub-Category (1)
        if len(ad_category)>1:
            if ad_category[0]=='Auto':
                tag = 'carbrand'
            elif ad_category[0]=='Tutto per i bambini':
                tag = 'children_type'
            elif ad_category[0]=='Abbigliamento e Accessori':
                tag = 'clothing_type'
            elif ad_category[0]=='Informatica':
                tag = 'computer_type'
            elif ad_category[0]=='Audio/Video':
                tag = 'audiovideo_type'
            elif ad_category[0]=='Collezionismo':
                tag = 'hobby_type'
            elif ad_category[0]=='Telefonia':
                tag = 'phone_type'
            else:
                tag = None
            if tag:
                browser.select_option_by_text(By.NAME, tag, ad_category[1], timeout=10)
        # Sub-Category (2)
        if len(ad_category)>2:
            if ad_category[0]=='Auto':
                tag = 'carmodel'
            elif ad_category[0]=='Tutto per i bambini':
                tag = 'children_age'
            elif ad_category[0]=='Abbigliamento e Accessori':
                tag = 'clothing_gender'
            else:
                tag = None
            if tag:
                browser.select_option_by_text(By.NAME, tag, ad_category[2], timeout=10)
        # Sub-Category (3)
        if len(ad_category)>3:
            if ad_category[0]=='Auto':
                tag = 'carversion'
            else:
                tag = None
            if tag:
                browser.select_option_by_text(By.NAME, tag, ad_category[3], timeout=10)

    def __publish_select_item_condition(self, item_condition: str):
        """select the item condition"""
        if item_condition:
            browser = self.get_browser()
            browser.select_option_by_text(By.NAME, 'item_condition', item_condition, timeout=0, raise_exception=False)

    def __publish_upload_item_images(self, item_images: list):
        """upload the images"""
        if item_images and len(item_images)>0:
            browser = self.get_browser()
            # limit the max number of images
            images_list = item_images[:self.__MAX_IMAGES]
            images_size = len(images_list)
            # upload files (with max images limit)
            browser.upload_files(By.NAME, 'fileElem', images_list)
            # wait until the last upload will be completed
            browser.get_element(By.ID, 'image_' + str(images_size-1), 20 * images_size)

    def __publish_write_ad_title(self, ad_title: str):
        """write the ad title"""
        browser = self.get_browser()
        browser.write_text(By.ID, 'subject', ad_title)

    def __publish_write_ad_description(self, ad_description: str):
        """write the ad description"""
        browser = self.get_browser()
        browser.write_text(By.ID, 'body', ad_description)

    def __publish_write_item_price(self, item_price: str):
        """write the item price (optional)"""
        if item_price:
            browser = self.get_browser()
            browser.write_text(By.ID, 'price', item_price)

    def __publish_compile_shipping(self, shipping: bool|int):
        """compile the shipping (optional)"""
        shipping_cost = shipping if isinstance(shipping,int) else 0
        shipping = shipping_cost > 0
        browser = self.get_browser()
        element = browser.get_element(By.NAME, 'item_shippable', timeout=0, raise_exception=False)
        if element:
            if element.is_selected() != shipping:
                browser.click_element(By.NAME,'item_shippable')

            if shipping and shipping_cost > 0:
                browser.select_radio(By.CSS_SELECTOR, "input[name='item_shipping_type'][value='1']")
                browser.write_text(By.ID, 'item_shipping_cost', shipping_cost, 10)

    def __publish_write_delivery_town(self, delivery_town: str):
        """write the delivery town for the item"""
        if delivery_town:
            sleep(1.0)
            browser = self.get_browser()
            browser.write_text(By.ID, 'town', delivery_town, 10).send_keys(Keys.TAB)

    def __publish_compile_author(self, author_type: int, author_name: str, author_phone: str):
        """compile ad author informations"""
        browser = self.get_browser()
        # Sono un/una (Privato / Azienda)
        browser.select_radio(By.CSS_SELECTOR, f"input[name='company_ad'][value='{author_type}']")
        # Nome
        browser.write_text(By.ID, 'name', author_name, timeout=0, raise_exception=False)
        # Telefono
        browser.write_text(By.ID, 'phone', author_phone)
        # # Nascondi il numero
        # browser.click_element(By.NAME, 'phone_hidden')

    def __publish_submit(self, submit: bool):
        """submit the ad to publish"""
        browser = self.get_browser()
        # Submit click (step 1/4)
        browser.get_element(By.ID, 'btnAiSubmit').send_keys(Keys.RETURN)
        # Confirm check (step 2/4) - wait until preview showing is completed
        browser.get_element(By.CSS_SELECTOR, "article[id='aiPreview'][style='display: block;']", 20)
        # Confirm click (step 3/4)
        browser.click_element(By.ID, 'btnConfirm', 0, submit)
        # Submit click (step 4/4) - wait until promotions page showing is completed
        if submit:
            browser.get_element(By.CSS_SELECTOR, "button[type='submit']", 20)
