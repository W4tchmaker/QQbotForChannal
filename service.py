import os
import re
from collections import defaultdict
from functools import wraps

import priv
import trigger
from log import _log

import json

_loaded_services: dict[str, "Service"] = {}  # {name: service}
_service_bundle: dict[str, list["Service"]] = defaultdict(list)
_re_illegal_char = re.compile(r'[\\/:*?"<>|.]')
_service_config_dir = os.path.expanduser('~/.Bot/service_config/')
os.makedirs(_service_config_dir, exist_ok=True)


def _load_service_config(service_name):
    config_file = os.path.join(_service_config_dir, f'{service_name}.json')
    if not os.path.exists(config_file):
        return {}  # config file not found, return default config.
    try:
        with open(config_file, encoding='utf8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        _log.exception(e)
        return {}


def _save_service_config(service):
    config_file = os.path.join(_service_config_dir, f'{service.name}.json')
    with open(config_file, 'w', encoding='utf8') as f:
        json.dump(
            {
                "name": service.name,
                "enable_on_default": service.enable_on_default,
                "enable_channel": list(service.enable_channel),
                "disable_channel": list(service.disable_channel)
            },
            f,
            ensure_ascii=False,
            indent=2)


class ServiceFunc:
    def __init__(self, sv: "Service", func: callable, normalize_text: bool = False):
        self.sv = sv
        self.func = func
        self.normalize_text = normalize_text
        self.__name__ = func.__name__

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class Service:
    """docstring for Message_handler"""

    def __init__(self, name, help_=None, bundle=None, enable_on_default=None):
        assert not _re_illegal_char.search(name), r'Service name cannot contain character in `\/:*?"<>|.`'
        config = _load_service_config(name)

        self.help = help_
        self.name = name
        self.help_image = None

        self.enable_on_default = config.get('enable_on_default')
        if self.enable_on_default is None:
            self.enable_on_default = enable_on_default
        if self.enable_on_default is None:
            self.enable_on_default = True

        self.enable_channel = set(config.get('enable_channel', []))
        self.disable_channel = set(config.get('disable_channel', []))

        assert self.name not in _loaded_services, f'Service name "{self.name}" already exist!'
        _loaded_services[self.name] = self
        _service_bundle[bundle or "通用"].append(self)

    @staticmethod
    def get_loaded_services() -> dict[str, "Service"]:
        return _loaded_services

    @staticmethod
    def get_bundles():
        return _service_bundle

    def set_enable(self, channel_id):
        self.enable_channel.add(channel_id)
        self.disable_channel.discard(channel_id)
        _save_service_config(self)
        _log.info(f'Service {self.name} is enabled at channel {channel_id}')

    def set_disable(self, channel_id):
        self.enable_channel.discard(channel_id)
        self.disable_channel.add(channel_id)
        _save_service_config(self)
        _log.info(
            f'Service {self.name} is disabled at channel {channel_id}')

    def check_enabled(self, channel_id):
        return bool((channel_id in self.enable_channel) or
                    (self.enable_on_default and channel_id not in self.disable_channel))

    def _check_all(self, message):
        gid = message.channel_id
        return self.check_enabled(gid) and not priv.check_block_channel(gid)

    def on_full_match(self, *word) -> callable:
        if len(word) == 1 and not isinstance(word[0], str):
            word = word[0]

        def deco(func) -> callable:
            @wraps(func)
            async def wrapper(bot, message):
                if len(message.content) != 0:
                    _log.info(f'Message {message.id} is ignored by full match condition.')
                    return
                return await func(bot, message)

            sf = ServiceFunc(self, wrapper)
            for w in word:
                if isinstance(w, str):
                    trigger.prefix.add(w, sf)
                else:
                    _log.error(f'Failed to add full match trigger `{w}`, expecting `str` but `{type(w)}` given!')
            return func

        return deco

    # 前缀匹配
    def on_prefix(self, *prefix) -> callable:
        if len(prefix) == 1 and not isinstance(prefix[0], str):
            prefix = prefix[0]

        def deco(func) -> callable:
            sf = ServiceFunc(self, func)
            for p in prefix:
                if isinstance(p, str):
                    trigger.prefix.add(p, sf)
                else:
                    _log.error(f'Failed to add prefix trigger `{p}`, expecting `str` but `{type(p)}` given!')
            return func

        return deco

    def on_suffix(self, *suffix) -> callable:
        if len(suffix) == 1 and not isinstance(suffix[0], str):
            prefix = suffix[0]

        def deco(func) -> callable:
            sf = ServiceFunc(self, func)
            for p in prefix:
                if isinstance(p, str):
                    trigger.suffix.add(p, sf)
                else:
                    _log.error(f'Failed to add prefix trigger `{p}`, expecting `str` but `{type(p)}` given!')
            return func

        return deco

    def on_keyword(self, *keywords, normalize=True) -> callable:
        if len(keywords) == 1 and not isinstance(keywords[0], str):
            keywords = keywords[0]

        def deco(func) -> callable:
            sf = ServiceFunc(self, func, normalize)
            for kw in keywords:
                if isinstance(kw, str):
                    trigger.keyword.add(kw, sf)
                else:
                    _log.error(f'Failed to add keyword trigger `{kw}`, expecting `str` but `{type(kw)}` given!')
            return func

        return deco

    def on_rex(self, rex: [str, re.Pattern], normalize=True) -> callable:
        if isinstance(rex, str):
            rex = re.compile(rex)

        def deco(func) -> callable:
            sf = ServiceFunc(self, func, normalize)
            if isinstance(rex, re.Pattern):
                trigger.rex.add(rex, sf)
            else:
                _log.error(
                    f'Failed to add rex trigger `{rex}`, expecting `str` or `re.Pattern` but `{type(rex)}` given!')
            return func

        return deco

