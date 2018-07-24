import socketserver
import time
import logging
import datetime
import os
import sys
import threading
from logging import handlers
from celery import Celery
from celery.schedules import crontab

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


# celery
app = Celery('quatek-task', broker=REDIS_URL, result_backend=REDIS_URL)


class UploadAllCardsHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
    '''

    def handle(self):
        logger.info('start an UploadAllCardsHandler to {}'.format(self.client_address))
        self.request.settimeout(5)
        mc_client = {}
        # get mc from database
        try:
            self.request.sendall(b'\rGET DI\n')
            data = self.request.recv(1024).decode()
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'DI' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error')

        # set datetime for mc
        try:
            self.request.sendall('\rSET DATETIME {}\n'.format(
                datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S').encode()))
            data = self.request.recv(1024).decode()
            if 'DATETIME' not in data:
                raise Exception('set datetime error for mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error')

        # delete all cards in mc
        try:
            for i in range(6000):
                self.request.sendall(b'\rCLR CARD ' + str(i).encode() + b'\n')
                data = self.request.recv(1024).decode()

                # if 'CARD' not in data:
                #     raise Exception('clear card error, card number: {}, mc: {}'.format(
                #         str(i), str(self.client_address)))
        except:
            logger.exception('delete all cards error, mc: {} {}'.format(mc_client, self.client_address))

        # add cards to mc
        try:
            for card in cards.find():
                belong_to_mc = card['belong_to_mc']
                # add to all mc
                if belong_to_mc == 'all' or not belong_to_mc:
                    self.request.sendall(
                        '\rSET CARD;{card_counter};{card_number};{job_number};{name};{department};{gender};{cart_category};0;{note}\n'.format(**card).encode())
                    data = self.request.recv(1024).decode()
                    if 'CARD' not in data:
                        raise Exception('upload card error, card: {}, mc: {} {}'.format(
                            card, mc_client, self.client_address))

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
                        data = self.request.recv(1024).decode()
                        if 'CARD' not in data:
                            raise Exception('clear card error, card: {}, mc: {} {}'.format(
                                card, mc_client, self.client_address))
        except:
            logger.exception('error')

        logger.info('stop the UploadAllCardsHandler for {} {}'.format(mc_client, self.client_address))


class UpdateACardHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        param: card
    '''

    def handle(self):
        self.request.settimeout(5)
        logger.info('start an UpdateACardHandler to {}'.format(self.client_address))
        mc_client = {}
        card = self.server.p_data['card']

        # get mc from database
        try:
            self.request.sendall(b'\rGET DI\n')
            data = self.request.recv(1024).decode()
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'DI' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error')

        try:
            belong_to_mc = card['belong_to_mc']
            # add to all mc
            if belong_to_mc == 'all' or not belong_to_mc:
                self.request.sendall(
                    '\rSET CARD;{card_counter};{card_number};{job_number};{name};{department};{gender};{cart_category};0;{note}\n'.format(**card).encode())
                data = self.request.recv(1024).decode()
                if 'CARD' not in data:
                    raise Exception('upload the card to all mc error, card: {}, mc: {} {}'.format(
                        card, mc_client, self.client_address))

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
                    data = self.request.recv(1024).decode()
                    if 'CARD' not in data:
                        raise Exception('upload the card to 1 mc error, card: {}, mc: {} {}'.format(
                            card, mc_client, self.client_address))
                else:
                    self.request.sendall('\rCLR CARD;{}\n'.format(card['card_counter']).encode())
                    data = self.request.recv(1024).decode()
                    if 'CARD' not in data:
                        raise Exception('update with delete a card to mc error, card: {}, mc: {} {}'.format(
                            card, mc_client, self.client_address))
        except:
            logger.exception('error')

        logger.info('stop the UpdateACardHandler for mc {} {}'.format(mc_client, self.client_address))


class DeleteACardHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rCLR CARD;0\n'
        recv: b'\rCARD 0;; ; ; ;0;0; ; \n'
    '''

    def handle(self):
        self.request.settimeout(5)
        logger.info('start an DeleteACardHandler to {}'.format(self.client_address))
        mc_client = {}
        card = self.server.p_data['card']

        # get mc from database
        try:
            self.request.sendall(b'\rGET DI\n')
            data = self.request.recv(1024).decode()
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'DI' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error')

        # delete card from mc
        try:
            self.request.sendall('\rCLR CARD;{}\n'.format(card['card_counter']).encode())
            data = self.request.recv(1024).decode()
            if 'CARD' not in data:
                raise Exception('delete a card from mc error, card: {}, mc: {} {}'.format(
                    card, mc_client, self.client_address))
        except:
            logger.exception('error')


class GetCardTestLogHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rGET LOG\n'
        recv：b'\rLOG 4294967295;0;00CF1974;3;1;16;1900-01-01 00:00:00;1;0;FREE;FREE;FREE;NO\n'
    '''

    def handle(self):
        logger.info('start a new handler for {}'.format(self.client_address))
        self.request.settimeout(5)
        all_data = []
        mc_client = {}

        # get mc from database
        try:
            self.request.sendall(b'\rGET DI\n')
            data = self.request.recv(1024).decode()
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'DI' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error')

        self.request.sendall(b'\rGET LOG\n')

        #  read all logs from mc
        while True:
            try:
                data = self.request.recv(1024).decode()
                all_data.append(data)
                logger.info(data)

                if not data:
                    logger.info('break, no data from {} {}'.format(mc_client, self.client_address))
                    break
            except TimeoutError:
                logger.exception('except break, timeout from {} {}'.format(mc_client, self.client_address))
                break
            except:
                logger.exception('except break, timeout from {} {}'.format(mc_client, self.client_address))
                break

        # process data and save to database
        try:
            all_data = all_data.join()
            all_data = all_data[all_data.find('LOG'):all_data.rfind(
                '\n')].replace('\r', '').replace('LOG ', '').split('\n')
            all_cardtests = []

            for data in all_data:
                temp_dict = {}
                for t, v in zip(['log_id', 'card_counter', 'card_number', 'card_category', 'in_out_symbol', 'mc_id', 'test_datetime', 'test_result', 'is_tested', 'hand', 'left_foot', 'right_foot', 'after_erg'], data.split(';')):
                    temp_dict.update({t: v})

                all_cardtests.append(temp_dict)
            cardtests.insert_many(all_cardtests)
        except:
            logger.exception('error from: {} {}'.format(mc_client, self.client_address))

        # send clr log command to mc
        for cardtest in all_cardtests:
            self.request.sendall('\rCLR LOG {}\n'.format(cardtest['log_id']).encode())

        logger.info('stop the GetCardTestLogHandler for {} {}'.format(mc_client, self.client_address))


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, p_data=None):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.p_data = p_data

    timeout = 5
    allow_reuse_address = True


@app.task()
def update_all_cards():
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), UploadAllCardsHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    logger.info("start an update_all_cards task...")
    time.sleep(60)
    server.shutdown()
    server.server_close()
    logger.info("start the update_all_cards task...")


@app.task()
def update_a_card(card_dict):
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), UpdateACardHandler, p_data={'card': card_dict})
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    logger.info("start an update_a_card task...")
    time.sleep(30)
    server.shutdown()
    server.server_close()
    logger.info("start the update_a_card task...")


@app.task()
def delete_a_card(card_dict):
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), DeleteACardHandler, p_data={'card': card_dict})
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a delete_a_card task...")
    time.sleep(30)
    server.shutdown()
    server.server_close()
    logger.info("start the delete_a_card task...")


@app.task()
def get_logs_from_mc():
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), GetCardTestLogHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a get_logs_from_mc task...")
    time.sleep(60)
    server.shutdown()
    server.server_close()
    logger.info("start the get_logs_from_mc task...")


@app.task()
def test_task(seconds):
    for i in range(seconds):
        logger.info(str(i))
        time.sleep(1)


@app.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60 * 5, get_logs_from_mc.s(), name='get log every 5 mins')
