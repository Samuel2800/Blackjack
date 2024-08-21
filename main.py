from deck import Deck
from hand import Hand, HandWithInitialCard

# Define a function to handle bets
def take_bet(chips):
    while True:
        try:
            bet = int(input("How many chips would you like to bet? "))
            if bet > chips:
                print(f"Sorry, you do not have enough chips. You have: {chips}")
            else:
                return bet
        except ValueError:
            print("Sorry, a bet must be an integer.")

# Define a function for hitting
def hit(deck, hand):
    hand.add_card(deck.deal())

# Define a function to handle hit, stand, or split
def hit_stand_split(deck, hands, hand_index, chips, bet):
    global playing
    hand = hands[hand_index]
    while True:
        choice = input(f"Player's Hand {hand_index + 1}: Would you like to Hit, Stand, or Split? Enter 'h', 's', or 'p' ")
        if choice.lower() == 'h':
            hit(deck, hand)
            show_all_hands(hands, dealer_hand)
            if hand.value > 21:
                print(f"Player's Hand {hand_index + 1} busts!")
                break
        elif choice.lower() == 's':
            print(f"Player's Hand {hand_index + 1} stands. Dealer is playing.")
            break
        elif choice.lower() == 'p':
            if hand.can_split():
                if chips >= bet:
                    split_hand = hand.split()
                    hands.insert(hand_index + 1, split_hand)
                    hit(deck, hand)
                    hit(deck, split_hand)
                    chips -= bet  # Deduct chips for the new bet
                    show_all_hands(hands, dealer_hand)
                else:
                    print("Sorry, you do not have enough chips to split.")
            else:
                print("Sorry, you cannot split this hand.")
        else:
            print("Sorry, please try again.")
    return hands, chips

# Define a function to show some cards
def show_some(player, dealer):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print(f"Value: {player.value}")

# Define a function to show all cards
def show_all_hands(hands, dealer):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print(f"Value: {dealer.value}")
    for i, hand in enumerate(hands):
        print(f"\nPlayer's Hand {i + 1}:", *hand.cards, sep='\n ')
        print(f"Value: {hand.value}")

# Define functions to handle game outcomes
def player_busts(chips, bet):
    print("Player busts!")
    chips -= bet
    return chips

def player_wins(chips, bet):
    print("Player wins!")
    chips += bet
    return chips

def player_blackjack(chips, bet):
    print("Player has a Blackjack! Player wins 1.5 times the bet!")
    chips += int(1.5 * bet)
    return chips

def dealer_busts(chips, bet):
    print("Dealer busts!")
    chips += bet
    return chips

def dealer_wins(chips, bet):
    print("Dealer wins!")
    chips -= bet
    return chips

def push():
    print("Dealer and Player tie! It's a push.")

if __name__ == '__main__':
    chips = 100  # Initial chips
    playing = True  # Control variable for the game loop

    deck = Deck()  # Create the deck once, outside the game loop

    while True:
        print("\nWelcome to Blackjack!")

        # If the deck is low on cards, reshuffle
        if len(deck.deck) < 10:
            deck = Deck()

        # Deal two cards to each player
        player_hand = Hand()
        dealer_hand = Hand()

        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Take the player's bet
        bet = take_bet(chips)

        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # Check for Blackjack
        if player_hand.value == 21:
            if dealer_hand.value == 21:
                show_all_hands([player_hand], dealer_hand)
                push()
            else:
                chips = player_blackjack(chips, bet)
        else:
            hands = [player_hand]
            current_hand_index = 0

            while playing and current_hand_index < len(hands):
                hands, chips = hit_stand_split(deck, hands, current_hand_index, chips, bet)
                if hands[current_hand_index].value > 21:
                    chips = player_busts(chips, bet)
                current_hand_index += 1
                playing = current_hand_index < len(hands)

            # If player hasn't busted, play Dealer's hand until Dealer reaches 17
            if all(hand.value <= 21 for hand in hands):
                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)

                # Show all cards
                show_all_hands(hands, dealer_hand)

                # Run different winning scenarios for each hand
                for i, hand in enumerate(hands):
                    print(f"\nResults for Player's Hand {i + 1}:")
                    if dealer_hand.value > 21:
                        chips = dealer_busts(chips, bet)
                    elif dealer_hand.value > hand.value:
                        chips = dealer_wins(chips, bet)
                    elif dealer_hand.value < hand.value:
                        chips = player_wins(chips, bet)
                    else:
                        push()

        # Inform Player of their chips total
        print(f"\nPlayer's chips total: {chips}")

        # Ask to play again
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")

        if new_game.lower() != 'y':
            print("Thanks for playing!")
            break
        else:
            playing = True
