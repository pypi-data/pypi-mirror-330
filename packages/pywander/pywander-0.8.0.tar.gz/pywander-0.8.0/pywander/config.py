

import importlib
import os

from pywander.functools import lazy

DEFAULT_CONFIG = {
    "APP_NAME": 'pywander'
}


def get_config(config_module=None):
    config = {}

    for k, v in DEFAULT_CONFIG.items():
        if k.isupper():
            config[k] = v

    if config_module is None:
        config_module = os.environ.get('CONFIG_MODULE')

    if config_module:
        mod = importlib.import_module(config_module)

        for k in dir(mod):
            if k.isupper():
                v = getattr(mod, k)
                config[k] = v

    return config


def lazy_get_config(config_module=None):
    """
    各个模块导入都不会加载，会在实际使用config时才实际执行。
    """

    return lazy(get_config, dict)(config_module)


config = lazy_get_config()
