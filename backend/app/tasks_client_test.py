import socket
import time
import datetime


while True:
    try:
        print('{} start a socket client...'.format(datetime.datetime.today()))
        sock = socket.socket()
        sock.settimeout(3)
        host = ('127.0.0.1', 5858)
        sock.connect(host)
        for i in range(30):
            sock.sendall(bytes('{} hello there, from {}'.format(str(i), str(host)), 'utf-8'))
            time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        print('{} try after 3 seconds...'.format(datetime.datetime.today()))
        time.sleep(0.5)
