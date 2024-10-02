from sources import ComparisonOperators, Operations


class BaseBlock:
    id = 0

    def __int__(self, operations, input_data):
        self.__id = BaseBlock.id + 1
        BaseBlock.id += 1
        self.operations = [(Operations.ADDITION, 9)]
        self.edges = []

    def __block_execution(self, input_data):
        for operation in self.operations:
            match operation[0]:
                case Operations.ADDITION: input_data += operation[1]
            match operation[0]:
                case Operations.SUBTRACTION: input_data -= operation[1]
            match operation[0]:
                case Operations.MULTIPLICATION: input_data *= operation[1]
            match operation[0]:
                case Operations.DIVISION: input_data //= operation[1]
            match operation[0]:
                case Operations.EXPONENTIATION: input_data **= operation[1]
            match operation[0]:
                case Operations.DIVISION_BY_MODULUS: input_data %= operation[1]

    def add_edge(self, edge):
        pass


class Edge:
    def __int__(self, from_vertex, to_vertex, condition):
        self.from_vertex = from_vertex
        self.to_vertex = to_vertex


class CFG:
    def __init__(self, number_vertices, number_edges, input_data):
        self.__number_vertices = number_vertices
        self.__number_edges = number_edges
        self.adjacency_dictionary = dict()
        self.existing_vertices = set()
        self.start_vertex = None

    def __generate_cfg(self):
        for i in range(self.__number_edges):
            from_vertex = randint(0, self.__number_edges + 1)
            to_vertex = randint(0, self.__number_edges + 1)

            # if from_vertex in self.existing_vertices:
            # else:
            #     newVertex = BaseBlock('+5*2//3%56')
