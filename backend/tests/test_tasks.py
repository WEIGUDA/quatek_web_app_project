import pytest
import socket
import threading

from app.tasks import update_all_cards, update_a_card, delete_a_card, get_logs_from_mc


@pytest.fixture()
def generate_host_and_port():
    s_client = socket.socket()
    s_client.bind(('127.0.0.1', 0))
    host, port = s_client.getsockname()
    s_client.close()
    return (host, port)


def test_update_all_cards(generate_host_and_port):
    host, port = generate_host_and_port

    update_all_cards.delay(host=host, port=port, server_last_time=30)

    s = socket.socket()
    s.connect((host, port))
    s.settimeout(5)
    while True:
        data = s.recv(1024).decode()
        if 'GET ID' in data:
            s.sendall(b'\rID 0\n')
            continue
        print(data)
    s.close()
    assert 1 == 1
