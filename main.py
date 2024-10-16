from sources import Constants, read_data, read_settings, visualize_cfg
from CFG import CFG


def main():
    read_data()
    read_settings()
    cfg = CFG(Constants.NUMBER_OF_BASE_BLOCKS, Constants.NUMBER_OF_EDGES, Constants.INPUT_DATA)
    visualize_cfg(cfg)


if __name__ == '__main__':
    main()
