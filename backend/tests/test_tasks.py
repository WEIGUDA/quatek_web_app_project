import random

from app.tasks import update_all_cards
from tests.CRUD_DB import insert_cards_to_db

from app.tasks import update_a_card
from tests.CRUD_DB import insert_a_card

from tests.CRUD_DB import get_card_from_db
from tests.CRUD_DB import remove_card_for_db
from app.tasks import delete_a_card

from app.tasks import get_logs_from_mc


def test_update_all_cards():
    update_all_cards()


def test_update_a_card():
    name_str = "abcdefghijklmnopqrstuvwxyz"
    name = ''.join(random.sample(name_str, 5))
    gender_str = "01"
    gender = ''.join(random.sample(gender_str, 1))
    category_str = "0123"
    card_category = ''.join(random.sample(category_str, 1))
    belong_to_mc = 'name1:0|name2:0'

    job_number = str(0)
    card_counter = str(0)

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
    update_a_card(card)
    insert_a_card(card)


def test_delete_a_card():
    card_dict = get_card_from_db("0")
    delete_a_card(card_dict)
    # remove_card_for_db("0")


if __name__ == "__main__":
    test_update_all_cards()
    # test_update_a_card()
    # test_delete_a_card()

