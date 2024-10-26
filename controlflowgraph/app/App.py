import json
from random import randint

from controlflowgraph.cfa.CFA import CFA
from controlflowgraph.cfg.CFG import CFG
from controlflowgraph.cfg.cfg_serialization import serialize_cfg, deserialize_cfg
from controlflowgraph.cfg.visualization.CFGVisualizer import CFGVisualizer
from controlflowgraph.utils import constants


class App:
    def __init__(self, number_of_base_blocks: int, file_path_to_read: str, file_path_to_save: str, input_data: int, settings_path: str, show: bool):
        constants.NUMBER_OF_BASE_BLOCKS = number_of_base_blocks
        self.file_path_to_read = file_path_to_read
        self.file_path_to_save = file_path_to_save
        constants.INPUT_DATA = input_data
        self.show = show
        self.settings_path = settings_path

    def _read_settings(self):
        with open(self.settings_path, 'rt', encoding='utf-8') as f:
            CFG.settings = json.load(f)

    def run(self):
        self._read_settings()
        if constants.NUMBER_OF_BASE_BLOCKS:
            constants.NUMBER_OF_EDGES = randint(int(1.3 * constants.NUMBER_OF_BASE_BLOCKS),
                                                2 * (constants.NUMBER_OF_BASE_BLOCKS - 1))
            cfg = CFG(constants.NUMBER_OF_BASE_BLOCKS, constants.NUMBER_OF_EDGES)
        else:
            with open(f"{self.file_path_to_read}.bin", "rb") as f:
                serialized_data = f.read()
                f.close()
            cfg = deserialize_cfg(serialized_data)
        if self.file_path_to_save:
            with open(f"{self.file_path_to_save}.bin", 'wb') as f:
                f.write(serialize_cfg(cfg))
                f.close()
        if constants.INPUT_DATA is not None: CFA.cfg_traversal(cfg, constants.INPUT_DATA)
        if self.show: CFGVisualizer.visualize_cfg(cfg)
