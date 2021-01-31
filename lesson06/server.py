"""Программа-сервер"""

import argparse
from socket import socket, AF_INET, SOCK_STREAM
import sys
import json

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT
from common.utils import get_message, send_message
from decos import Log, log

from logs.configs.config_server_log import LOGGER as SERVER_LOGGER  # Инициализация логирования сервера.
from errors import IncorrectDataReceivedError


@log
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


@log
def create_arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


def main():
    """Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию"""
    # server.py -p 8079 -a 192.168.1.2
    parser = create_arg_parser()
    # parser.parse_args(sys.argv[1:]) 0 это имя файла, по этому берём все, которые после:
    namespace = parser.parse_args(sys.argv[1:])
    serv_listen_address = namespace.a
    serv_listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < serv_listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта {serv_listen_port}. '
                               f'Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {serv_listen_port}, адрес,'
                       f' с которого принимаются подключения: {serv_listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

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
            print(message_from_client)
            response = process_client_message(message_from_client)
            SERVER_LOGGER.info(f'Сформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(f'Соединение с клиентом {client_address} закрывается.')
            client.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(f'Не удалось декодировать JSON строку, полученную от '
                                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataReceivedError:
            SERVER_LOGGER.error(f'От клиента {client_address} приняты некорректные данные. '
                                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()
