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
        # Выявляю кодировку detect и декодирую в этом формате, затем кодирую в байты в utf-8 и разкодирую из utf-8
        print(line.decode(chardet.detect(line)['encoding']).encode('utf-8').decode('utf-8'))
