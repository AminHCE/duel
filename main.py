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
        for item in cost:
            if self.resource[item] < cost[item]:
                payable = cost[item] - self.resource[item]
                coin += payable * (2 + (opponent[item] - self.resource[item]))

        return coin, True if coin <= self.coin else False

    def pick_card(self, card: Card, opponent):
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
        age_one_cards = cards['age_three']
        age_one = []
        for c in age_one_cards:
            card0 = Card(c['name'], c['age'], c['cost'], c['effect'], c['kind'], c['chain'] if 'chain' in c else None)
            age_one.append(card0)
            # print(card.chain)

    player2 = Player()
    test_card = age_one[11]
    print(test_card.cost)
    print('-----', player1.pick_card(test_card, player2))

    print('Player1 -> coin:', player1.coin)
    print('Player1 -> military:', player1.military)
    print('Player1 -> science:', player1.science)
    print('Player1 -> action:', player1.action)
    print('Player1 -> vp:', player1.count_vp())
    print('Player1 -> resource:', player1.resource)

    print('-------------------------------')

    print('Player2 -> coin:', player2.coin)
    print('Player2 -> military:', player2.military)
    print('Player2 -> science:', player2.science)
    print('Player2 -> action:', player2.action)
    print('Player2 -> vp:', player2.count_vp())
    print('Player2 -> resource:', player2.resource)
