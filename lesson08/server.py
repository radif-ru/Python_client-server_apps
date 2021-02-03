"""Программа-сервер"""

import argparse
from select import select
from time import time
from socket import socket, AF_INET, SOCK_STREAM
import sys
import json

from common.variables import ACTION, ACCOUNT_NAME, RESPONSE, MAX_CONNECTIONS, \
    PRESENCE, TIME, USER, ERROR, DEFAULT_PORT, MESSAGE, MESSAGE_TEXT, SENDER, RESPONSE_200, RESPONSE_400, EXIT, \
    DESTINATION
from common.utils import get_message, send_message
from decos import Log, log

from logs.configs.config_server_log import LOGGER as SERVER_LOGGER  # Инициализация логирования сервера.
from errors import IncorrectDataReceivedError


@log
def process_client_message(client_socket, messages_list, client, clients_list, names):
    """
    Обработчик сообщений от клиентов, принимает словарь - сообщение от клиента,
    проверяет корректность, отправляет словарь-ответ в случае необходимости.
    :param client_socket:
    :param messages_list:
    :param client:
    :param clients_list:
    :param names:
    :return:
    """
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {client_socket}')
    # Если это сообщение о присутствии, принимаем и отвечаем, если успех
    if ACTION in client_socket and client_socket[ACTION] == PRESENCE and TIME in client_socket \
            and USER in client_socket:
        # Если такой пользователь ещё не зарегистрирован,
        # регистрируем, иначе отправляем ответ и завершаем соединение.
        if client_socket[USER][ACCOUNT_NAME] not in names.keys():
            names[client_socket[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже занято.'
            send_message(client, response)
            clients_list.remove(client)
            client.close()
        return
        # Если это сообщение, то добавляем его в очередь сообщений.
        # Ответ не требуется.
    elif ACTION in client_socket and client_socket[ACTION] == MESSAGE and \
            DESTINATION in client_socket and TIME in client_socket \
            and SENDER in client_socket and MESSAGE_TEXT in client_socket:
        messages_list.append(client_socket)
        return
        # Если клиент выходит
    elif ACTION in client_socket and client_socket[ACTION] == EXIT and ACCOUNT_NAME in client_socket:
        clients_list.remove(names[client_socket[ACCOUNT_NAME]])
        names[client_socket[ACCOUNT_NAME]].close()
        del names[client_socket[ACCOUNT_NAME]]
        return
        # Иначе отдаём Bad request
    else:
        response = RESPONSE_400
        response[ERROR] = 'Запрос некорректен.'
        send_message(client, response)
        return


@log
def process_message(message, names, listen_socks):
    """
    Функция адресной отправки сообщения определённому клиенту. Принимает словарь сообщение,
    список зарегистрированых пользователей и слушающие сокеты. Ничего не возвращает.
    :param message:
    :param names:
    :param listen_socks:
    :return:
    """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        SERVER_LOGGER.info(f'Отправлено сообщение пользователю {message[DESTINATION]} '
                           f'от пользователя {message[SENDER]}.')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        SERVER_LOGGER.error(
            f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере, '
            f'отправка сообщения невозможна.')


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
    """
    Загрузка параметров командной строки, если нет параметров, то задаём значения по умоланию
    :return:
    """
    # server.py -p 8079 -a 192.168.1.2
    serv_listen_address, serv_listen_port = create_arg_parser()

    SERVER_LOGGER.info(
        f'Запущен сервер, порт для подключений: {serv_listen_port}, '
        f'адрес с которого принимаются подключения: {serv_listen_address}. '
        f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Готовим сокет
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind((serv_listen_address, serv_listen_port))
    server_socket.settimeout(0.5)

    # список клиентов , очередь сообщений
    clients_list = []
    messages_list = []

    # Словарь, содержащий имена пользователей и соответствующие им сокеты.
    names = dict()

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

        # принимаем сообщения и если ошибка, исключаем клиента.
        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:
                    process_client_message(get_message(client_with_message),
                                           messages_list, client_with_message, clients_list, names)
                except Exception:
                    SERVER_LOGGER.info(f'Клиент {client_with_message.getpeername()} '
                                       f'отключился от сервера.')
                    clients_list.remove(client_with_message)

                # Если есть сообщения, обрабатываем каждое.
                for i in messages_list:
                    try:
                        process_message(i, names, send_data_lst)
                    except Exception:
                        SERVER_LOGGER.info(f'Связь с клиентом с именем {i[DESTINATION]} была потеряна')
                        clients_list.remove(names[i[DESTINATION]])
                        del names[i[DESTINATION]]
                messages_list.clear()


if __name__ == '__main__':
    main()
