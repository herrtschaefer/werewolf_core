"""Test the Deck class"""

import pytest
import sys
from utils.Deck import Deck  # assuming Deck.py defines the Deck class


class Card:
    def __init__(self, suit: str, value: int):
        self.suit = suit
        self.value = value

    def __eq__(self, other):
        return isinstance(other, Card) and self.suit == other.suit and self.value == other.value

    def __repr__(self):
        return f"Card:({self.suit}, {self.value})"


def test_deck_with_card_objects():
    cards = [Card("Heart", 1), Card("Clubs", 10), Card("Heart", 4), Card("Diamond", 5)]
    deck = Deck(cards)
    assert len(deck) == 4
    assert all(isinstance(c, Card) for c in deck.cards)


def test_deck_with_card_tuples():
    cards = [
        (Card("Heart", 1), 2),
        (Card("Clubs", 10), 3),
        (Card("Diamond", 5), 1)
    ]
    deck = Deck(cards)
    assert len(deck) == 6
    assert deck.cards.count(Card("Heart", 1)) == 2
    assert deck.cards.count(Card("Clubs", 10)) == 3


def test_deck_with_mixed_entries():
    mixed = [
        Card("Heart", 1),
        (Card("Clubs", 10), 2),
        "Witch",
        ("Werewolf", 3),
        42
    ]
    deck = Deck(mixed)
    assert len(deck) == 1 + 2 + 1 + 3 + 1  # total: 8
    assert deck.cards.count("Werewolf") == 3
    assert "Witch" in deck.cards
    assert 42 in deck.cards


def test_deck_with_invalid_tuples():
    invalid_inputs = [
        ("Wolf", "two"),
        ("Villager",),
        ("Ghost", 1, "extra"),
        (Card("Spade", 2), "one")
    ]
    for item in invalid_inputs:
        with pytest.raises(ValueError):
            Deck([item])


def test_deck_add_card_and_remove_card():
    deck = Deck()
    card = Card("Heart", 7)
    deck.add_card(card, amount=3)
    assert deck.cards.count(card) == 3

    deck.remove_card(card)
    assert deck.cards.count(card) == 2

    with pytest.raises(ValueError):
        deck.remove_card("Not in deck")


def test_shuffle_does_not_change_count():
    cards = [("A", 10), "B", "C"]
    deck = Deck(cards)
    original_count = len(deck.cards)
    deck.shuffle()
    assert len(deck.cards) == original_count

def test_shuffle_does_rearrange_cards():
    original = ["A", "B", "C", "D", "E"]
    deck = Deck(original)

    original_order = deck.cards.copy()
    different_order_found = False

    # Versuch es mehrfach, da Shuffle rein zufällig ist
    for _ in range(10):
        deck.shuffle()
        if deck.cards != original_order:
            different_order_found = True
            break

    assert different_order_found, "Deck.shuffle() hat auch nach mehreren Versuchen keine neue Reihenfolge erzeugt."
    
def test_draw_valid_number():
    deck = Deck(["A", "B", "C", "D", "E"])
    drawn = deck.draw(2)
    assert drawn == ["E", "D"]
    assert deck.cards == ["A", "B", "C"]

def test_draw_default_one_card():
    deck = Deck(["X", "Y", "Z"])
    drawn = deck.draw()
    assert drawn == ["Z"]
    assert deck.cards == ["X", "Y"]

def test_draw_invalid_number_type():
    deck = Deck(["A", "B"])
    with pytest.raises(ValueError):
        deck.draw("two")

def test_draw_number_less_than_one():
    deck = Deck(["A", "B"])
    with pytest.raises(ValueError):
        deck.draw(0)

def test_draw_too_many_cards():
    deck = Deck(["A", "B"])
    with pytest.raises(IndexError):
        deck.draw(3)
        
def test_draw_from_empty_deck():
    deck = Deck()
    with pytest.raises(IndexError):
        deck.draw()
        
def test_draw_none():
    deck = Deck(["A", "B", "C", "D", "E"])
    drawn = deck.draw(None)
    assert drawn == ["E"]
    assert deck.cards == ["A", "B", "C","D"]

def test_draw_negative():
    deck = Deck(["A", "B", "C", "D", "E"])
    with pytest.raises(ValueError):
        deck.draw(-1)

def test_str():
    deck = Deck(["A", ("B",2), "D"])
    
    assert str(deck) == "Deck(['A', 'B', 'B', 'D'])"

def test_add_card():
    deck = Deck()
    deck.add_card("A")
    deck.add_card("b",3)
    assert deck.cards==["A","b","b","b"]
    
def test_len():
    deck1 = Deck()
    deck2 = Deck(["A","B"])
    deck3 = Deck([("A",3)])
    deck4 = Deck(["A"])
    deck4.draw()
    
    assert len(deck4) == 0
    assert len(deck1) == 0
    assert len(deck2) == 2
    assert len(deck3) == 3