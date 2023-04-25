import json
import socket
import sys
import log.server_log_config
import logging
import datetime
import inspect
import select
import argparse


def log(func):
    def wrapper(*args, **kwargs):
        calling_func = inspect.stack()[1][3]
        now = datetime.datetime.now()
        log_string = f'{now} Function {func.__name__} called from function {calling_func}'
        print(log_string)
        with open('log.txt', 'a') as log_file:
            log_file.write(log_string + '\n')
        result = func(*args, **kwargs)
        return result
    return wrapper


SERVER_LOGGER = logging.getLogger('server')


@log
def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


@log
def receive_message(sock):
    data = sock.recv(1024)
    return json.loads(data.decode('utf-8'))


@log
def handle_presence_message(message):
    response = {
        'response': 200,
        'time': message['time'],
        'alert': f"{message['user']['account_name']} is online"
    }
    return response


@log
def handle_client_message(sock, message, message_list):
    action = message.get('action')
    if action == 'presence' and 'time' in message \
            and 'user' in message and message['user']['account_name'] == 'Guest':
        response = handle_presence_message(message)
        send_message(sock, response)
    elif action in message and message['action'] == message and \
            'time' in message and 'any_text' in message:
        message_list.append((message['account_name'], message['any_text']))
        return message_list
    else:
        response = {
            'response': 400,
            'error': f"Unknown action '{action}'"
        }
        send_message(sock, response)


def main():
    if len(sys.argv) < 2:
        print("Usage: server.py -p <port> [-a <addr>]")
        SERVER_LOGGER.info(" Use 'server.py -p <port> [-a <addr>]'")
        return

    port_index = sys.argv.index('-p') + 1
    port = int(sys.argv[port_index])

    address = ''
    if '-a' in sys.argv:
        addr_index = sys.argv.index('-a') + 1
        address = sys.argv[addr_index]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((address, port))
    clients = []
    messages = []
    sock.listen(4)
    SERVER_LOGGER.debug(f"Listening on {address}:{port}")
    print(f"Listening on {address}:{port}")

    while True:
        try:
            client_sock, client_address = sock.accept()
            print(f"Accepted connection from {client_address}")

            message = receive_message(client_sock)
            handle_client_message(client_sock, message, message_list=messages)
            SERVER_LOGGER.info(f"Accepted connection from {client_address}")
            client_sock.close()
        except json.JSONDecodeError:
            SERVER_LOGGER.error(
                f"Couldn't decode json string from {client_address}")
        else:
            SERVER_LOGGER.info(f'Connection accepted with {client_address}')
            clients.append(client_sock)

        recv_data_list = []
        send_data_list = []
        err_list = []
        try:
            if clients:
                recv_data_list, send_data_list, err_list = select.select(
                    clients, clients, [], 0)
        except OSError:
            SERVER_LOGGER.error('OSError')

        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    handle_client_message(receive_message(client_with_message),
                                          messages, client_with_message)
                except:
                    SERVER_LOGGER.info(f'Client {client_with_message.getpeername()} '
                                       f'Disconnrcted')
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = {
                'action': 'message',
                'sender': messages[0][0],
                'time': datetime(),
                'any_text': messages[0][1]
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    SERVER_LOGGER.info(
                        f'Client {waiting_client.getpeername()} disconnected.')
                    clients.remove(waiting_client)
        client_sock.close()


if __name__ == '__main__':
    main()


# python server.py -p 7777 -a 0.0.0.0
