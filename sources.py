import json
from random import randint
from enum import Enum
import graphviz


class Constants:
    INPUT_DATA = None
    NUMBER_OF_BASE_BLOCKS = None
    NUMBER_OF_EDGES = None
    SETTINGS = None


class ComparisonOperators(Enum):
    EQUALITY = 0                # ==
    INEQUALITY = 1              # !=
    LESS_THAN = 2               # <
    GREATER_THAN = 3            # >
    LESS_THAN_OR_EQUAL = 4      # <=
    GREATER_THAN_OR_EQUAL = 5   # >=
    COMPARABLE_MODULO = 6       # % ==
    INCOMPARABLY_MODULO = 7     # % !=


class Operations(Enum):
    ADDITION = 0                # +=
    SUBTRACTION = 1             # -=
    MULTIPLICATION = 2          # *=
    DIVISION = 3                # //=
    EXPONENTIATION = 4          # **=
    DIVISION_BY_MODULUS = 5     # %=
    BIT_SHIFT_TO_LEFT = 6       # <<
    BIT_SHIFT_TO_RIGHT = 7      # >>
    BITWISE_OR = 8              # x|y
    BITWISE_EXCLUSIVE_OR = 9    # x^y
    BITWISE_AND = 10            # x&y
    BIT_INVERSION = 11          # ~x


def read_data():
    print("Введите количество вершин:", end=' ')
    Constants.NUMBER_OF_BASE_BLOCKS = int(input())
    Constants.NUMBER_OF_EDGES = randint(int(1.3 * Constants.NUMBER_OF_BASE_BLOCKS),
                                        2 * (Constants.NUMBER_OF_BASE_BLOCKS - 1))


def read_settings():
    with open('config/settings.json', 'r', encoding='utf-8') as f:
        Constants.SETTINGS = json.load(f)


def operations_in_base_block_convert_to_string(base_block):
    string_operations_in_base_block = ""
    if base_block.id == 0:
        string_operations_in_base_block += "INITIAL BLOCK\n\n"
    else:
        string_operations_in_base_block += f"{base_block.id}\n\n"
    for operation in base_block.get_operations():
        match operation[0]:
            case Operations.ADDITION:
                string_operations_in_base_block += f"X += {operation[1]}\n"
            case Operations.SUBTRACTION:
                string_operations_in_base_block += f"X -= {operation[1]}\n"
            case Operations.MULTIPLICATION:
                string_operations_in_base_block += f"X *= {operation[1]}\n"
            case Operations.DIVISION:
                string_operations_in_base_block += f"X //= {operation[1]}\n"
            case Operations.EXPONENTIATION:
                string_operations_in_base_block += f"X **= {operation[1]}\n"
            case Operations.DIVISION_BY_MODULUS:
                string_operations_in_base_block += f"X %= {operation[1]}\n"
            case Operations.BIT_SHIFT_TO_LEFT:
                string_operations_in_base_block += f"X << {operation[1]}\n"
            case Operations.BIT_SHIFT_TO_RIGHT:
                string_operations_in_base_block += f"X >> {operation[1]}\n"
            case Operations.BITWISE_OR:
                string_operations_in_base_block += f"X | {operation[1]}\n"
            case Operations.BITWISE_EXCLUSIVE_OR:
                string_operations_in_base_block += f"X ^ {operation[1]}\n"
            case Operations.BITWISE_AND:
                string_operations_in_base_block += f"X & {operation[1]}\n"
            case Operations.BIT_INVERSION:
                string_operations_in_base_block += "~X\n"
    return string_operations_in_base_block


def condition_in_edge_convert_to_string(edge):
    condition = edge.get_condition()
    match condition[0]:
        case ComparisonOperators.EQUALITY:
            string_condition = f"X == {condition[2]}"
        case ComparisonOperators.INEQUALITY:
            string_condition = f"X != {condition[2]}"
        case ComparisonOperators.LESS_THAN:
            string_condition = f"X < {condition[2]}"
        case ComparisonOperators.GREATER_THAN:
            string_condition = f"X > {condition[2]}"
        case ComparisonOperators.LESS_THAN_OR_EQUAL:
            string_condition = f"X <= {condition[2]}"
        case ComparisonOperators.GREATER_THAN_OR_EQUAL:
            string_condition = f"X >= {condition[2]}"
        case ComparisonOperators.COMPARABLE_MODULO:
            string_condition = f"X % {condition[1]} == {condition[2]}"
        case ComparisonOperators.INCOMPARABLY_MODULO:
            string_condition = f"X % {condition[1]} != {condition[2]}"
    return string_condition


def visualize_cfg(cfg):
    dot = graphviz.Digraph(comment='Control-flow graph')

    for id_base_block, base_block in cfg.get_dictionary_base_blocks().items():
        operations_in_base_block = operations_in_base_block_convert_to_string(base_block)
        dot.node(str(id_base_block), operations_in_base_block)

    for id_base_block, base_block in cfg.get_dictionary_base_blocks().items():
        for edge in base_block.get_edges():
            condition_in_edge = condition_in_edge_convert_to_string(edge)
            dot.edge(str(edge.get_from_base_block_id()), str(edge.get_to_base_block_id()), condition_in_edge)

    # dot.render('Control-flow graph', format='png')
    dot.render('Control-flow graph', view=True)
