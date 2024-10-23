import json
from random import randint
from resources import constants
from src.cfg.CFG import CFG
from src.cfg.visualization.CFGVisualizer import CFGVisualizer
from src.cfg.cfg_serialization import serialize_cfg, deserialize_cfg
from src.cfa.CFA import CFA


class App:
    def __init__(self, settings_path:str="config/settings.json"):
        self.settings_path = settings_path
        self.input_data = 0

    def _read_data(self):
        print("Введите количество вершин:", end=' ')
        constants.NUMBER_OF_BASE_BLOCKS = int(input())
        constants.NUMBER_OF_EDGES = randint(int(1.3 * constants.NUMBER_OF_BASE_BLOCKS),
                                            2 * (constants.NUMBER_OF_BASE_BLOCKS - 1))

    def _read_settings(self):
        with open(self.settings_path, 'rt', encoding='utf-8') as f:
            CFG.settings = json.load(f)

    def run(self):
        self._read_data()
        self._read_settings()
        cfg = CFG(constants.NUMBER_OF_BASE_BLOCKS, constants.NUMBER_OF_EDGES)
        #CFGVisualizer.visualize_cfg(cfg)
        # print(serialize_cfg(cfg))
        # CFGVisualizer.visualize_cfg(deserialize_cfg(serialize_cfg(cfg)))
        CFA.cfg_traversal(cfg, 10)
        CFGVisualizer.visualize_cfg(cfg)

