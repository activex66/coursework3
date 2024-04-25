import pytest

from src.dto import Payment, Operation
from datetime import datetime


def test_init_from_str():
    payment = Payment.init_from_str('Visa Classic 6831982476737658')
    assert payment.name == 'Visa Classic'
    assert payment.number == '6831982476737658'


def test_safe_payment_for_amount():
    payment = Payment(name='счет', number='64686473678894779589')
    assert payment.safe() == 'счет **9589'


def test_safe_payment_for_card_number():
    payment = Payment(name='MasterCard', number='7158300734726758')
    assert payment.safe() == 'MasterCard 7158 30** **** 6758'


def test_split_card_number_by_block():
    card_number = '7158300734726758'
    result = Payment.split_card_number_by_block(card_number)
    assert result == '7158 3007 3472 6758'


def test_init_operation_from_dict(operation_data_without_from):
    op = Operation.init_from_dict(operation_data_without_from)

    assert op.id == 522357576
    assert op.state == "EXECUTED"
    assert op.date == datetime(2019, 7, 12, 20, 41, 47, 882230)
    assert op.amount.value == 51463.70
    assert op.amount.currency_name == "USD"
    assert op.amount.currency_code == "USD"
    assert op.description == "Открытие вклада"
    assert op.payment_to.name == "Счет"
    assert op.payment_to.number == "38976430693692818358"
    assert op.payment_from is None


def test_safe_operation_data_with_from(operation_data_with_from):
    operation = Operation.init_from_dict(operation_data_with_from)
    expected_result = (
        '12.07.2019 Перевод организации\n'
        'Visa Classic 6831 98** **** 7658 -> Счет **8358\n'
        '51463.70 USD'

    )
    return operation.safe() == expected_result


def test_safe_operation_data_without_from(operation_data_without_from):
    operation = Operation.init_from_dict(operation_data_without_from)
    expected_result = (
        '12.07.2019 Открытие вклада\n'
        'Счет **8358'
        '51463.70 USD'

    )
    return operation.safe() == expected_result
