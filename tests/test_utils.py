from src.dto import Operation
from src.utils import filter_operation_by_state
from pytest import fixture


@fixture
def canceled_operation(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    operation.state = 'CANCELED'
    return operation


@fixture
def executed_operation(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    operation.state = 'EXECUTED'
    return operation


def test_filtered_operations(canceled_operation, executed_operation):
    operation = executed_operation, canceled_operation

    [op] = filter_operation_by_state(*operation, state='CANCELED')
    assert op == canceled_operation

    [op] = filter_operation_by_state(*operation, state='EXECUTED')
    assert op == executed_operation
