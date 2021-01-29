"""
3. Задание на закрепление знаний по модулю yaml.
 Написать скрипт, автоматизирующий сохранение данных
 в файле YAML-формата.
Для этого:

Подготовить данные для записи в виде словаря, в котором
первому ключу соответствует список, второму — целое число,
третьему — вложенный словарь, где значение каждого ключа —
это целое число с юникод-символом, отсутствующим в кодировке
ASCII(например, €);

Реализовать сохранение данных в файл формата YAML — например,
в файл file.yaml. При этом обеспечить стилизацию файла с помощью
параметра default_flow_style, а также установить возможность работы
с юникодом: allow_unicode = True;

Реализовать считывание данных из созданного файла и проверить,
совпадают ли они с исходными.
"""
import yaml

DATA_TO_YAML = {
    'my_list': [
        'table',
        'chair',
        'wardrobe'
    ],
    'my_number': 222,
    'my_dict': {
        'el1': '25€',
        'el2': '20€'
    }
}


def write_to_yaml(data_to_yaml):
    """
    Функция для записи данных в YAML формате
    :param data_to_yaml: данные
    """
    with open('my_data.yaml', mode='w', encoding='utf-8') as file:
        yaml.dump(data_to_yaml, file, default_flow_style=True, allow_unicode=True)


def read_to_yaml():
    """
    Функция для чтения файлов в YAML формате
    :return: возвращает результат чтения
    """
    with open('my_data.yaml', encoding='utf-8') as file:
        file_content = yaml.load(file, Loader=yaml.FullLoader)
    return file_content


write_to_yaml(DATA_TO_YAML)
print(read_to_yaml())
