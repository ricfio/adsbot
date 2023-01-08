"""
Kernel
"""

import os

from dotenv import find_dotenv, load_dotenv

from src.controller import Controller

class Kernel:
    """Kernel"""

    __environment: str = None
    __dotenv_list: list[str]
    __config_path: str = None

    def __init__(self) -> None:
        """kernel boot"""
        # detect environment type
        self.__environment = self.__detect_environment()
        # load environment variables
        self.__dotenv_list = self.__load_environment_variables(self.__environment)
        # detect config path
        self.__config_path = self.__detect_config_path()

    @property
    def environment(self):
        """get environment"""
        return self.__environment

    @property
    def dotenv_list(self):
        """get dotenv list"""
        return self.__dotenv_list

    @property
    def config_path(self):
        """get config path"""
        return self.__config_path

    @staticmethod
    def __detect_environment() -> str:
        """detect environment type"""
        return os.getenv('ENV', '')

    @staticmethod
    def __load_environment_variables(environment: str = None) -> list[str]:
        """load environment variables"""
        dotenv_list = []
        if environment:
            dotenv_list.append(f'.env.{environment}.local')
            dotenv_list.append(f'.env.{environment}')
        dotenv_list.append('.env.local')
        dotenv_list.append('.env')
        for dotenv_file in dotenv_list:
            dotenv_path = find_dotenv(
                filename = dotenv_file,
                raise_error_if_not_found = False,
                usecwd = False,
            )
            if os.path.exists(dotenv_path):
                load_dotenv(dotenv_path = dotenv_path, override = False)
        return dotenv_list

    @staticmethod
    def __detect_config_path() -> str:
        """detect config path"""
        return os.getenv('CONFIG_PATH', 'config.json')

    def get_controller(self) -> Controller:
        """create application from config file"""
        return Controller.create(self.__config_path)
