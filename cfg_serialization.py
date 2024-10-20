from construct import *
from CFG import *

operation_enum = Enum(Int8ub,
                      ADDITION=Operations.ADDITION.value,
                      SUBTRACTION=Operations.SUBTRACTION.value,
                      MULTIPLICATION=Operations.MULTIPLICATION.value,
                      DIVISION=Operations.DIVISION.value,
                      EXPONENTIATION=Operations.EXPONENTIATION.value,
                      DIVISION_BY_MODULUS=Operations.DIVISION_BY_MODULUS.value,
                      BIT_SHIFT_TO_LEFT=Operations.BIT_SHIFT_TO_LEFT.value,
                      BIT_SHIFT_TO_RIGHT=Operations.BIT_SHIFT_TO_RIGHT.value,
                      BITWISE_OR=Operations.BITWISE_OR.value,
                      BITWISE_EXCLUSIVE_OR=Operations.BITWISE_EXCLUSIVE_OR.value,
                      BITWISE_AND=Operations.BITWISE_AND.value,
                      BIT_INVERSION=Operations.BIT_INVERSION.value
                      )

comparison_enum = Enum(Int8ub,
                       EQUALITY=ComparisonOperators.EQUALITY.value,
                       INEQUALITY=ComparisonOperators.INEQUALITY.value,
                       LESS_THAN=ComparisonOperators.LESS_THAN.value,
                       GREATER_THAN=ComparisonOperators.GREATER_THAN.value,
                       LESS_THAN_OR_EQUAL=ComparisonOperators.LESS_THAN_OR_EQUAL.value,
                       GREATER_THAN_OR_EQUAL=ComparisonOperators.GREATER_THAN_OR_EQUAL.value,
                       COMPARABLE_MODULO=ComparisonOperators.COMPARABLE_MODULO.value,
                       INCOMPARABLY_MODULO=ComparisonOperators.INCOMPARABLY_MODULO.value
                       )

operation_struct = Struct(
    "operation" / operation_enum,
    "operand" / Int64sb
)

condition_struct = Struct(
    "condition_operator" / comparison_enum,
    "module" / Int64ub,
    "comparison_value" / Int64sb
)

edge_struct = Struct(
    "from_base_block" / Int16ub,
    "to_base_block" / Int16ub,
    "condition" / condition_struct
)

base_block_struct = Struct(
    "id" / Int16ub,  # id блока
    "operations" / PrefixedArray(Int8ub, operation_struct),
    "edges" / PrefixedArray(Int8ub, edge_struct)
)

cfg_struct = Struct(
    "number_base_blocks" / Int16ub,
    "number_edges" / Int32ub,
    "base_blocks" / PrefixedArray(Int16ub, base_block_struct)
)


def serialize_cfg(cfg):
    serialized_data = cfg_struct.build({
        "number_base_blocks": cfg.number_base_blocks,
        "number_edges": cfg.number_edges,
        "base_blocks": [
            {
                "id": block.id,
                "operations": [
                    {"operation": operation[0].value, "operand": operation[1] if operation[1] is not None else 0} for
                    operation in block.operations
                ],
                "edges": [
                    {
                        "from_base_block": edge.from_base_block,
                        "to_base_block": edge.to_base_block,
                        "condition": {
                            "condition_operator": edge.condition[0].value,
                            "module": edge.condition[1] if edge.condition[1] is not None else 0,
                            "comparison_value": edge.condition[2]
                        }
                    } for edge in block.edges
                ]
            } for block in cfg.dictionary_base_blocks.values()
        ]
    })
    with open("cfg.bin", 'wb') as f:
        f.write(serialized_data)
        f.close()
    return serialized_data


def deserialize_cfg(serialized_data):
    parsed_data = cfg_struct.parse(serialized_data)
    cfg = CFG(parsed_data.number_base_blocks, parsed_data.number_edges, input_data=None, generation=False)
    for base_block_data in parsed_data.base_blocks:
        base_block = BaseBlock([(Operations(op.operation), op.operand) for op in base_block_data.operations])
        for edge_data in base_block_data.edges:
            condition = (
                ComparisonOperators(edge_data.condition_operator),
                edge_data.module if edge_data.module != 0 else None,
                edge_data.comparison_value
            )
            base_block.add_edge(Edge(edge_data.from_base_block, edge_data.to_base_block, condition))
        cfg.dictionary_base_blocks[base_block.id] = base_block
    return cfg
