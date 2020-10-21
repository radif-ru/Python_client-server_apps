"""
2. Каждое из слов «class», «function», «method» записать в байтовом формате
без преобразования в последовательность кодов
не используя методы encode и decode)
и определить тип, содержимое и длину соответствующих переменных.

Подсказки:
--- b'class' - используйте маркировку b''
--- используйте списки и циклы, не дублируйте функции
"""

WORDS = ['class', 'function', 'method']

for word in WORDS:
    word_bytes = bytes(word, 'utf-8')
    print(f"{word_bytes} - {type(word_bytes)} - len {len(word_bytes)}")
