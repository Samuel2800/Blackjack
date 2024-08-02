import random
from card import Card

# Define the deck and values
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace']

class Deck:
    def __init__(self):
        self.deck = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()
