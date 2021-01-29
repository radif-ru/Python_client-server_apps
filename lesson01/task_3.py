"""
3. Определить, какие из слов «attribute», «класс», «функция», «type»
невозможно записать в байтовом типе с помощью маркировки b'' (без encode decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
--- усложните задачу, "отловив" и обработав исключение
"""

WORDS = ['attribute', 'класс', 'type']

for word in WORDS:
    try:
        word_bytes = bytes(word, 'utf-8')
        if len(word) != len(word_bytes):
            # чтобы по заданию отловить исключение пришлось его создать:
            raise UnicodeError(
                f'Слово "{word}" невозможно записать в байтовом типе '
                f'с помощью маркировки b\'\' (без encode decode)')
        print(f"{word_bytes} - {type(word_bytes)} - len {len(word_bytes)}")
    except UnicodeError as exception:
        print(exception)
