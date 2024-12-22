import argparse

from controlflowgraph.app.App import App

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-n", "--number-base-blocks", help="sets the number of base blocks", metavar="", type=int)
group.add_argument("-r", "--read", help="read a control flow graph", metavar="", type=str)

parser.add_argument("-sv", "--save", help="sets the name of the file in which the control flow graph will be saved", metavar="", type=str, required=False)
parser.add_argument("-inp", "--input-data", help="sets the value of the input data", metavar="", type=int, required=False)
parser.add_argument("-out", "--save-out", help="sets the name of the file in which the control flow graph coverage will be saved.", metavar="", type=str, required=False)
parser.add_argument("-conf", "--config", help="sets the path to the settings", metavar="", type=str, default="config/settings.json", required=False)
parser.add_argument("-sh", "--show", help="show the control flow graph", action="store_true")

args = parser.parse_args()

if __name__ == '__main__':
    app = App(args.number_base_blocks, args.read, args.save, args.save_out, args.input_data, args.config, args.show)
    app.run()
