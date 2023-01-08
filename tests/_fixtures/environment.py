import pytest

import os
from dotenv import load_dotenv

@pytest.fixture(scope='session', autouse=True)
def load_env():
    dotenv_list = [
        '.env.test.local',
        '.env.test',
    ]
    for dotenv_path in dotenv_list:
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path = dotenv_path, override = False)
