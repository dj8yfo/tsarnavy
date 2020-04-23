try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from yaml import load
import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "./bot_cfg.yaml")
with open(filename, "r") as cfg:
    BOT_CFG = load(cfg.read(), Loader=Loader)
