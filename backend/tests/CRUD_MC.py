from tests.CRUD_DB import get_gate_from_db
from tests.CRUD_DB import db

import socket

host = ''
port = 5858


def get_card(id):
    s = socket.socket()
    s.bind((host, port))

    s.listen()

    connection, address = s.accept()

    r = 'GET CARD;{}\r\n'.format(id)
    r = r.encode()
    connection.sendall(r)
    connection.settimeout(5)

    re = connection.recv(1024)

    print(re)

    connection.close()
    s.close()


def get_id():
    s = socket.socket()
    s.bind((host, port))

    s.listen(5)
    connection, address = s.accept()
    r = b'GET MCID\r\n'
    connection.sendall(r)

    connection.settimeout(5)
    re = connection.recv(1024)

    connection.close()
    s.close()

    return re.decode()


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
    # data = get_id()
    # mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
    # gates = db.gate
    # mc_client = gates.find({'mc_id': mc_client_id})[0]
    # print(mc_client)
    get_card(0)
    # get_client()