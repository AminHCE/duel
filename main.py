import json


class Wonder:
    def __init__(self, name, cost, effect):
        self.name = name
        self.cost = cost
        self.effect = effect


class Card:
    def __init__(self, name, age, cost, effect, kind, chain):
        self.name = name
        self.age = age
        self.cost = cost
        self.chain = chain
        self.effect = effect
        self.kind = kind

    def coin(self) -> int:
        return self.cost['coin']

    def resource(self) -> dict:
        resource = self.cost.copy()
        del resource['coin']
        return resource


class Progress:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect


class Player:
    def __init__(self):
        self.coin = 7
        self.resource = {
            'wood': 0,
            'clay': 0,
            'stone': 0,
            'glass': 0,
            'papyrus': 0
        }
        self.military = 0
        self.science = list()
        self.action = list()
        self.cards = list()
        self.vp = 0

    def count_vp(self):
        coin_vp = self.coin // 3
        return self.vp + coin_vp

    def card_cost(self, cost, coin, opponent):
        expenses = list()
        for item in cost:
            if self.resource[item] < cost[item]:
                payable_count = cost[item] - self.resource[item]
                if f'{item}_cost_set_one' in self.action:
                    item_cost = 1
                else:
                    item_cost = 2 + (opponent[item] - self.resource[item])

                expenses.append({'resource': item, 'cost': item_cost, 'count': payable_count})
                coin += payable_count * item_cost

        expenses = sorted(expenses, key=lambda d: d['cost'], reverse=True)

        discount_actions = ['glass|papyrus', 'wood|clay|stone']
        for discount in discount_actions:
            for i in range(self.action.count(discount)):
                discount_resources = discount.split('|')
                indexes = list()
                for resource in discount_resources:
                    index = next((i for i, d in enumerate(expenses) if d.get('resource') == resource), None)
                    if index is not None:
                        indexes.append(index)

                for target_index in sorted(indexes):
                    if target_index is not None and expenses[target_index]['count'] > 0:
                        coin -= expenses[target_index]['cost']
                        expenses[target_index]['count'] = max(expenses[target_index]['count'] - 1, 0)
                        break

        return coin, True if coin <= self.coin else False

    def pick_card(self, card: Card, opponent):
        if card.chain is not None and card.chain in self.action:
            cost, can_pick_card = 0, True
        else:
            cost, can_pick_card = self.card_cost(card.resource(), card.coin(), opponent.resource)
        if can_pick_card and card not in self.cards:
            self.coin -= cost
            self.cards.append(card)
            self.vp += card.effect['vp'] if 'vp' in card.effect else 0
            if 'military' in card.effect:
                self.military += card.effect['military']
                opponent.military -= card.effect['military']
            if 'science' in card.effect:
                self.science.append(card.effect['science'])
            self.resource['wood'] += card.effect['wood'] if 'wood' in card.effect else 0
            self.resource['clay'] += card.effect['clay'] if 'clay' in card.effect else 0
            self.resource['stone'] += card.effect['stone'] if 'stone' in card.effect else 0
            self.resource['glass'] += card.effect['glass'] if 'glass' in card.effect else 0
            self.resource['papyrus'] += card.effect['papyrus'] if 'papyrus' in card.effect else 0
            if 'action' in card.effect:
                self.action.append(card.effect['action'])
        else:
            print('you can\'t pick this card')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    player1 = Player()
    # print(player1.vp)
    # print(player1.count_vp())

    with open('cards.json') as f:
        cards = json.load(f)
        age_one_cards = cards['age_one']
        age_one = []
        for c in age_one_cards:
            card0 = Card(c['name'], c['age'], c['cost'], c['effect'], c['kind'], c['chain'] if 'chain' in c else None)
            age_one.append(card0)
            # print(card.chain)

    with open('cards.json') as f:
        cards = json.load(f)
        age_two_cards = cards['age_three']
        age_two = []
        for c in age_two_cards:
            card0 = Card(c['name'], c['age'], c['cost'], c['effect'], c['kind'], c['chain'] if 'chain' in c else None)
            age_two.append(card0)
            # print(card.chain)

    player2 = Player()
    test_card = age_one[2]
    print(age_two[10].cost)
    print(age_two[10].chain)
    print('-----', player1.pick_card(age_one[3], player2))
    print('-----', player1.pick_card(age_one[6], player2))
    print('-----', player1.pick_card(age_one[12], player2))
    print('-----', player1.pick_card(age_one[16], player2))
    print('-----', player1.pick_card(age_one[9], player2))
    print('-----', player1.pick_card(age_two[10], player2))
    # print('-----', player1.pick_card(test_card, player2))

    print('Player1 -> coin:', player1.coin)
    print('Player1 -> military:', player1.military)
    print('Player1 -> science:', player1.science)
    print('Player1 -> action:', player1.action)
    print('Player1 -> vp:', player1.count_vp())
    print('Player1 -> resource:', player1.resource)

    # print('-------------------------------')

    # print('Player2 -> coin:', player2.coin)
    # print('Player2 -> military:', player2.military)
    # print('Player2 -> science:', player2.science)
    # print('Player2 -> action:', player2.action)
    # print('Player2 -> vp:', player2.count_vp())
    # print('Player2 -> resource:', player2.resource)
