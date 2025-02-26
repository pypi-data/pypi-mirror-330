import os
from importlib import reload

import pytest

import uyeia


@pytest.fixture(autouse=True)
def cleanup_tests_folder():
    def delete_file_config(path):
        if os.path.exists(path):
            os.remove(path)

    delete_file_config("./tests/uyeia.errors.json")
    delete_file_config("./tests/errors_cache.db")
    yield
    delete_file_config("./tests/uyeia.errors.json")
    delete_file_config("./tests/errors_cache.db")


@pytest.fixture(autouse=True)
def reload_package():
    global uyeia
    reload(uyeia)
    yield


@pytest.fixture
def sample_config():
    return uyeia.Config(
        error_config_location="./tests/samples/uyeia.errors.json",
        error_cache_location="./tests/errors_cache.db",
    )
