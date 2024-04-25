from src.utils import get_operations, filter_operation_by_state, sort_operation_by_data


def main(failname='operations.json'):
    operations = get_operations(failname)
    operations = filter_operation_by_state(*operations, state='EXECUTED')
    operations = sort_operation_by_data(*operations)
    for op in operations[:5]:
        print(op.safe())
        print()


if __name__ == "__main__":
    operations_path = input('Введите путь до файла с операциями\n')
    main(operations_path)
