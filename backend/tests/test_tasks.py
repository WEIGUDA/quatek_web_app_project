import socketserver
import threading
import time
from datetime import datetime


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, p_data=None):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.p_data = p_data

    timeout = 5
    allow_reuse_address = True


class TestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        self.request.sendall(b'GET MCID\r\n')

        data = self.request.recv(1024).decode().replace('\r\n', '')
        print('{} - {} from {} {}'.format(datetime.now(), data, *self.client_address))
        time.sleep(10)


def test_task():
    print('{} - {}'.format(datetime.now(), 'start a server'))
    server = ThreadedTCPServer(('0.0.0.0', 5858), TestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(10)
    server.shutdown()
    server.server_close()


if __name__ == '__main__':
    test_task()
