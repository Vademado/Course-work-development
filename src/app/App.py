import json
from random import randint
from resources import constants
from src.cfg.CFG import CFG
from src.cfa.CFA import CFA
from src.cfg.visualization.CFGVisualizer import CFGVisualizer
from src.cfg.cfg_serialization import serialize_cfg, deserialize_cfg


class App:
    def __init__(self, number_of_base_blocks: int, file_path_to_read: str, name_of_file_to_save: str, input_data: int, settings_path: str, show: bool):
        constants.NUMBER_OF_BASE_BLOCKS = number_of_base_blocks
        self.file_path_to_read = file_path_to_read
        self.name_of_file_to_save = name_of_file_to_save
        constants.INPUT_DATA = input_data
        self.show = show
        self.settings_path = settings_path
        constants.NUMBER_OF_EDGES = randint(int(1.3 * constants.NUMBER_OF_BASE_BLOCKS),
                                            2 * (constants.NUMBER_OF_BASE_BLOCKS - 1))

    def _read_settings(self):
        with open(self.settings_path, 'rt', encoding='utf-8') as f:
            CFG.settings = json.load(f)

    def run(self):
        self._read_settings()
        if constants.NUMBER_OF_BASE_BLOCKS:
            cfg = CFG(constants.NUMBER_OF_BASE_BLOCKS, constants.NUMBER_OF_EDGES)
        else:
            cfg = deserialize_cfg(self.file_path_to_read)
        if self.name_of_file_to_save: serialize_cfg(cfg, self.name_of_file_to_save)
        if constants.INPUT_DATA: CFA.cfg_traversal(cfg, constants.INPUT_DATA)
        if self.show: CFGVisualizer.visualize_cfg(cfg)
        #CFGVisualizer.visualize_cfg(cfg)
        # print(serialize_cfg(cfg))
        # CFGVisualizer.visualize_cfg(deserialize_cfg(serialize_cfg(cfg)))
        # CFA.cfg_traversal(cfg, 10)
        # CFGVisualizer.visualize_cfg(cfg)

