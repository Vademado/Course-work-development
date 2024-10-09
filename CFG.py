from sources import ComparisonOperators, Operations
from random import randint


# ОБРАБОТАТЬ СИТУЦИИ, КОГДА В ПРОЦЕССЕ ВЫПОЛНЕНИЯ БАЗОВОГО БЛОКА INPUT_DATA ОБРАЩАЕТСЯ В НОЛЬ

class BaseBlock:
    id = 0

    def __init__(self, operations, input_data=None):
        self.id = BaseBlock.id
        print(self.id)
        BaseBlock.id += 1
        self.__operations = operations
        self.__edges = []

    # ОПРЕДЕЛИТЬ ПОВЕДЕНИЕ ПРИ operation[1] == 0
    def __block_execution(self, input_data):
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

    def get_operations(self):
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
            operations = [(Operations(randint(0, len(Operations) - 1)), randint(-100, 100)) for _ in
                          range(number_operations)]
            # print(operations)
            self.__dictionary_base_blocks[i] = BaseBlock(operations, self.__input_data if not i else None)
        # print(self.dictionary_base_blocks)

        for _ in range(self.__number_edges):
            while True:
                from_base_block = randint(0, self.__number_base_blocks - 1)
                to_base_block = randint(0, self.__number_base_blocks - 1)
                if len(self.__dictionary_base_blocks[from_base_block].get_edges()) < 2 and  to_base_block: break
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
                self.__dictionary_base_blocks[from_base_block].add_edge(
                    Edge(from_base_block, to_base_block, new_condition))
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
                self.__dictionary_base_blocks[from_base_block].add_edge(
                    Edge(from_base_block, to_base_block, (comparison_operator, module, value_for_comparison)))

    def get_dictionary_base_blocks(self):
        return self.__dictionary_base_blocks
