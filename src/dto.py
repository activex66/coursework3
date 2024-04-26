from datetime import datetime


class Payment:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    @classmethod
    def init_from_str(cls, payment):
        *name, number = payment.split(' ')
        return cls(' '.join(name), number)

    def __repr__(self):  # pragma: nocover
        return f'payment(name={self.name}, number={self.number})'

    def safe(self) -> str:
        """
        Определяет, откуда поступает операция - счет или карта
        """
        if self.name.lower() == 'счет':
            safe_number = self._get_safe_account()
        else:
            safe_number = self._get_safe_card_number()
            safe_number = self.split_card_number_by_block(safe_number)
        return f'{self.name} {safe_number}'

    def _get_safe_account(self) -> str:
        """
        Шифрует номер счета
        """
        return '*' * 2 + self.number[-4:]

    def _get_safe_card_number(self) -> str:
        """
        Шифрует номер счета
        """
        start, middle, end = self.number[:6], self.number[6:-4], self.number[-4:]
        return start + '*' * len(middle) + end

    @staticmethod
    def split_card_number_by_block(card_number: str) -> str:
        """
        Разделяет номер карты на 4 блока
        """
        block_size = (4, 4, 4, 4)
        result = []
        for bs in block_size:
            block, tail = card_number[:bs], card_number[bs:]
            result.append(block)
            card_number = tail
        return ' '.join(result)


class Amount:
    def __init__(self, value, currency_name, currency_code):
        self.value = value
        self.currency_name = currency_name
        self.currency_code = currency_code

    def __repr__(self):  # pragma: nocover
        return f'Amount(value={self.value}, currency_name={self.currency_name})'


class Operation:
    def __init__(
        self,
        operation_id,
        state,
        operation_data,
        amount,
        description,
        payment_to,
        payment_from=None

    ):
        self.id = operation_id
        self.state = state
        self.date = operation_data
        self.amount = amount
        self.description = description
        self.payment_to = payment_to
        self.payment_from = payment_from

    def __repr__(self):  # pragma: nocover
        return (
            f'operation('
            f'{self.id}, {self.description}, state={self.state}, date={self.date}, amount={self.amount},'
            f'from={self.payment_from} to={self.payment_to}'
            f')'
        )

    @classmethod
    def init_from_dict(cls, data):
        return cls(
            operation_id=int(data["id"]),
            state=data['state'],
            operation_data=datetime.fromisoformat(data['date']),
            amount=Amount(
                value=float(data['operationAmount']['amount']),
                currency_name=(data['operationAmount']['currency']['name']),
                currency_code=(data['operationAmount']['currency']['code'])
            ),
            description=data['description'],
            payment_to=Payment.init_from_str(data['to']),
            payment_from=Payment.init_from_str(data['from']) if 'from' in data else None
        )

    def safe(self) -> str:
        """
        Вывод операции
        """
        lines = [f'{self.date.strftime("%d.%m.%Y")} {self.description}',]
        if self.payment_from:
            lines.append(f'{self.payment_from.safe()} -> {self.payment_to.safe()}')
        else:
            lines.append(f'{self.payment_to.safe()}')

        lines.append(f'{self.amount.value:.2f} {self.amount.currency_name}')
        return '\n'.join(lines)
