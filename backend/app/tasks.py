import socketserver
import time
import json
import logging
import os
import sys
import socket
import threading
from time import sleep
from logging import handlers
from datetime import datetime, timedelta
from redis import Redis
import rq

from pymongo import MongoClient

# load configs
from instance.config_default import MONGODB_SETTINGS, REDIS_URL, SOCKET_HOST, SOCKET_PORT
try:
    from instance.config_pro import MONGODB_SETTINGS, REDIS_URL, SOCKET_HOST, SOCKET_PORT
except:
    pass

# logging
logger = logging.getLogger(os.path.splitext(
    os.path.split((os.path.abspath(__file__)))[1])[0])
logger.setLevel(logging.INFO)
logFormatter = logging.Formatter('%(asctime)s - %(message)s')
fileHandler = handlers.RotatingFileHandler(
    '{}{}'.format(os.path.splitext(os.path.abspath(__file__))[0], '.log'),
    maxBytes=1024 * 1024 * 10,  # 10MB
    backupCount=10,
)
fileHandler.setFormatter(logFormatter)
consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

# pymongo
client = MongoClient(MONGODB_SETTINGS['host'], MONGODB_SETTINGS['port'])
db = client.quatek_web_app
cards = db.card
gates = db.gate
cardtests = db.cardtest
users = db.user

# rq
redis = Redis.from_url(REDIS_URL)
task_queue = rq.Queue('quatek-rq', connection=redis)


class UploadAllCardsHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
    '''

    def handle(self):
        logger.info('upload all cards in {}'.format(self.client_address))
        self.request.settimeout(5)
        mc_client = {}

        # set datetime for mc
        try:
            self.request.sendall('\rSET DATETIME {}\n'.format(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').encode()))
            data = self.recv(1024).decode()
            if 'DATETIME' not in data:
                raise Exception('set datetime error, mc: '.format(self.client_address))
        except:
            logger.exception()

        # get mc
        try:
            self.request.sendall(b'\rGET DI\n')
            data = self.recv(1024).decode()
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'number': mc_client_id})[0]

            if 'DI' not in data:
                raise Exception('get mc error, mc: '.format(self.client_address))
        except:
            logger.exception()

        # delete all cards in mc
        try:
            for i in range(6000):
                self.request.sendall(b'\rCLR CARD ' + str(i).encode() + b'\n')
                data = self.recv(1024).decode()

                # if 'CARD' not in data:
                #     raise Exception('clear card error, card number: {}, mc: {}'.format(
                #         str(i), str(self.client_address)))
        except:
            logger.exception()

        # add cards to mc
        try:
            for card in cards.find():
                belong_to_mc = card['belong_to_mc']
                # add to all mc
                if belong_to_mc == 'all':
                    self.request.sendall(
                        '\rSET CARD;{card_counter};{card_number};{job_number};{name};{department};{gender};{cart_category};0;{note}\n'.format(**card).encode())
                    data = self.recv(1024).decode()
                    if 'CARD' not in data:
                        raise Exception('upload card error, card: {}, mc: {}'.format(card, self.client_address))
                # add to configed mc
                else:
                    belong_to_mc = [{item.split(':')[0]: item.split(':'[1])}
                                    for item in belong_to_mc.split('|')]  # [{'mc1': '0'}, {'mc2': 1}]

                    belong_to_mc_dict = {}  # {'mc1': '0', 'mc2': 1}
                    for item in belong_to_mc:
                        belong_to_mc_dict.update(item)

                    if mc_client['name'] in belong_to_mc_dict:
                        self.request.sendall(
                            '\rSET CARD;{1[card_counter]};{1[card_number]};{1[job_number]};{1[name]};{1[department]};{1[gender]};{1[cart_category]};{0};{1[note]}\n'.format(belong_to_mc_dict[mc_client['name']], **card).encode())
                        data = self.recv(1024).decode()
                        if 'CARD' not in data:
                            raise Exception('clear card error, card: {}, mc: {}'.format(card, self.client_address))
        except:
            logger.exception('upload all cards failed, {}'.format(self.client_address))

        logger.info('stop the handler for {}'.format(self.client_address))


class UpdateACardHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
    '''

    def setup(self):
        logger.info('')
        self.request.settimeout(5)

    def handle(self):
        pass


class DeleteACardHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rCLR CARD;0\n'
        recv: b'\rCARD 0;; ; ; ;0;0; ; \n'
    '''

    def setup(self):
        logger.info('')
        self.request.settimeout(5)

    def handle(self):
        pass


class GetCardTestLogHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rGET LOG\n'
        recv：b'\rLOG 4294967295;0;00CF1974;3;1;16;1900-01-01 00:00:00;1;0;FREE;FREE;FREE;NO\n'
    '''

    def setup(self):
        logger.info('')
        self.request.settimeout(5)

    def handle(self):
        pass


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, p_data=None):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.p_data = p_data

    timeout = 5
    allow_reuse_address = True


class TestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        logger.info('start a new handler for {}'.format(self.client_address))
        self.request.settimeout(5)
        logger.info('test args {}'.format(self.server.p_data))
        while True:
            try:
                data = str(self.request.recv(1024), 'utf-8')
                logger.info(data)

                if not data:
                    logger.info('break, no data from {}'.format(self.client_address))
                    break
            except TimeoutError:
                logger.exception('except break, timeout from {}'.format(self.client_address))
                break
            except:
                logger.exception('except break, timeout from {}'.format(self.client_address))
                break

        logger.info('stop the handler for {}'.format(self.client_address))


def create_cards(times):
    for i in range(times):
        cards.insert_one({'name': str(i), 'card_number': str(i)})


def test_task():
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), TestHandler, p_data={})
    ip, port = server.server_address

    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    logger.info("Server loop running in thread: {}".format(server_thread.name))
    time.sleep(20)
    server.shutdown()
    server.server_close()
    logger.info("Server stopped: {}".format(server_thread.name))


# if __name__ == '__main__':
#     task_queue.enqueue('test_task', )
