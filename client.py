import json
import socket
import sys


def send_message(sock, message):
    encoded_message = json.dumps(message).encode('utf-8')
    sock.send(encoded_message)


def receive_message(sock):
    data = sock.recv(1024)
    return json.loads(data.decode('utf-8'))


def create_presence_message(account_name):
    message = {
        'action': 'presence',
        'time': 12345,
        'user': {
            'account_name': account_name,
            'status': 'online'
        }
    }
    return message


def parse_server_response(response):
    if 'response' in response:
        return response['response']
    else:
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: client.py <addr> [<port>]")
        return

    address = sys.argv[1]
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 7777

    sock = socket.socket()
    sock.connect((address, port))

    account_name = 'Guest'
    message = create_presence_message(account_name)
    send_message(sock, message)

    response = receive_message(sock)
    result = parse_server_response(response)
    if result:
        print(f"Server response: {result}")
    else:
        print("Invalid server response")

    sock.close()


if __name__ == '__main__':
    main()

# python client.py 127.0.0.1 7777
