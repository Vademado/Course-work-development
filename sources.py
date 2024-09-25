from random import randint

NUMBER_OF_VERTICES = 0
RANGE_OF_NUMBER_OF_EDGES = 0


def reading_data():
    global NUMBER_OF_VERTICES, RANGE_OF_NUMBER_OF_EDGES
    print("Введите количество вершин:", end=' ')
    NUMBER_OF_VERTICES = int(input())
    RANGE_OF_NUMBER_OF_EDGES = randint(NUMBER_OF_VERTICES // 5 * (NUMBER_OF_VERTICES - 1),
                                       (NUMBER_OF_VERTICES - 1) ** 2 + 1)