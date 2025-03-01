import os
import sys
script_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
from blackjack_api.blackjack import BlackJack
from blackjack_api.deck import Deck
from blackjack_api.card import Card


blackjack = BlackJack(num_decks=2)
print("Deck:", blackjack.deck)
print("Discard:", blackjack.discard)
for card in blackjack.active_cards:
    print(f"{card}: {blackjack.active_cards[card]}")
print()
print(blackjack.dealer)
print(blackjack.player)


blackjack.stand()
blackjack.start_round()
blackjack.start_hand()
print("\n")


print("Deck:", blackjack.deck)
print("Discard:", blackjack.discard)
for card in blackjack.active_cards:
    print(f"{card}: {blackjack.active_cards[card]}")
print("\n")
print(blackjack.dealer)
print(blackjack.player)
blackjack.stand()


blackjack.reset()


print("\nDeck:", blackjack.deck)
print("Discard:", blackjack.discard)
for card in blackjack.active_cards:
    print(f"{card}: {blackjack.active_cards[card]}")
print("\n")
print(blackjack.dealer)
print(blackjack.player)