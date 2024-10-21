import graphviz
from resources.utils import *


class CFGVisualizer:
    @staticmethod
    def operations_in_base_block_convert_to_string(base_block):
        string_operations_in_base_block = ""
        if base_block.id == 0:
            string_operations_in_base_block += "INITIAL BLOCK\n\n"
        else:
            string_operations_in_base_block += f"{base_block.id}\n\n"
        for operation in base_block.operations:
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

    @staticmethod
    def condition_in_edge_convert_to_string(edge):
        condition = edge.condition
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

    @staticmethod
    def visualize_cfg(cfg):
        dot = graphviz.Digraph(comment='Control-flow graph')

        for id_base_block, base_block in cfg.dictionary_base_blocks.items():
            operations_in_base_block = CFGVisualizer.operations_in_base_block_convert_to_string(base_block)
            dot.node(str(id_base_block), operations_in_base_block)

        for id_base_block, base_block in cfg.dictionary_base_blocks.items():
            for edge in base_block.edges:
                condition_in_edge = CFGVisualizer.condition_in_edge_convert_to_string(edge)
                dot.edge(str(edge.from_base_block), str(edge.to_base_block), condition_in_edge)

        # dot.render('Control-flow graph', format='png')
        dot.render('Control-flow graph', view=True)