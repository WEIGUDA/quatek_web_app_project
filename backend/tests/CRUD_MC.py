from tests.CRUD_DB import get_gate_from_db

import socket

host = ''
port = 5858


def get_card(id):
    s = socket.socket()
    s.bind((host, port))

    s.listen()

    connection, address = s.accept()

    r = 'GET CARD;{}\n'.format(id)
    r = r.encode()
    connection.sendall(r)

    re = connection.recv(1024)

    print(re)

    connection.close()


def get_id():
    s = socket.socket()
    s.bind((host, port))

    s.listen(5)
    connection, address = s.accept()
    r = b'GET MCID\r\n'
    connection.sendall(r)

    connection.settimeout(5)
    re = connection.recv(1024)
    print(re)

    connection.close()
    s.close()


def get_log():
    s = socket.socket()
    s.bind((host, port))

    s.listen()

    connection, address = s.accept()

    r = b'GET LOG\n'
    connection.sendall(r)

    re = connection.recv(1024)

    print(re)

    connection.close()


def get_client():
    s = socket.socket()
    s.bind((host, port))

    s.listen()

    connection, address = s.accept()

    # s.settimeout(5)

    r = b'\rGET ID\n'
    connection.sendall(r)

    re = connection.recv(1024)

    re = re.decode()

    print('re', re)

    # client_id = re.replace('\r', '').replace('\n', '').split(' ')[1]
    #
    # print('client_id', client_id)
    #
    # my_client = get_gate_from_db(client_id)
    #
    # print('my_client', my_client)

    connection.close()


if __name__ == "__main__":
    get_id()
    # get_card(2)
    # get_client()