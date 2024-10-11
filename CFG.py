from sources import ComparisonOperators, Operations
from random import randint, choice


# ОБРАБОТАТЬ СИТУЦИИ, КОГДА В ПРОЦЕССЕ ВЫПОЛНЕНИЯ БАЗОВОГО БЛОКА INPUT_DATA ОБРАЩАЕТСЯ В НОЛЬ

class BaseBlock:
    id = 0

    def __init__(self, operations, input_data=None):
        self.id = BaseBlock.id
        BaseBlock.id += 1
        self.__operations = operations
        self.__edges = []

    # ОПРЕДЕЛИТЬ ПОВЕДЕНИЕ ПРИ operation[1] == 0
    def __block_execution(self, input_data):
        """Returns the data converted in the base block.

                    :param input_data: arg1
                    :type input_data: int

                    :raises ValueError: if division by zero is performed

                    :rtype: int
                    :return: the result of processing the input data in the base block
                    """
        for operation in self.__operations:
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

    def get_operations(self):
        """Return sum of multiplication of all arguments.

            :param a: arg1
            :type a: int
            :param b: arg2
            :type b: int
            :param c: arg3, defaults to 0
            :type c: int, optional

            :raises ValueError: if arg1 is equal to arg2

            :rtype: int
            :return: multiplication of all arguments
            """
        return self.__operations

    def get_edges(self):
        return self.__edges

    def add_edge(self, edge):
        self.__edges.append(edge)


class Edge:
    def __init__(self, from_base_block, to_base_block, condition):
        self.__from_base_block = from_base_block
        self.__to_base_block = to_base_block
        self.__condition = condition

    def get_from_base_block_id(self):
        return self.__from_base_block

    def get_to_base_block_id(self):
        return self.__to_base_block

    def get_condition(self):
        return self.__condition


class CFG:
    def __init__(self, number_base_blocks, number_edges, input_data):
        self.__number_base_blocks = number_base_blocks
        self.__number_edges = number_edges
        self.__input_data = input_data
        self.__dictionary_base_blocks = {}
        self.__generate_cfg()

    def __generate_cfg(self):
        for i in range(self.__number_base_blocks):
            number_operations = randint(1, len(Operations))
            # ОПРЕДЕЛИТЬ ЧИСЛЕННЫЕ ЗНАЧЕНИЕ ОПЕРАЦИИ (ПРЕДЕЛЫ)
            operations = [(Operations(randint(0, len(Operations) - 1)), randint(0, 10)) for _ in
                          range(number_operations)]
            self.__dictionary_base_blocks[i] = BaseBlock(operations, None if i else self.__input_data)

        self.__base_blocks_related_with_initial_base_block = {0}
        self.__base_blocks_unrelated_with_initial_base_block= set(range(1, self.__number_base_blocks))

        for i in range(self.__number_edges):
            if len(self.__base_blocks_unrelated_with_initial_base_block) == self.__number_edges - i:
                to_base_block = choice(list(self.__base_blocks_unrelated_with_initial_base_block))
                while True:
                    from_base_block = choice(list(self.__base_blocks_related_with_initial_base_block))
                    if len(self.__dictionary_base_blocks[from_base_block].get_edges()) < 2: break
                self.dfs(to_base_block)
            else:
                while True:
                    from_base_block = randint(0, self.__number_base_blocks - 1)
                    to_base_block = randint(0, self.__number_base_blocks - 1)
                    if len(self.__dictionary_base_blocks[from_base_block].get_edges()) < 2 and to_base_block: break

            if self.__dictionary_base_blocks[from_base_block].get_edges():
                first_edge_condition = self.__dictionary_base_blocks[from_base_block].get_edges()[0].get_condition()
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
                comparison_operator = ComparisonOperators(randint(0, 7))
                if comparison_operator == ComparisonOperators.COMPARABLE_MODULO or comparison_operator == ComparisonOperators.INCOMPARABLY_MODULO:
                    # ОПРЕДЕЛИТЬ ЧИСЛЕННЫЕ ЗНАЧЕНИЕ ОПЕРАЦИИ (ПРЕДЕЛЫ)
                    module = randint(1, 100)
                    value_for_comparison = randint(0, module - 1)
                else:
                    module = None
                    # ОПРЕДЕЛИТЬ ЧИСЛЕННЫЕ ЗНАЧЕНИЕ ОПЕРАЦИИ (ПРЕДЕЛЫ)
                    value_for_comparison = randint(-100, 100)
                new_condition = (comparison_operator, module, value_for_comparison)
            self.__dictionary_base_blocks[from_base_block].add_edge(Edge(from_base_block, to_base_block, new_condition))

    def dfs(self, id_base_block, visited_base_blocks=None):
        if visited_base_blocks is None: visited_base_blocks = [False] * self.__number_base_blocks
        visited_base_blocks[id_base_block] = True
        self.__base_blocks_related_with_initial_base_block.add(id_base_block)
        self.__base_blocks_unrelated_with_initial_base_block.discard(id_base_block)
        for edge in self.__dictionary_base_blocks[id_base_block].get_edges():
            if not visited_base_blocks[edge.get_to_base_block_id()]:
                self.dfs(edge.get_to_base_block_id(), visited_base_blocks)

    def get_dictionary_base_blocks(self):
        return self.__dictionary_base_blocks
