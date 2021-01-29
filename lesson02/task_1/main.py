"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""
import csv
import re

DATA_FILE_PATHS = ['info_1.txt', 'info_2.txt', 'info_3.txt']
EXTRACTED_PARAMETERS = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']
CSV_FILE_NAME = 'task_result.csv'


def get_data(data_file_paths, extracted_parameters):
    """
    Функция для выборки данных из текстового файла
    :param data_file_paths: Пути файлов
    :param extracted_parameters: Параметры извлекаемых данных
    :return: Полученные данные в результате выборки
    """
    os_prod_list, os_name_list, os_code_list, os_type_list = [], [], [], []

    for file_path in data_file_paths:
        with open(file_path) as file:
            for string in file.readlines():
                list_of_string = [el.rstrip() for el in re.split(':\s+', string)]
                for el in list_of_string:
                    if el in extracted_parameters:
                        if el == EXTRACTED_PARAMETERS[0]:
                            os_prod_list.append(list_of_string[-1])
                        elif el == EXTRACTED_PARAMETERS[1]:
                            os_name_list.append(list_of_string[-1])
                        elif el == EXTRACTED_PARAMETERS[2]:
                            os_code_list.append(list_of_string[-1])
                        elif el == EXTRACTED_PARAMETERS[3]:
                            os_type_list.append(list_of_string[-1])
    return [
        extracted_parameters,
        os_prod_list,
        os_name_list,
        os_code_list,
        os_type_list
    ]


def write_to_csv(csv_file_name):
    """
    Функция записи данных в CSV файл
    :param csv_file_name: Путь к файлу
    """
    data = get_data(DATA_FILE_PATHS, EXTRACTED_PARAMETERS)
    column_names = data[0]
    data_rows = list(zip(*data[1:]))
    with open(csv_file_name, mode='w', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(column_names)
        for row in data_rows:
            csv_writer.writerow(row)


write_to_csv(CSV_FILE_NAME)
