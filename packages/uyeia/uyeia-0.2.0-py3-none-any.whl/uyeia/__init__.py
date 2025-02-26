import _pickle as cPickle
import atexit
import io
import json
import logging
import os
import pickle
import re
import threading
from copy import deepcopy
from datetime import datetime, timezone
from typing import Literal

import jsonschema

from uyeia.exceptions import UYEIAConfigError
from uyeia.serializers import errors_config_schema
from uyeia.type import CommonStatus, Config, Status

__all__ = ["Watcher", "set_global_config", "get_errors", "register", "reset"]

_lock = threading.RLock()
_uyeia_config: Config = Config()
__uyeia_init__ = False
__default_logger__ = logging.getLogger("__UYEIA__")
__error_mapper__: dict[str, CommonStatus] = {}


def set_global_config(config: Config):
    global _uyeia_config

    if error := config.validate():
        if (
            __uyeia_init__
            and config.error_config_location != _uyeia_config.error_config_location
        ):
            __default_logger__.warning(
                "Error config location will be ignored. Global config has already been initialized."
            )
        raise UYEIAConfigError(f"Invalid UYEIA config: {error}")

    _uyeia_config = config
    _init_uyeia_env()


def _load_cache():
    if os.path.exists(_uyeia_config.error_cache_location):
        with io.open(_uyeia_config.error_cache_location, "rb") as db:
            return cPickle.load(db)
    return {}


def _load_config():
    path = _uyeia_config.error_config_location
    if os.path.isfile(path) and os.access(path, os.R_OK):
        try:
            with io.open(path, "r") as db_file:
                data = json.load(db_file)
                jsonschema.validate(data, errors_config_schema)
                return data
        except (jsonschema.ValidationError, json.decoder.JSONDecodeError) as e:
            raise UYEIAConfigError("Invalid errors config:", e)

    with io.open(path, "w") as db_file:
        json.dump({}, db_file)
    return {}


def _init_uyeia_env():
    global __uyeia_init__, __error_mapper__, __root__

    with _lock:
        __error_mapper__ = _load_config()
        __uyeia_init__ = True
        __root__.load_cache()


class Watcher:
    def __init__(self, name: str | None = None, logger: logging.Logger | None = None):
        self._cache: Status | None = None

        if logger:
            self.logger = logger
            self.name = self.logger.name
        elif name:
            self.logger = logging.getLogger(name)
            self.name = name
        else:
            raise ValueError("Name or logger is required for Watcher instance")

        global __root__
        self.manager = __root__.register(self)

        if not __uyeia_init__:
            _init_uyeia_env()

    def __log(self, status: CommonStatus, config: Config):
        level = config.status.get(status["status"])
        if isinstance(level, str):
            level = logging.getLevelName(level)

        if level:
            self.logger.log(level, status["message"])
        else:
            raise ValueError(
                f"Invalid status: {status['status']}. Not in UYEIA config!"
            )

    def __is_empty_or_high(self, status: CommonStatus) -> bool:
        levels = list(_uyeia_config.status.keys())
        return not self._cache or levels.index(status["status"]) > levels.index(
            self._cache["status"]
        )

    def get_actual_status(self):
        return self._cache

    def __replace_vars(self, message, args):
        var = re.search(r"{{(.*?)}}", message)
        if not var:
            return message
        var_name = var.groups()[0]
        value = args.get(var_name, "")
        return self.__replace_vars(
            message[: var.start()] + str(value) + message[var.end() :], args
        )

    def register(self, error_code: str, custom_message=None, vars: dict[str, str] = {}):
        error = __error_mapper__.get(error_code)
        if not error:
            raise ValueError(
                f"Invalid error code: {error_code}. Not in UYEIA errors config!"
            )

        if not _uyeia_config.disable_logging:
            self.__log(error, _uyeia_config)

        with _lock:
            if self.__is_empty_or_high(error):
                if self._cache and self._cache["status"] != error["status"].upper():
                    self.manager.delete_entry_cache(self.name, self._cache)

                message = custom_message or error["message"]
                if vars:
                    message = self.__replace_vars(message, vars)
                self._cache = {
                    "status": error["status"].upper(),
                    "message": self.__add_timestamp(message),
                    "solution": error.get("solution", _uyeia_config.default_solution),
                    "escalation": 0,
                }
                self.manager.write_entry_cache(self.name, self._cache)

    def release(self):
        if not self._cache:
            return

        with _lock:
            self.manager.delete_entry_cache(self.name, self._cache)
            self._cache = None

    def __del__(self):
        self.manager.unregister(self.name)

    def __add_timestamp(self, error_log: str) -> str:
        return (
            f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - {error_log}"
        )


class Manager:
    def __init__(self) -> None:
        self.watcherDict: dict[str, Watcher] = {}
        self.__cache = {}

    def getWatcher(self, name: str | None = None, logger: logging.Logger | None = None):
        if name and logger:
            raise ValueError(
                "Name or logger is required for Watcher instance! Not both."
            )

        rv = None
        name = name or getattr(logger, "name", None)
        if not name:
            raise ValueError("Name or logger is required for Watcher instance")

        with _lock:
            if name in self.watcherDict:
                rv = self.watcherDict[name]
            else:
                rv = Watcher(name, logger)
        return rv

    def __find_data_watcher(self, watcher_name: str):
        with _lock:
            return next(
                (
                    status
                    for entries in self.__cache.values()
                    for name, status in entries.items()
                    if name == watcher_name
                ),
                None,
            )

    def delete_entry_cache(self, name: str, old_status: Status):
        with _lock:
            self.__cache.get(old_status["status"], {}).pop(name, None)

    def write_entry_cache(self, name: str, status: Status):
        with _lock:
            self.__cache.setdefault(status["status"], {})[name] = status

    def get_cache(self):
        return self.__cache

    def set_cache(self, new_cache):
        with _lock:
            self.__cache = new_cache
            for watcher in self.watcherDict.values():
                watcher._cache = self.__find_data_watcher(watcher.name)

    def load_cache(self):
        with _lock:
            self.__cache = _load_cache()

    def clear_cache(self):
        with _lock:
            for watcher in self.watcherDict.values():
                watcher.release()

    def register(self, watcher: Watcher):
        with _lock:
            self.watcherDict[watcher.name] = watcher
            watcher._cache = self.__find_data_watcher(watcher.name)
            return self

    def unregister(self, name: str):
        with _lock:
            self.watcherDict.pop(name, None)


__root__ = Manager()


def _persist_cache():
    with _lock:
        if __root__.get_cache():
            with io.open(_uyeia_config.error_cache_location, "wb") as db:
                cPickle.dump(__root__.get_cache(), db, protocol=pickle.HIGHEST_PROTOCOL)


def get_errors(mode: Literal["all", "hot", "cold"] = "all"):
    cache = __root__.get_cache()
    if not cache:
        return None

    if mode == "all":
        return cache

    if mode not in {"hot", "cold"}:
        raise ValueError(f"Invalid mode: {mode}. Must be 'all', 'hot' or 'cold'!")

    for status in (
        _uyeia_config.status.keys()
        if mode == "cold"
        else reversed(_uyeia_config.status.keys())
    ):
        if status in cache:
            return next(iter(cache[status].values()), None)

    return None


def escalate():
    if _uyeia_config.disable_escalation:
        __default_logger__.warning("Escalate function is disabled in config.")
        return

    cache = __root__.get_cache()
    with _lock:
        high_status = _uyeia_config.escalation_status or next(
            reversed(_uyeia_config.status)
        )
        first_status = next(iter(_uyeia_config.status))

        new_cache = deepcopy(cache)
        to_escalate = {}

        for status, entries in cache.items():
            if status not in {high_status, first_status}:
                for name, entry in entries.items():
                    entry["escalation"] += 1
                    if entry["escalation"] >= _uyeia_config.max_escalation:
                        to_escalate[name] = entry
                        del new_cache[status][name]

        new_cache.setdefault(high_status, {}).update(to_escalate)
        __root__.set_cache(new_cache)


atexit.register(_persist_cache)
