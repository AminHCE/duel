import json
import random


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


class Age:
    def __init__(self):
        self.placements = {
            'age_one': [
                [1, 1, 0, 0, 0, 0],
                [1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
            ],
            'age_two': [
                [1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 1, 1, 1, 1],
                [0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 1, 1],
                [0, 0, 0, 0, 0, 0],
            ],
            'age_three': [
                [1, 1, 0, 0],
                [1, 1, 1, 0],
                [1, 1, 1, 1],
                [1, 2, 0, 1],
                [1, 1, 1, 1],
                [0, 1, 1, 1],
                [0, 0, 1, 1],
                [0, 0, 0, 0],
            ]
        }

        self.card_position = list()

    def position(self, age):
        with open('cards.json') as f:
            cards_dict = json.load(f)
            cards = cards_dict[f'age_{age}']
            age_cards = []
            for c in cards:
                card = Card(c['name'], c['age'], c['cost'], c['effect'], c['kind'], c['chain'] if 'chain' in c else None)
                age_cards.append(card)

        numbers = list(range(23))
        random.shuffle(numbers)

        index = 0
        for idx, x in enumerate(self.placements[f'age_{age}']):
            row_position = list()
            for idy, y in enumerate(x):
                single_position = {
                    "index": index if y == 1 else None,
                    "card": age_cards[index] if y == 1 else None,
                    "has_card": y,
                    "visible": True if idx % 2 == 0 else False
                }
                index += 1 if y == 1 else 0
                row_position.append(single_position)
            self.card_position.append(row_position)

    def available_position(self):
        available_card = list()
        max_x_len = len(self.card_position) - 1
        max_y_len = len(self.card_position[0]) - 1
        for idx, x in enumerate(self.card_position):
            for idy, y in enumerate(x):
                pointer = self.card_position[idx][idy]['has_card']
                pointer_down = self.card_position[min(idx+1, max_x_len)][idy]['has_card']
                pointer_down_right = self.card_position[min(idx+1, max_x_len)][min(idy+1, max_y_len)]['has_card']

                if pointer > pointer_down + pointer_down_right:
                    if self.card_position[idx][idy]['has_card'] == 1:
                        self.card_position[idx][idy]['visible'] = True
                        available_card.append(self.card_position[idx][idy])
                    elif self.card_position[idx][idy]['has_card'] == 2:
                        self.card_position[idx][idy]['has_card'] = 0

        return available_card

    def remained_position(self):
        remained = 0
        for idx, x in enumerate(self.card_position):
            for idy, y in enumerate(x):
                if y['has_card'] == 1:
                    remained += 1

        return remained

    def pick_card(self, index):
        if any(d['index'] == index for d in self.available_position()):
            for idx, x in enumerate(self.card_position):
                for idy, y in enumerate(x):
                    if y['index'] == index:
                        self.card_position[idx][idy]['card'] = None
                        self.card_position[idx][idy]['has_card'] = 0
                        break
        else:
            print('pick wrong number!')


def run():
    age = Age()
    age.position('two')
    for turn in range(20):
        print(age.available_position())
        print(age.remained_position())
        index = input("enter an index: ")
        age.pick_card(int(index))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    player1 = Player()
    # print(player1.vp)
    # print(player1.count_vp())

    # player2 = Player()
    # test_card = age_one[2]
    # print(age_two[10].cost)
    # print(age_two[10].chain)
    # print('-----', player1.pick_card(age_one[3], player2))
    # print('-----', player1.pick_card(age_one[6], player2))
    # print('-----', player1.pick_card(age_one[12], player2))
    # print('-----', player1.pick_card(age_one[16], player2))
    # print('-----', player1.pick_card(age_one[9], player2))
    # print('-----', player1.pick_card(age_two[10], player2))
    # # print('-----', player1.pick_card(test_card, player2))
    #
    # print('Player1 -> coin:', player1.coin)
    # print('Player1 -> military:', player1.military)
    # print('Player1 -> science:', player1.science)
    # print('Player1 -> action:', player1.action)
    # print('Player1 -> vp:', player1.count_vp())
    # print('Player1 -> resource:', player1.resource)

    # print('-------------------------------')

    # print('Player2 -> coin:', player2.coin)
    # print('Player2 -> military:', player2.military)
    # print('Player2 -> science:', player2.science)
    # print('Player2 -> action:', player2.action)
    # print('Player2 -> vp:', player2.count_vp())
    # print('Player2 -> resource:', player2.resource)

    run()
