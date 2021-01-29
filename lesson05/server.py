"""Программа-сервер"""

from socket import socket, AF_INET, SOCK_STREAM
import sys
import json

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message

from logs.configs.config_server_log import LOGGER as SERVER_LOGGER  # Инициализация логирования сервера.
from errors import IncorrectDataReceivedError


def process_client_message(message):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента

    :param message:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message \
            and USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию.
    Сначала обрабатываем порт:
    server.py -p 8079 -a 192.168.1.2
    :return:
    """

    try:
        if '-p' in sys.argv:
            serv_listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            serv_listen_port = DEFAULT_PORT
        if serv_listen_port < 1024 or serv_listen_port > 65535:
            SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                                   f'{serv_listen_port}. Допустимы адреса с 1024 до 65535.')
            raise ValueError
        SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {serv_listen_port}, ')
    except IndexError:
        print('После параметра -\'p\' необходимо указать номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Затем загружаем какой адрес слушать

    try:
        if '-a' in sys.argv:
            serv_listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            serv_listen_address = ''
        SERVER_LOGGER.info(f'Адрес с которого принимаются подключения: {serv_listen_address}. '
                           f'Если адрес не указан, принимаются соединения с любых адресов.')

    except IndexError:
        print(
            'После параметра \'a\'- необходимо указать адрес, который будет слушать сервер.')
        sys.exit(1)

    # Готовим сокет

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((serv_listen_address, serv_listen_port))

    # Слушаем порт

    server_socket.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = server_socket.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = get_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            # print(message_from_client)  # принты замняем логированием
            # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            # print('Принято некорретное сообщение от клиента.')  # принты замняем логированием
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataReceivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
