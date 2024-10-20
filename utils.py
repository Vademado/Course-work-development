from enum import Enum


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