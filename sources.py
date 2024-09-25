from random import randint

INPUT_DATA = None
NUMBER_OF_VERTICES = None
RANGE_OF_NUMBER_OF_EDGES = None


def reading_data():
    global INPUT_DATA, NUMBER_OF_VERTICES, RANGE_OF_NUMBER_OF_EDGES
    print("Введите количество вершин:", end=' ')
    NUMBER_OF_VERTICES = int(input())
    RANGE_OF_NUMBER_OF_EDGES = randint(NUMBER_OF_VERTICES // 5 * (NUMBER_OF_VERTICES - 1),
                                       (NUMBER_OF_VERTICES - 1) ** 2 + 1)
