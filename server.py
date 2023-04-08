import json
import socket
import sys


def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


def receive_message(sock):
    data = sock.recv(1024)
    return json.loads(data.decode('utf-8'))


def handle_presence_message(message):
    response = {
        'response': 200,
        'time': message['time'],
        'alert': f"{message['user']['account_name']} is online"
    }
    return response


def handle_client_message(sock, message):
    action = message.get('action')
    if action == 'presence':
        response = handle_presence_message(message)
        send_message(sock, response)
    else:
        response = {
            'response': 400,
            'error': f"Unknown action '{action}'"
        }
        send_message(sock, response)


def main():
    if len(sys.argv) < 2:
        print("Usage: server.py -p <port> [-a <addr>]")
        return

    port_index = sys.argv.index('-p') + 1
    port = int(sys.argv[port_index])

    address = ''
    if '-a' in sys.argv:
        addr_index = sys.argv.index('-a') + 1
        address = sys.argv[addr_index]

    sock = socket.socket()
    sock.bind((address, port))
    sock.listen(1)
    print(f"Listening on {address}:{port}")

    while True:
        client_sock, client_address = sock.accept()
        print(f"Accepted connection from {client_address}")

        message = receive_message(client_sock)
        handle_client_message(client_sock, message)

        client_sock.close()


if __name__ == '__main__':
    main()


# python server.py -p 7777 -a 0.0.0.0
