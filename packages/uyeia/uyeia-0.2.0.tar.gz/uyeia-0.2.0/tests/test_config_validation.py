import pytest

import uyeia


def test_error_config_missing_message():
    config = uyeia.Config(
        error_config_location="./tests/samples/uyeia.errors_missing_message.json",
    )
    with pytest.raises(uyeia.UYEIAConfigError):
        uyeia.set_global_config(config)

        uyeia.reset()


def test_error_config_missing_status():
    config = uyeia.Config(
        error_config_location="./tests/samples/uyeia.errors_missing_status.json",
    )
    with pytest.raises(uyeia.UYEIAConfigError):
        uyeia.set_global_config(config)

        uyeia.reset()


def test_global_config_unknow_logging_level_int():
    config = uyeia.Config(
        status={
            "HEALTHY": -1,
        }
    )

    with pytest.raises(uyeia.UYEIAConfigError):
        uyeia.set_global_config(config)


def test_global_config_unknow_logging_level_str():
    config = uyeia.Config(
        status={
            "HEALTHY": "test",
        }
    )

    with pytest.raises(uyeia.UYEIAConfigError):
        uyeia.set_global_config(config)
