import datetime
import logging
import os
import re
import socketserver
import sys
import threading
import time
import smtplib
import io
from email.message import EmailMessage
from email.utils import formataddr
from email.utils import formatdate
from email.utils import COMMASPACE

from email.header import Header
from email import encoders

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from logging import handlers

from celery import Celery
from pymongo import MongoClient, UpdateOne, bulk
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import pyexcel
from app.mod_gate.schema import Log, Base
from app.mod_gate.utils import card_log_calculate

# load configs
from instance.config_default import MONGODB_DB, MONGODB_HOST, MONGODB_PORT, SOCKET_HOST, SOCKET_PORT, REDIS_URL

try:
    from instance.config_dev import MONGODB_DB, MONGODB_HOST, MONGODB_PORT, SOCKET_HOST, SOCKET_PORT, REDIS_URL
except:
    pass

try:
    from instance.config_pro import MONGODB_DB, MONGODB_HOST, MONGODB_PORT, SOCKET_HOST, SOCKET_PORT, REDIS_URL
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
# logger.addHandler(consoleHandler)


# celery
app = Celery('quatek-task', broker=REDIS_URL, result_backend=REDIS_URL)
app.conf.update({
    'CELERY_MONGODB_SCHEDULER_DB': MONGODB_DB,
    'CELERY_MONGODB_SCHEDULER_COLLECTION': "schedules",
    'CELERY_MONGODB_SCHEDULER_URL': f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}",
    'enable_utc': False,
})


class UploadAllCardsHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
    '''

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        cards = db.card
        gates = db.gate

        self.request.settimeout(5)
        mc_client = {}

        # get mc from database
        try:
            self.request.sendall(b'GET MCID\r\n')
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]
            gates.update_one({'mc_id': 'mc_client.mc_id'},
                             {'$set': {'ip': self.client_address[0], 'port': self.client_address[1]}})

            if 'MCID' not in data:
                raise Exception('get mc error')
        except:
            logger.exception(f'error in UploadAllCardsHandler')

        logger.info(f'start UploadAllCardsHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall('SET DATE {}\r\n'.format(
                dt.strftime('%Y-%m-%d')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'DATE' not in data:
                raise Exception('set date error')

            self.request.sendall('SET TIME {}\r\n'.format(dt.strftime('%H:%M:%S')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'TIME' not in data:
                raise Exception('set time error')

        except:
            logger.exception(
                f'error in UploadAllCardsHandler <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        # add cards to mc
        try:
            commands = []
            for card in cards.find():
                belong_to_mc = card['belong_to_mc']
                # add to all mc
                if belong_to_mc == 'all' or not belong_to_mc:
                    # command = 'SET CARD {card_counter},{card_number},{job_number},{name},{department},{gender},{card_category},0,{note}\r\n'.format(
                    #     **card).encode()
                    for key in card.keys():
                        if not card[key]:
                            card[key] = 'default'
                    commands.append(
                        f'SET CARD {card["card_counter"]},{card["card_number"]},{card["job_number"]},{card["name"]},{card["department"]},{card["gender"]},{card["card_category"]},0,{card["note"]}\r\n')

                # add to configed mc
                else:
                    # [{'mc1': '0'}, {'mc2': 1}]
                    belong_to_mc = [{item.split(':')[0]: item.split(':')[1]} for item in belong_to_mc.split('|')]

                    belong_to_mc_dict = {}  # {'mc1': '0', 'mc2': 1}

                    for item in belong_to_mc:
                        belong_to_mc_dict.update(item)

                    if mc_client['name'] in belong_to_mc_dict:

                        for key in card.keys():
                            if not card[key]:
                                card[key] = 'default'

                        commands.append(
                            f'SET CARD {card["card_counter"]},{card["card_number"]},{card["job_number"]},{card["name"]},{card["department"]},{card["gender"]},{card["card_category"]},{belong_to_mc_dict[mc_client["name"]]},{card["note"]}\r\n')

            for command in commands:
                logger.info(command)
                self.request.sendall(command.encode())
                logger.info(self.request.recv(1000).decode())

            # commands = ''.join(commands).encode()
            # self.request.sendall(commands)
            # logger.info(f'send commands to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {commands}')
            # logger.info(
            #     f'recv from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {self.request.recv(100000)}')
        except:
            logger.exception(
                f'error in UploadAllCardsHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        time.sleep(self.server.p_data['server_last_time'])
        logger.info(f'stop UploadAllCardsHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')


class UpdateACardHandler(socketserver.BaseRequestHandler):
    ''' send: b'\rSET CARD;0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        recv: b'\rCARD 0;00CF1974;5454;Gorden;RD Team;1;3;0000;Remark\n'
        param: card
    '''

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        gates = db.gate
        self.request.settimeout(5)

        mc_client = {}
        card = self.server.p_data['card']

        # get mc from database
        try:
            self.request.sendall(b'GET MCID\r\n')
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'MCID' not in data:
                raise Exception('get mc error, from {}'.format(self.client_address))
        except:
            logger.exception('error in UpdateACardHandler')

        logger.info(f'start UpdateACardHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall('SET DATE {}\r\n'.format(
                dt.strftime('%Y-%m-%d')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'DATE' not in data:
                raise Exception('set date error for  {}'.format(self.client_address))

            self.request.sendall('SET TIME {}\r\n'.format(dt.strftime('%H:%M:%S')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'TIME' not in data:
                raise Exception('set time error for {}'.format(self.client_address))

        except:
            logger.exception('error in UpdateACardHandler')

        try:
            belong_to_mc = card['belong_to_mc']

            # add to all mc
            if belong_to_mc == 'all' or not belong_to_mc:
                command = 'SET CARD {card_counter},{card_number},{job_number},{name},{department},{gender},{card_category},0,{note}\r\n'.format(
                    **card).encode()
                logger.info(command.decode())
                self.request.sendall(command)

                data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
                if 'CARD' not in data:
                    raise Exception('upload the card to all mc error, card: {} from{}'.format(
                        card, self.client_address))

            # add to configed mc
            else:
                # [{'mc1': '0'}, {'mc2': 1}]
                belong_to_mc = [{item.split(':')[0]: item.split(':')[1]} for item in belong_to_mc.split('|')]

                belong_to_mc_dict = {}  # {'mc1': '0', 'mc2': 1}
                for item in belong_to_mc:
                    belong_to_mc_dict.update(item)

                if mc_client['name'] in belong_to_mc_dict:
                    self.request.sendall(
                        'SET CARD {card_counter},{card_number},{job_number},{name},{department},{gender},{card_category},{0},{note}\r\n'.format(
                            belong_to_mc_dict[mc_client['name']], **card).encode())
                    data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
                    if 'CARD' not in data:
                        raise Exception('upload the card to 1 mc error, card: {}, from {}'.format(
                            card, self.client_address))
                else:
                    self.request.sendall('CLR CARD {}\r\n'.format(card['card_counter']).encode())
                    data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
                    if 'CARD' not in data:
                        raise Exception('update with delete a card to mc error, card: {}, from {}'.format(
                            card, self.client_address))
        except:
            logger.exception('error in UpdateACardHandler')

        time.sleep(self.server.p_data['server_last_time'])
        logger.info('stop the UpdateACardHandler for mc {} {}'.format(mc_client, self.client_address))


class DeleteACardHandler(socketserver.BaseRequestHandler):
    ''' send: b'CLR CARD;0\r\n'
        recv: b'CARD 0;; ; ; ;0;0; ; \r\n'
    '''

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        gates = db.gate
        mc_client = {}

        self.request.settimeout(5)
        logger.info('start an DeleteACardHandler for {}'.format(self.client_address))
        card = self.server.p_data['card']

        # get mc from database
        try:
            self.request.sendall(b'GET MCID\r\n')
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'MCID' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error in GetCardTestLogHandler')

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall('SET DATE {}\r\n'.format(
                dt.strftime('%Y-%m-%d')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'DATE' not in data:
                raise Exception('set date error for  {}'.format(self.client_address))

            self.request.sendall('SET TIME {}\r\n'.format(dt.strftime('%H:%M:%S')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'TIME' not in data:
                raise Exception('set time error for {}'.format(self.client_address))

        except:
            logger.exception('error in DeleteACardHandler')

        # delete card from mc
        try:
            self.request.sendall('CLR CARD {}\r\n'.format(card['card_counter']).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'CARD' not in data:
                raise Exception('delete a card from mc error, card: {}, from {}'.format(
                    card, self.client_address))
        except:
            logger.exception('error in DeleteACardHandler')

        time.sleep(self.server.p_data['server_last_time'])
        logger.info('stop DeleteACardHandler for {}'.format(self.client_address))


class GetCardTestLogHandler(socketserver.BaseRequestHandler):
    ''' send: b'GET LOG\r\n'
        recv：b'LOG 1536388814,1,00BC5C01,1,1,0,0,0,NO,NO,NO,NO,NO\r\n'
    '''

    def handle(self):
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        gates = db.gate
        cardtests = db.card_test

        self.request.settimeout(5)
        all_data = []
        mc_client = {}
        all_cardtests = []

        # get mc from database
        try:
            self.request.sendall(b'GET MCID\r\n')
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]

            if 'MCID' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error in GetCardTestLogHandler')

        logger.info(f'start GetCardTestLogHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        # set datetime for mc
        try:
            dt = datetime.datetime.utcnow()
            self.request.sendall('SET DATE {}\r\n'.format(
                dt.strftime('%Y-%m-%d')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'DATE' not in data:
                raise Exception('set date error for {}'.format(self.client_address))

            self.request.sendall('SET TIME {}\r\n'.format(dt.strftime('%H:%M:%S')).encode())
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            if 'TIME' not in data:
                raise Exception('set time error for {}'.format(self.client_address))

        except:
            logger.exception('error in GetCardTestLogHandler')

        #  read all logs from mc

        while True:
            try:
                self.request.sendall(b'GET LOG\r\n')
                data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())

                if '0,0,00000000,0,0,0,0,0,,,,,' in data:
                    logger.info(f'break, no logs in <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')
                    break

                if not data:
                    logger.info(f'break, no data from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')
                    break

                all_data.append(data)
                self.request.sendall('CLR LOG {}\r\n'.format(data.split(
                    ',')[0].replace('LOG ', '')).encode())
                self.request.recv(1024)

            except TimeoutError:
                logger.exception('except break, timeout from {} {}'.format(mc_client, self.client_address))
                break
            except:
                logger.exception('except break, timeout from {} {}'.format(mc_client, self.client_address))
                break

        # process data and save to database
        if all_data:
            try:
                all_data = ''.join(all_data)
                all_data = re.sub(r'CSN.*\r\n|\r|LOG ', '', all_data).split('\n')

                if not all_data[-1]:
                    all_data.pop()
                logger.info(f'format: LOG 流水号;卡片编号;卡片号码;卡片类型;进出标志;进出机号;是否通过;是否测试;RSG;手腕带检测;左脚检测;右脚检测;ERG')
                logger.info(f'raw data: {all_data}')
                for data in all_data:
                    data = data.split(',')

                    temp_dict = {
                        'log_id': data[0],
                        'card_counter': data[1],
                        'card_number': data[2],
                        'card_category': data[3],
                        'in_out_symbol': data[4],
                        'mc_id': data[5],
                        'test_result': data[6],
                        'is_tested': data[7],
                        'RSG': data[8],
                        'hand': data[9],
                        'left_foot': data[10],
                        'right_foot': data[11],
                        'after_erg': data[12],
                    }

                    all_cardtests.append(temp_dict)

                for cardtest in all_cardtests:
                    cardtest['test_datetime'] = datetime.datetime.fromtimestamp(
                        int(cardtest['log_id']), tz=datetime.timezone.utc)
                    cardtest['is_copied_to_other_database'] = False

                cardtests.insert_many(all_cardtests)
            except:
                logger.exception('error from: {} {}'.format(mc_client, self.client_address))

        time.sleep(self.server.p_data['server_last_time'])
        logger.info(
            f'stop the GetCardTestLogHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')


class DeleteAllCardsFromMcHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.settimeout(5)
        mc_client = {}

        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        cards = db.card
        gates = db.gate

        # get mc from database
        try:
            self.request.sendall(b'GET MCID\r\n')
            data = re.sub(r'CSN.*\r\n|\r|LOG ', '', self.request.recv(1024).decode())
            mc_client_id = data.replace('\r', '').replace('\n', '').split(' ')[1]
            mc_client = gates.find({'mc_id': mc_client_id})[0]
            gates.update_one({'mc_id': 'mc_client.mc_id'},
                             {'$set': {'ip': self.client_address[0], 'port': self.client_address[1]}})

            if 'MCID' not in data:
                raise Exception('get mc error, mc: {} {}'.format(mc_client, self.client_address))
        except:
            logger.exception('error in DeleteAllCardsFromMcHandler')

        logger.info(
            f'start DeleteAllCardsFromMcHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        # delete all cards from mc
        commands = []
        try:
            for i in range(6000):
                # command = f'CLR CARD {i}\r\n'.encode()
                commands.append(f'CLR CARD {i}\r\n')
                # self.request.sendall(command)
                # logger.info(f'send command {command} to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

            for card in cards.find():
                # command = f'CLR CARD {card["card_counter"]}\r\n'.encode()
                commands.append(f'CLR CARD {card["card_counter"]}\r\n')
                # self.request.sendall(command)
                # logger.info(f'send command {command} to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

            self.request.sendall(''.join(commands).encode())
            logger.info(f'send commands to <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {commands}')

            logger.info(
                f'receive from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>: {self.request.recv(100000)}')

        except:
            logger.exception(
                f'DeleteAllCardsFromMcHandler error from <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')

        time.sleep(self.server.p_data['server_last_time'])
        logger.info(
            f'stop DeleteAllCardsFromMcHandler for <MC(name={mc_client["name"]}, mc_id={mc_client["mc_id"]})>')


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, p_data=None):
        super().__init__(server_address, RequestHandlerClass, bind_and_activate=True)
        self.p_data = p_data

    timeout = 30
    allow_reuse_address = True


@app.task()
def update_all_cards_to_mc_task(host=SOCKET_HOST, port=SOCKET_PORT, server_last_time=3):
    server = ThreadedTCPServer((host, port), UploadAllCardsHandler, p_data={'server_last_time': server_last_time})
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start an update_all_cards task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the update_all_cards task")


@app.task()
def update_a_card_to_all_mc_task(card_dict, server_last_time=3):
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), UpdateACardHandler,
                               p_data={'card': card_dict, 'server_last_time': server_last_time})
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start an update_a_card task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the update_a_card task")


@app.task()
def delete_a_card_from_mc_task(card_dict, server_last_time=3):
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), DeleteACardHandler,
                               p_data={'card': card_dict, 'server_last_time': server_last_time})
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a delete_a_card task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the delete_a_card task")


@app.task()
def get_logs_from_mc_task(server_last_time=3):
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), GetCardTestLogHandler,
                               p_data={'server_last_time': server_last_time})
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a get_logs_from_mc task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the get_logs_from_mc task")


@app.task()
def delete_all_cards_task(server_last_time=3):
    server = ThreadedTCPServer((SOCKET_HOST, SOCKET_PORT), DeleteAllCardsFromMcHandler,
                               p_data={'server_last_time': server_last_time})
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    logger.info("start a delete_all_cards_task")
    time.sleep(server_last_time)
    server.shutdown()
    server.server_close()
    logger.info("stop the delete_all_cards_task")


@app.task()
def send_email_of_logs(card_class_time=''):
    # pymongo
    client = MongoClient(MONGODB_HOST, MONGODB_PORT)
    db = client[MONGODB_DB]
    system_config = db.system_config
    card_class_time_collection = db.card_class_time

    logger.info('start send_email_of_logs task')
    config = system_config.find()[0]
    logger.info(f'config: {config}')

    card_class = {}
    if card_class_time:
        card_class = card_class_time_collection.find_one({'name': card_class_time})

    else:
        card_class = {'name': 'all',
                      'working_time_from': config['work_hours'].split('-')[0],
                      'working_time_to': config['work_hours'].split('-')[1]}

    # process data
    wb = card_log_calculate(MONGODB_HOST, MONGODB_PORT, MONGODB_DB,
                            hours_start=card_class['working_time_from'],
                            hours_end=card_class['working_time_to'],
                            card_class_time=card_class_time)

    # sending email
    file_name_utf = f"report_generated_at_{datetime.datetime.now()}_for_{card_class['name']}_{card_class['working_time_from']}_{card_class['working_time_to']}"
    file_name = f"report_generated_at_{datetime.datetime.now()}"
    msg = EmailMessage()
    msg['Subject'] = file_name
    msg['From'] = config['smtp_username']
    msg['To'] = ', '.join(config['emails'].split(','))
    msg.add_alternative(file_name_utf + '\n')
    # msg.preamble = file_name
    excel_data = io.BytesIO()
    pyexcel.get_book(bookdict=wb).save_to_memory('xlsx', stream=excel_data)
    excel_data.seek(0)

    msg.add_attachment(excel_data.read(), maintype='application', subtype='vnd.ms-excel',
                       filename=f'{file_name_utf}.xlsx',)

    if config['smtp_use_ssl']:
        with smtplib.SMTP_SSL(config['smtp_host'], config['smtp_port']) as s:
            if config['smtp_use_tls']:
                s.starttls()
            if config['smtp_need_auth']:
                s.login(config['smtp_username'], config['smtp_password'])
            s.send_message(msg)
    else:
        with smtplib.SMTP(config['smtp_host'], config['smtp_port']) as s:
            if config['smtp_use_tls']:
                s.starttls()
            if config['smtp_need_auth']:
                s.login(config['smtp_username'], config['smtp_password'])
            s.send_message(msg)

    logger.info('stop send_email_of_logs task')


@app.task()
def save_to_other_database():
    logger.info('start save_to_other_database task')

    try:
        # pymongo
        client = MongoClient(MONGODB_HOST, MONGODB_PORT)
        db = client[MONGODB_DB]
        cards = db.card
        cardtests = db.card_test
        system_config = db.system_config
        config = system_config.find()[0]

        os.environ["NLS_LANG"] = 'AMERICAN_AMERICA.UTF8'
        # sqlalchemy
        engine = create_engine(
            URL(
                drivername=config['db_type'],
                host=config['db_host'],
                port=config['db_port'],
                database=config['db_name'],
                username=config['db_username'],
                password=config['db_password']
            ),
        )

        inspector = inspect(engine)

        if 'logs' not in inspector.get_table_names():
            logger.info('create logs table')
            Base.metadata.create_all(bind=engine)

        Session = sessionmaker(bind=engine)
        session = Session()

        logs = []
        uncopied_cardtests = list(cardtests.find({'is_copied_to_other_database': False}))

        all_cards = list(cards.find())
        for cardtest in uncopied_cardtests:
            users_list = [user for user in all_cards if user['card_number'] == cardtest['card_number']]
            if users_list:
                user = users_list[0]
            else:
                user = {}
            log = Log(
                id=str(cardtest.get('_id', '')),
                log_id=cardtest.get('log_id', ''),
                card_counter=cardtest.get('card_counter', ''),
                card_number=cardtest.get('card_number', ''),
                card_category=cardtest.get('card_category', ''),
                in_out_symbol=cardtest.get('in_out_symbol', ''),
                mc_id=cardtest.get('mc_id', ''),
                test_datetime=cardtest.get('test_datetime', datetime.datetime.utcnow()),
                test_result=cardtest.get('test_result', ''),
                is_tested=cardtest.get('is_tested', ''),
                hand=cardtest.get('hand', ''),
                left_foot=cardtest.get('left_foot', ''),
                right_foot=cardtest.get('right_foot', ''),
                after_erg=cardtest.get('after_erg', ''),
                rsg=cardtest.get('rsg', ''),
                name=user.get('name', ''),
                job_number=user.get('job_number', ''),
                department=user.get('department', ''),
                gender=user.get('gender', ''),
                note=user.get('note', ''),
                belong_to_mc=user.get('belong_to_mc', ''),
            )

            if log.card_category == '0':
                log.card_category = 'vip'
            if log.card_category == '1':
                log.card_category = '只测手'
            if log.card_category == '2':
                log.card_category = '只测脚'
            if log.card_category == '3':
                log.card_category = '手脚都测'
            if log.gender == '0':
                log.gender = '女'
            if log.gender == '1':
                log.gender = '男'
            if log.test_result == '0':
                log.test_result = '不通过'
            if log.test_result == '1':
                log.test_result = '通过'
            if log.is_tested == '0':
                log.is_tested = '不测试'
            if log.is_tested == '1':
                log.is_tested = '测试'

            logs.append(log)

        logger.info(str(logs))
        session.add_all(logs)
        session.commit()

        requests = []
        for cardtest in uncopied_cardtests:
            requests.append(UpdateOne({'_id': cardtest['_id']}, {'$set': {'is_copied_to_other_database': True}}))
        try:
            cardtests.bulk_write(requests)
        except bulk.InvalidOperation:
            logger.info('pymongo bulk InvalidOperation: No operations to execute')

        session.close()
        engine.dispose()
    except Exception as e:
        logger.exception(e)

    logger.info('stop save_to_other_database task')
