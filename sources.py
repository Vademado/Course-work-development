from random import randint
from enum import Enum

INPUT_DATA = None
NUMBER_OF_VERTICES = None
RANGE_OF_NUMBER_OF_EDGES = None


class ComparisonOperators(Enum):
    EQUALITY: 0               # ==
    INEQUALITY: 1             # !=
    LESS_THAN: 2              # <
    GREATER_THAN: 3           # >
    LESS_THAN_OR_EQUAL: 4     # <=
    GREATER_THAN_OR_EQUAL: 5  # >=
    COMPARABLE_MODULO: 6      # % ==
    INCOMPARABLY_MODULO: 7    # % !=


class Operations(Enum):
    ADDITION: 0               # +=
    SUBTRACTION: 1            # -=
    MULTIPLICATION: 2         # *=
    DIVISION: 3               # //=
    EXPONENTIATION: 4         # **=
    DIVISION_BY_MODULUS: 5    # %=


def reading_data():
    global INPUT_DATA, NUMBER_OF_VERTICES, RANGE_OF_NUMBER_OF_EDGES
    print("Введите количество вершин:", end=' ')
    NUMBER_OF_VERTICES = int(input())
    RANGE_OF_NUMBER_OF_EDGES = randint(1.3 * NUMBER_OF_VERTICES,
                                       2 * (NUMBER_OF_VERTICES - 1))