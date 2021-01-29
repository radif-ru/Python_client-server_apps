"""Программа-клиент"""

import argparse
import sys
import json
from socket import socket, AF_INET, SOCK_STREAM
import time
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, ERROR, DEFAULT_IP_ADDRESS, DEFAULT_PORT
from common.utils import get_message, send_message
from decos import log
from errors import ReqFieldMissingError

from logs.configs.config_client_log import LOGGER as CLIENT_LOGGER  # Инициализация клиентского логера


@log
def create_new_presence(account_name='Guest'):
    """
    Функция генерирует запрос о присутствии клиента
    :param account_name: Guest - имя аккаунта по умолчанию
    :return: out:  возвращает сгенерированный словарь словарь
    """
    # {'action': 'presence', 'time': 1573760672.167031, 'user': {'account_name': 'Guest'}}
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(f'Сформировано {PRESENCE} сообщение для пользователя {account_name}')
    return out


@log
def process_answer(message):
    """
    Функция разбирает ответ сервера
    :param message: проверяется код ответа от сервера
    :return:
    """
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        return f'400 : {message[ERROR]}'
    raise ReqFieldMissingError(RESPONSE)


@log
def create_arg_parser():
    """Создаём парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    """Загружаем параметы коммандной строки"""
    # client.py 192.168.1.2 8079
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port

    # проверим подходящий номер порта
    if not 1023 < server_port < 65536:
        CLIENT_LOGGER.critical(
            f'Попытка запуска клиента с неподходящим номером порта: {server_port}. '
            f'Допустимы адреса с 1024 до 65535. Клиент завершается.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: адрес сервера: '
                       f'{server_addr}, порт: {server_port}')

    # Инициализация сокета и обмен

    try:
        client_socket = socket(AF_INET, SOCK_STREAM)
        client_socket.connect((server_addr, server_port))
        message_to_server = create_new_presence()
        send_message(client_socket, message_to_server)
        answer = process_answer(get_message(client_socket))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле {missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(f'Не удалось подключиться к серверу {server_addr}:{server_port}, '
                               f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
