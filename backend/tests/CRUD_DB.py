import random
from pymongo import MongoClient
from instance.config_default import MONGODB_SETTINGS

log = print

client = MongoClient(MONGODB_SETTINGS['host'], MONGODB_SETTINGS['port'])
mongodb_name = "quatek_web_app"
db = client[mongodb_name]


def insert_a_card(card):
    db.card.insert(card)


def insert_cards_to_db(num):
    for i in range(num):
        name_str = "abcdefghijklmnopqrstuvwxyz"
        name = ''.join(random.sample(name_str, 5))
        gender_str = "01"
        gender = ''.join(random.sample(gender_str, 1))
        category_str = "0123"
        card_category = ''.join(random.sample(category_str, 1))
        belong_to_mc = 'name1:0|name2:0'

        job_number = str(i)
        card_counter = str(i)

        card = {
            'name': name,
            'job_number': job_number,
            'department': 'RD',
            'gender': gender,
            'note': 'REMARK',
            'belong_to_mc': belong_to_mc,
            'card_number': "002A7DAA",
            'card_counter': card_counter,
            'card_category': card_category,
        }
        db.card.insert(card)


def get_card_from_db(card_counter):
    query = {
        'card_counter': card_counter,
    }
    cards = db.card.find(query)
    card = cards[0]
    card_dict = {
        'name': card["name"],
        'job_number': card["job_number"],
        'department': card["department"],
        'gender': card["gender"],
        'note': card["note"],
        'belong_to_mc': card["belong_to_mc"],
        'card_number': card["card_counter"],
        'card_counter': card["card_counter"],
        'card_category': card["card_category"],
    }
    return card_dict


def remove_card_for_db(card_counter):
    query = {
        'card_counter': card_counter,
    }
    db.card.remove(query)


def get_gate_from_db(client_id):
    query = {
        'mc_id': client_id,
    }
    gates = db.gate
    mc_client = gates.find(query)[0]

    return mc_client


if __name__ == "__main__":
    insert_cards_to_db(2)
    # cards = db.card
    # for card in cards.find():
    #     # print(card)
    #     belong_to_mc = card['belong_to_mc']
    #     # print('belong_to_mc1', belong_to_mc)
    #     belong_to_mc = [{item.split(':')[0]: item.split(':')[1]} for item in belong_to_mc.split('|')]
    #     belong_to_mc_dict = {}
    #     for item in belong_to_mc:
    #         belong_to_mc_dict.update(item)
    # #     # print('belong_to_mc_dict', belong_to_mc_dict)
    #     string = '\rSET CARD;{card_counter};{card_number};{job_number};{name};{department};{gender};{card_category};{0};{note}\n'.format(
    #         belong_to_mc_dict[card['mc_id']], **card).encode()
    #     print(string)

    # card_dict = get_card_from_db("0")
    # print(card_dict)

    # insert_a_card()
