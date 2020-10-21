"""
5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и
преобразовать результаты из байтовового в строковый тип на кириллице.

Подсказки:
--- используйте модуль chardet!!!
"""

import subprocess
import chardet

RESOURCES = ['radif.ru', 'ya.ru', 'youtu.be', 'vk.ru', 'ok.ru']

for resource in RESOURCES:
    subprocess_ping = subprocess.Popen(['ping', resource], stdout=subprocess.PIPE)
    for line in subprocess_ping.stdout:
        print(line.decode(chardet.detect(line)['encoding']))
