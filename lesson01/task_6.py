"""
6. Создать программно текстовый файл test_file.txt, заполнить его тремя строками:
«сетевое программирование», «сокет», «декоратор».
Проверить кодировку файла по умолчанию.

Принудительно открыть файл в формате Unicode и вывести его содержимое.

Подсказки:
--- обратите внимание, что заполнять файл вы можете в любой кодировке
но открыть нужно ИМЕННО в формате Unicode (utf-8)

например, with open('test_file.txt', encoding='utf-8') as t_f
невыполнение условия - минус балл
"""
import locale

default_encoding = locale.getpreferredencoding()
print('Стандартная кодировка -', default_encoding, end='\n\n')

LINES = ['сетевое программирование', 'сокет', 'декоратор']
with open('./test_file.txt', mode='w') as file:
    for line in LINES:
        file.write(f'{line}\n')


# На конкретном устройстве стандартная кодировка cp1251, в результате отлова ошибки
# данные перекодируются в utf-8
try:
    with open('./test_file.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            print(line, end='')
except UnicodeDecodeError as exception:
    file_contents = ''
    with open('./test_file.txt', mode='r', encoding=default_encoding) as file:
        for line in file:
            file_contents += line
    with open('./test_file.txt', mode='w', encoding='utf-8') as file:
        file.write(file_contents)
    with open('./test_file.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            print(line, end='')

# Лучший вариант:

# from chardet import detect
#
# LINES_LST = ['сетевое программирование', 'сокет', 'декоратор']
# with open('test.txt', 'w') as file:
#     for line in LINES_LST:
#         file.write(f'{line}\n')
# file.close()
#
#
# def encoding_convert():
#     """Конвертация"""
#     with open('test.txt', 'rb') as f_obj:
#         content_bytes = f_obj.read()
#     detected = detect(content_bytes)
#     encoding = detected['encoding']
#     content_text = content_bytes.decode(encoding)
#     with open('test.txt', 'w', encoding='utf-8') as f_obj:
#         f_obj.write(content_text)
#
#
# encoding_convert()
#
# # открываем файл в правильной кодировке
# with open('test.txt', 'r', encoding='utf-8') as file:
#     CONTENT = file.read()
# print(CONTENT)
