"""
Config Exception
"""

from src.exceptions.application_exception import ApplicationException

class ConfigException(ApplicationException):
    """
    Config Exception.

    If you encounter this exception, you may want to check application configuration:
        * Check content of your environment files (.env, .env.local)
        * Check content of your configuration file (config.json)
    """
