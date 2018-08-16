import random

from app.tasks import update_all_cards_to_mc_task, delete_a_card_from_mc_task, get_logs_from_mc_task, update_a_card_to_all_mc_task
from tests.CRUD_DB import insert_cards_to_db, insert_a_card, get_card_from_db, remove_card_for_db


def test_update_all_cards():
    update_all_cards_to_mc_task()


def test_update_a_card():
    name_str = "abcdefghijklmnopqrstuvwxyz"
    name = ''.join(random.sample(name_str, 5))
    gender_str = "01"
    gender = ''.join(random.sample(gender_str, 1))
    category_str = "0123"
    card_category = ''.join(random.sample(category_str, 1))
    belong_to_mc = 'name1:0|name2:1'

    job_number = str(1)
    card_counter = str(1)

    card = {
        'name': name,
        'job_number': job_number,
        'department': 'RD',
        'gender': gender,
        'note': 'REMARK',
        'belong_to_mc': belong_to_mc,
        'card_number': "00BC5C01",
        'card_counter': card_counter,
        'card_category': card_category,
    }
    update_a_card_to_all_mc_task(card)
    # insert_a_card(card)


def test_delete_a_card():
    card_dict = get_card_from_db("2")
    delete_a_card_from_mc_task(card_dict, 10)
    # remove_card_for_db("0")


def test_get_log():
    get_logs_from_mc_task()


if __name__ == "__main__":
    # test_update_all_cards()
    # test_update_a_card()
    # test_delete_a_card()
    get_logs_from_mc_task()
    # lis = ['1', '2', '3', '4']
    # string = ''.join(lis)
    # print(string)
    # all_data = '\rLOG 4294967295,0,00CF1974,3,1,16,1900-01-01 00:00:00,1,0,FREE,FREE,FREE,NO\n\rLOG 4294967295,0,00CF1974,3,1,16,1900-01-01 00:00:00,1,0,FREE,FREE,FREE,NO\n'
    # all_data = all_data[all_data.find('LOG'):all_data.rfind(
    #     '\n')].replace('\r', '').replace('LOG ', '').split('\n')
    # # print(all_data)
    # all_cardtests = []
    # for data in all_data:
    #     temp_dict = {}
    #     for t, v in zip(
    #             ['log_id', 'card_counter', 'card_number', 'card_category', 'in_out_symbol', 'mc_id', 'test_datetime',
    #              'test_result', 'is_tested', 'hand', 'left_foot', 'right_foot', 'after_erg'], data.split(',')):
    #         temp_dict.update({t: v})
    #     all_cardtests.append(temp_dict)
    # print(all_cardtests)
