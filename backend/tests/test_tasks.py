import pytest
import socket
import socketserver
from datetime import datetime, timedelta, timezone
from random import randrange, choice

from app.tasks import ThreadedTCPServer, update_all_cards_to_mc_task, delete_a_card_from_mc_task, get_logs_from_mc_task, update_a_card_to_all_mc_task,


def test_server(command, host='0.0.0.0', port=5858):
    s2_result = None
    try:
        s = socket.socket()
        s.settimeout(5)
        s.bind((host, port))
        s.listen()

        try:
            s2, address = s.accept()
            s2.settimeout(5)
            s2.sendall(f'{command}'.encode())
            s2_result = s2.recv(1000).decode()
        except Exception as e:
            print(e)
        finally:
            s2.close()

    except Exception as e:
        print(e)

    finally:
        s.close()
        return s2_result
