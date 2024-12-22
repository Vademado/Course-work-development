from controlflowgraph.cfg.CFG import CFG, BaseBlock
from controlflowgraph.utils.enums import ComparisonOperators, Operations


class CFA:
    @staticmethod
    def cfg_traversal(cfg: CFG, input_data: int, file_path_to_save_coverage: str):
        print(f"Input data: {input_data}")
        to_base_block = 0
        hang_indicator = cfg.number_base_blocks ** 2
        path = []
        while to_base_block != -1:
            print(f"Moving base block {to_base_block}, input: {input_data}", end=", ")
            path.append(to_base_block)
            input_data = CFA._block_execution(cfg.dictionary_base_blocks[to_base_block], input_data)
            print(f"output: {input_data}")
            to_base_block = CFA._go_to_next_base_block(cfg.dictionary_base_blocks[to_base_block], input_data)
            hang_indicator -= 1
            if not hang_indicator:
                print("hang detected")
                break

        if file_path_to_save_coverage:
            with open(f"{file_path_to_save_coverage}.bin", "wb") as f:
                f.write(b''.join([base_block.to_bytes(2, byteorder='big') for base_block in path]))

        print(path)

    @staticmethod
    def _block_execution(base_block: BaseBlock, input_data: int) -> int:
        for operation, value_operand in base_block.operations:
            match operation:
                case Operations.ADDITION:
                    input_data += value_operand
                case Operations.SUBTRACTION:
                    input_data -= value_operand
                case Operations.MULTIPLICATION:
                    input_data *= value_operand
                case Operations.DIVISION:
                    if value_operand:
                        input_data //= value_operand
                    else:
                        raise ValueError("Division by zero is not allowed.")
                case Operations.EXPONENTIATION:
                    input_data **= value_operand
                case Operations.DIVISION_BY_MODULUS:
                    if value_operand:
                        input_data %= value_operand
                    else:
                        raise ValueError("Division by zero is not allowed.")
                case Operations.BIT_SHIFT_TO_LEFT:
                    input_data <<= value_operand
                case Operations.BIT_SHIFT_TO_RIGHT:
                    input_data >>= value_operand
                case Operations.BITWISE_OR:
                    input_data |= value_operand
                case Operations.BITWISE_EXCLUSIVE_OR:
                    input_data ^= value_operand
                case Operations.BITWISE_AND:
                    input_data &= value_operand
        return input_data

    @staticmethod
    def _go_to_next_base_block(base_block: BaseBlock, input_data: int) -> int:
        for from_base_block, to_base_block, condition in base_block.edges:
            comparison_operator, module, value_for_comparison = condition
            match comparison_operator:
                case ComparisonOperators.NO_CONDITION:
                    return to_base_block
                case ComparisonOperators.EQUALITY:
                    if input_data == value_for_comparison: return to_base_block
                case ComparisonOperators.INEQUALITY:
                    if input_data != value_for_comparison: return to_base_block
                case ComparisonOperators.LESS_THAN:
                    if input_data < value_for_comparison: return to_base_block
                case ComparisonOperators.GREATER_THAN:
                    if input_data > value_for_comparison: return to_base_block
                case ComparisonOperators.LESS_THAN_OR_EQUAL:
                    if input_data <= value_for_comparison: return to_base_block
                case ComparisonOperators.GREATER_THAN_OR_EQUAL:
                    if input_data >= value_for_comparison: return to_base_block
                case ComparisonOperators.COMPARABLE_MODULO:
                    if input_data % module == value_for_comparison: return to_base_block
                case ComparisonOperators.INCOMPARABLY_MODULO:
                    if input_data % module != value_for_comparison: return to_base_block
        return -1
