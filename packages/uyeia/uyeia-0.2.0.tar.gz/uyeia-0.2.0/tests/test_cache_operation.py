import uyeia


def test_read_cache_error():
    config = uyeia.Config(
        error_cache_location="./tests/samples/errors_cache.db",
        error_config_location="./tests/samples/uyeia.errors.json",
    )
    uyeia.set_global_config(config)
    errors = uyeia.get_errors()
    assert errors and len(errors) == 2
