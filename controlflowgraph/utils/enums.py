from enum import Enum


class ComparisonOperators(Enum):
    NO_CONDITION = 0            # no condition
    EQUALITY = 1                # ==
    INEQUALITY = 2              # !=
    LESS_THAN = 3               # <
    GREATER_THAN = 4            # >
    LESS_THAN_OR_EQUAL = 5      # <=
    GREATER_THAN_OR_EQUAL = 6   # >=
    COMPARABLE_MODULO = 7       # % ==
    INCOMPARABLY_MODULO = 8     # % !=


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
