import pytest


@pytest.fixture
def operation_data_with_from() -> dict:
    return {
        "id": 522357576,
        "state": "EXECUTED",
        "date": "2019-07-12T20:41:47.882230",
        "operationAmount": {
            "amount": "51463.70",
            "currency": {
                "name": "USD",
                "code": "USD"
            }
        },
        "description": "Перевод организации",
        "from": "Visa Classic 6831982476737658",
        "to": "Счет 38976430693692818358"
    }


@pytest.fixture
def operation_data_without_from(operation_data_with_from):
    operation_data_with_from['description'] = 'Открытие вклада'
    del operation_data_with_from['from']
    return operation_data_with_from
