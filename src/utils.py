import json
from src.dto import Operation


def get_operations(failname) -> list[Operation]:
    operations: list[Operation] = []
    with open(failname, encoding="utf-8") as f:
        for data in json.load(f):
            if data:
                op = Operation.init_from_dict(data)
                operations.append(op)

    return operations


def filter_operation_by_state(*operations: Operation, state: str) -> list[Operation]:
    """
    Фильтрует операции по их статусу
    """
    filtered_operations: list[Operation] = []
    for op in operations:
        if op.state == state:
            filtered_operations.append(op)
    return filtered_operations


def sort_operation_by_data(*operations: Operation) -> list[Operation]:
    """
    Сортировка операций по дате поступления в обратном порядке
    """
    return sorted(operations, key=lambda op: op.date, reverse=True)
