"""
4. Преобразовать слова «разработка», «администрирование», «protocol»,
«standard» из строкового представления в байтовое и выполнить
обратное преобразование (используя методы encode и decode).

Подсказки:
--- используйте списки и циклы, не дублируйте функции
"""

WORDS = ['разработка', 'администрирование', 'protocol']

for word in WORDS:
    word_bytes = word.encode('utf-8')
    print(f"{word_bytes} - {type(word_bytes)} - len {len(word_bytes)}")
    word_bytes = word_bytes.decode('utf-8')
    print(f"{word_bytes} - {type(word_bytes)} - len {len(word_bytes)}")
