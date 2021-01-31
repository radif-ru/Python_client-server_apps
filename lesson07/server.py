"""Программа-сервер"""

import argparse
from select import select
from time import time
from socket import socket, AF_INET, SOCK_STREAM
import sys
import json

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER
from common.utils import get_message, send_message
from decos import Log, log

from logs.configs.config_server_log import LOGGER as SERVER_LOGGER  # Инициализация логирования сервера.
from errors import IncorrectDataReceivedError


@log
def process_client_message(client_socket, messages_list, client):
    """
    Обработчик сообщений от клиентов, принимает словарь -
    сообщение от клинта, проверяет корректность,
    возвращает словарь-ответ для клиента с результатом приёма.

    :param client_socket:
    :param messages_list:
    :param client:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {client_socket}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in client_socket and client_socket[ACTION] == PRESENCE and TIME in client_socket \
            and USER in client_socket and client_socket[USER][ACCOUNT_NAME] == 'Guest':
        send_message(client, {RESPONSE: 200})
        return
    # Если это сообщение, то добавляем его в очередь сообщений. Ответ не требуется.
    elif ACTION in client_socket and client_socket[ACTION] == MESSAGE and \
            TIME in client_socket and MESSAGE_TEXT in client_socket:
        messages_list.append((client_socket[ACCOUNT_NAME], client_socket[MESSAGE_TEXT]))
        return
    # Иначе отдаём Bad request
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def create_arg_parser():
    """Парсер аргументов коммандной строки"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    # parser.parse_args(sys.argv[1:]) 0 это имя файла, по этому берём все, которые после:
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p

    # проверка получения корретного номера порта для работы сервера.
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(
            f'Попытка запуска сервера с указанием неподходящего порта '
            f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)

    return listen_address, listen_port


def main():
    """Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию"""
    # server.py -p 8079 -a 192.168.1.2
    serv_listen_address, serv_listen_port = create_arg_parser()

    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {serv_listen_port}, адрес,'
                       f' с которого принимаются подключения: {serv_listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((serv_listen_address, serv_listen_port))
    server_socket.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients_list = []
    messages_list = []

    # Слушаем порт
    server_socket.listen(MAX_CONNECTIONS)

    # Основной цикл программы сервера
    while True:
        # Ждём подключения, если таймаут вышел, ловим исключение.
        try:
            client_socket, client_address = server_socket.accept()
        except OSError:
            pass
        else:
            SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
            clients_list.append(client_socket)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []
        # Проверяем на наличие ждущих клиентов
        try:
            if clients_list:
                recv_data_lst, send_data_lst, err_lst = select(clients_list, clients_list, [], 0)
        except OSError:
            pass

        # принимаем сообщения и если там есть сообщения,
        # кладём в словарь, если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages_list, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                f'отключился от сервера.')
                    clients_list.remove(client_with_message)

        # Если есть сообщения для отправки и ожидающие клиенты, отправляем им сообщение.
        if messages_list and send_data_lst:
            message = {
                ACTION: MESSAGE,
                SENDER: messages_list[0][0],
                TIME: time(),
                MESSAGE_TEXT: messages_list[0][1]
            }
            del messages_list[0]
            for waiting_client in send_data_lst:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    clients_list.remove(waiting_client)


if __name__ == '__main__':
    main()
