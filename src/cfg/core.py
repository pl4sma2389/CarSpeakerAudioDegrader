import configparser
from cfg.data import config_default

config = configparser.ConfigParser()

print(config_default)


def load_config():
    return config_default  # TODO: Implement config loading instead of loading hardcoded values from cfg/data.py
