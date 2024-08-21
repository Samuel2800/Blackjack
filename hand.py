from deck import values

class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == 'Ace':
            self.aces += 1
        self.adjust_for_ace()

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def split(self):
        card = self.cards.pop()
        self.value = values[self.cards[0].rank]
        return HandWithInitialCard(card)

class HandWithInitialCard(Hand):
    def __init__(self, initial_card):
        super().__init__()
        self.add_card(initial_card)
