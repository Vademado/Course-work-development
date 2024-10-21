from utils import ComparisonOperators, Operations
from random import randint, choice


class BaseBlock:
    id = 0

    def __init__(self, operations, input_data=None):
        self.id = BaseBlock.id
        BaseBlock.id += 1
        self.operations = operations
        self.edges = []

    def _block_execution(self, input_data):
        for operation in self.operations:
            match operation[0]:
                case Operations.ADDITION:
                    input_data += operation[1]
                case Operations.SUBTRACTION:
                    input_data -= operation[1]
                case Operations.MULTIPLICATION:
                    input_data *= operation[1]
                case Operations.DIVISION:
                    if operation[1]:
                        input_data //= operation[1]
                    else:
                        raise ValueError("Division by zero is not allowed.")
                case Operations.EXPONENTIATION:
                    input_data **= operation[1]
                case Operations.DIVISION_BY_MODULUS:
                    if operation[1]:
                        input_data %= operation[1]
                    else:
                        raise ValueError("Division by zero is not allowed.")
                case Operations.BIT_SHIFT_TO_LEFT:
                    input_data <<= operation[1]
                case Operations.BIT_SHIFT_TO_RIGHT:
                    input_data >>= operation[1]
                case Operations.BITWISE_OR:
                    input_data |= operation[1]
                case Operations.BITWISE_EXCLUSIVE_OR:
                    input_data ^= operation[1]
                case Operations.BITWISE_AND:
                    input_data &= operation[1]
                case Operations.BIT_INVERSION:
                    input_data = ~input_data

    def add_edge(self, edge):
        self.edges.append(edge)


class Edge:
    def __init__(self, from_base_block, to_base_block, condition):
        self.from_base_block = from_base_block
        self.to_base_block = to_base_block
        self.condition = condition


class CFG:
    settings = dict()

    def __init__(self, number_base_blocks, number_edges, input_data, generation=True):
        self.number_base_blocks = number_base_blocks
        self.number_edges = number_edges
        self.input_data = input_data
        self.dictionary_base_blocks = {}
        if generation: self._generate_cfg()

    def _generate_cfg(self):
        base_blocks_settings = CFG.settings["base_blocks"]["number_operations"]
        settings_comparison_operators = CFG.settings["comparison_operators"]
        operation_settings = CFG.settings["operations"]

        for i in range(self.number_base_blocks):
            number_operations = randint(base_blocks_settings["lower_bound"], base_blocks_settings["upper_bound"])
            operations = []
            for j in range(number_operations):
                index_operation = randint(0, len(Operations) - 1)
                value_operand = None if Operations(index_operation) == Operations.BIT_INVERSION else randint(operation_settings[Operations(index_operation).name.lower()]["lower_bound"], operation_settings[Operations(index_operation).name.lower()]["upper_bound"])
                operations.append((Operations(index_operation), value_operand))
            self.dictionary_base_blocks[i] = BaseBlock(operations, None if i else self.input_data)

        self._base_blocks_related_with_initial_base_block = {0}
        self._base_blocks_unrelated_with_initial_base_block= set(range(1, self.number_base_blocks))

        for i in range(self.number_edges):
            if len(self._base_blocks_unrelated_with_initial_base_block) == self.number_edges - i:
                to_base_block = choice(list(self._base_blocks_unrelated_with_initial_base_block))
                while True:
                    from_base_block = choice(list(self._base_blocks_related_with_initial_base_block))
                    if len(self.dictionary_base_blocks[from_base_block].edges) < 2: break
                self.dfs(to_base_block)
            else:
                while True:
                    from_base_block = randint(0, self.number_base_blocks - 1)
                    to_base_block = randint(0, self.number_base_blocks - 1)
                    if len(self.dictionary_base_blocks[from_base_block].edges) < 2 and to_base_block: break

            if self.dictionary_base_blocks[from_base_block].edges:
                first_edge_condition = self.dictionary_base_blocks[from_base_block].edges[0].condition
                match first_edge_condition[0]:
                    case ComparisonOperators.EQUALITY:
                        new_condition = (
                            ComparisonOperators.INEQUALITY, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.INEQUALITY:
                        new_condition = (
                            ComparisonOperators.EQUALITY, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.LESS_THAN:
                        new_condition = (
                            ComparisonOperators.GREATER_THAN_OR_EQUAL, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.GREATER_THAN:
                        new_condition = (
                            ComparisonOperators.LESS_THAN_OR_EQUAL, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.LESS_THAN_OR_EQUAL:
                        new_condition = (
                            ComparisonOperators.GREATER_THAN, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.GREATER_THAN_OR_EQUAL:
                        new_condition = (
                            ComparisonOperators.LESS_THAN, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.COMPARABLE_MODULO:
                        new_condition = (
                            ComparisonOperators.INCOMPARABLY_MODULO, first_edge_condition[1], first_edge_condition[2])
                    case ComparisonOperators.INCOMPARABLY_MODULO:
                        new_condition = (
                            ComparisonOperators.COMPARABLE_MODULO, first_edge_condition[1], first_edge_condition[2])
            else:
                comparison_operator = ComparisonOperators(randint(0, len(ComparisonOperators) - 1))
                if comparison_operator == ComparisonOperators.COMPARABLE_MODULO or comparison_operator == ComparisonOperators.INCOMPARABLY_MODULO:
                    module = randint(settings_comparison_operators[comparison_operator.name.lower()]["lower_bound"], settings_comparison_operators[comparison_operator.name.lower()]["upper_bound"])
                    value_for_comparison = randint(0, module - 1)
                else:
                    module = None
                    value_for_comparison = randint(settings_comparison_operators[comparison_operator.name.lower()]["lower_bound"], settings_comparison_operators[comparison_operator.name.lower()]["upper_bound"])
                new_condition = (comparison_operator, module, value_for_comparison)
            self.dictionary_base_blocks[from_base_block].add_edge(Edge(from_base_block, to_base_block, new_condition))
        BaseBlock.id = 0

    def dfs(self, id_base_block, visited_base_blocks=None):
        if visited_base_blocks is None: visited_base_blocks = [False] * self.number_base_blocks
        visited_base_blocks[id_base_block] = True
        self._base_blocks_related_with_initial_base_block.add(id_base_block)
        self._base_blocks_unrelated_with_initial_base_block.discard(id_base_block)
        for edge in self.dictionary_base_blocks[id_base_block].edges:
            if not visited_base_blocks[edge.to_base_block]:
                self.dfs(edge.to_base_block, visited_base_blocks)

    def get_dictionary_base_blocks(self):
        return self.dictionary_base_blocks
