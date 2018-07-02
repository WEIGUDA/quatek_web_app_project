from . import *


main = Blueprint('card', __name__)
card_api = Api(main)


def get_card(card):
    card_dic = dict(
        card_id=card.card_id,
        category=card.category,
        job_number=card.job_number,
        created_time=card.created_time,
    )
    return card_dic


class CardResource(Resource):
    def get(self):
        args = request.args
        card_id = args.get('card_id')
        setoff = args.get('setoff')
        limit = args.get('limit')

        try:
            # 获取单个卡片
            if card_id is not None and setoff is None and limit is None:
                card = Card.objects(card_id=card_id).first()
                card_dic = get_card(card)
                return jsonify(card_dic)
            # 获取所有卡片
            if card_id is None and setoff is None and limit is None:
                cards = Card.objects().all()
                card_list = []
                for card in cards:
                    card_dic = get_card(card)
                    card_list.append(card_dic)
                return jsonify(card_list)
            # 按 setoff 和 limit 获取卡片
            if card_id is None and setoff is not None and limit is not None:
                cards = Card.objects().skip(int(setoff)).limit(int(limit))
                card_list = []
                for card in cards:
                    card_dic = get_card(card)
                    card_list.append(card_dic)
                return jsonify(card_list)
        except:
            message = "get cards failed"
            return message

    def post(self):
        json = request.json
        card_id = json.get('card_id', '')
        category = json.get('category')
        job_number = json.get('job_number', '')

        dic = dict(
            card_id=card_id,
            category=category,
            job_number=job_number,
        )
        try:
            if card_id is not None:
                card = Card.objects(card_id=card_id).first()
                if card:
                    message = "Card {} has been added already, please use patch".format(card_id)
                else:
                    card = Card()
                    card.set_attribute(dic)
                    card.save()
                    message = "card {} add successfully".format(card_id)
            else:
                message = "Card id should not be ignored."
            return message
        except:
            message = "card add failed"
            return message

    def patch(self):
        json = request.json
        card_id = json.get('card_id')
        if card_id is not None:
            card = Card.objects(card_id=card_id).first()
            category = json.get('category', card.category)
            job_number = json.get('job_number', card.job_number)

            try:
                card.update(
                    category=category,
                    job_number=job_number,
                )
                message = "card {} update successfully".format(card_id)
                return message
            except:
                message = "card {} update failed".format(card_id)
                return message
        else:
            message = "Card id should not be ignored."
            return message

    def delete(self):
        args = request.args
        card_id = args.get('card_id')
        try:
            card = Card.objects(card_id=card_id).first()
            card.delete()
            message = "card {} delete successfully".format(card_id)
            return message
        except:
            message = "card {} delete failed".format(card_id)
            return message


card_api.add_resource(CardResource, '/gate/card')


def get_card_template(card, user):
    template_dic = dict(
        username=user.username,
        job_number=card.job_number,
        card_id=card.card_id,
        category=card.category,
        department=user.department,
    )
    return template_dic


class CardTemplate(Resource):
    def get(self):
        args = request.args
        setoff = args.get('setoff', '0')
        limit = args.get('limit', '10')

        try:
            card_list = []
            cards = Card.objects().skip(int(setoff)).limit(int(limit)).order_by("department")
            for card in cards:
                job_number = card.job_number
                user = User.objects(job_number=job_number).first()
                card_dic = get_card_template(card, user)
                card_list.append(card_dic)
            return jsonify(card_list)
        except:
            message = "get card templates failed"
            return message


card_api.add_resource(CardTemplate, '/gate/card/template')


class SearchCardTemplate(Resource):
    # 姓名 工号 卡号 部门
    def get(self):
        args = request.args
        content = args.get('query')
        user_kwargs = dict(
            username=content,
            job_number=content,
            department=content,
        )
        card_kwargs = dict(
            card_id=content,
        )
        user_queries = list(map(lambda i: Q(**{i[0]: i[1]}), user_kwargs.items()))
        card_queries = list(map(lambda i: Q(**{i[0]: i[1]}), card_kwargs.items()))
        user_query = QCombination(QCombination.OR, user_queries)
        card_query = QCombination(QCombination.OR, card_queries)
        users = User.objects(user_query).all()
        cards = Card.objects(card_query).all()
        card_list = []
        for user in users:
            if user is not None:
                job_number = user.job_number
                card = Card.objects(job_number=job_number).first()
                if card is not None:
                    card_dic = get_card_template(card, user)
                    card_list.append(card_dic)
        for card in cards:
            if card is not None:
                job_number = card.job_number
                user = User.objects(job_number=job_number).first()
                if user is not None:
                    card_dic = get_card_template(card, user)
                    for i in card_list:
                        if i["job_number"] != job_number:
                            card_list.append(card_dic)
        return jsonify(card_list)


card_api.add_resource(SearchCardTemplate, '/gate/card/template/search')


if __name__ == "__main__":
    pass
