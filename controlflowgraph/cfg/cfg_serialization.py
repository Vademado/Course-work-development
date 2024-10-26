from construct import *

from controlflowgraph.cfg.CFG import CFG, BaseBlock, Edge
from controlflowgraph.utils.enums import ComparisonOperators, Operations

operation_struct = Struct(
    "index_operation" / Int8ub,
    "operand" / Int64sb
)

condition_struct = Struct(
    "index_condition" / Int8ub,
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


def serialize_cfg(cfg: CFG):
    serialized_data = cfg_struct.build({
        "number_base_blocks": cfg.number_base_blocks,
        "number_edges": cfg.number_edges,
        "base_blocks": [
            {
                "id": block.id,
                "operations": [
                    {"index_operation": op[0].value, "operand": op[1] if op[1] is not None else 0} for op in
                    block.operations
                ],
                "edges": [
                    {
                        "from_base_block": edge.from_base_block,
                        "to_base_block": edge.to_base_block,
                        "condition": {
                            "index_condition": edge.condition[0].value,
                            "module": edge.condition[1] if edge.condition[1] is not None else 0,
                            "comparison_value": edge.condition[2] if edge.condition[2] is not None else 0
                        }
                    } for edge in block.edges
                ]
            } for block in cfg.dictionary_base_blocks.values()
        ]
    })
    return serialized_data


def deserialize_cfg(serialized_data):
    parsed_data = cfg_struct.parse(serialized_data)
    cfg = CFG(parsed_data.number_base_blocks, parsed_data.number_edges, generation=False)
    for base_block_data in parsed_data.base_blocks:
        base_block = BaseBlock([(Operations(op.index_operation), op.operand) for op in base_block_data.operations])
        for edge_data in base_block_data.edges:
            condition = (
                ComparisonOperators(edge_data.condition.index_condition),
                edge_data.condition.module if edge_data.condition.module != 0 else None,
                edge_data.condition.comparison_value
            )
            base_block.add_edge(Edge(edge_data.from_base_block, edge_data.to_base_block, condition))
        cfg.dictionary_base_blocks[base_block_data.id] = base_block
    return cfg
