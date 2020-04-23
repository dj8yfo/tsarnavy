from yaml import load, dump
from pprint import pprint
with open('./bot_cfg.yaml', 'r') as cfg:
    pprint(load(cfg.read()))
