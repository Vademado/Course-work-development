import argparse
from src.app.App import App

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)

group.add_argument("-n", "--number-base-blocks", help="sets the number of base blocks", metavar="", type=int)
group.add_argument("-r", "--read", help="read a control flow graph", metavar="", type=str)

parser.add_argument("-sv", "--save", help="sets the name of the file in which the control flow graph will be saved", metavar="", type=str, required=False)
parser.add_argument("-inp", "--input-data", help="sets the value of the input data", metavar="", type=int, required=False)
parser.add_argument("-sh", "--show", help="show the control flow graph", action="store_true")

args = parser.parse_args()
print(f"n={args.number_base_blocks} r={args.read} save={args.save} inp={args.input_data} show={args.show}")

if __name__ == '__main__':
    app = App(args.number_base_blocks, args.read, args.input_data, args.show)
    app.run()
