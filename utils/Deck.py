import random


class Deck:
    def __init__(self, cards=None):
        self.cards = []
        if cards:
            for card in cards:
                if isinstance(card, tuple):
                    if len(card) == 2 and isinstance(card[1], int):
                        self.cards.extend([card[0]] * card[1])
                    else:
                        raise ValueError(f"Ungültiges Kartenformat: {card}. Erwarte (Objekt, int).")
                else:
                    self.cards.append(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def add_card(self, card, amount=1):
        if not isinstance(amount, int) or amount < 1:
            raise ValueError("Die Anzahl muss eine positive ganze Zahl sein.")
        self.cards.extend([card] * amount)

    def remove_card(self, card):
        try:
            self.cards.remove(card)
        except ValueError:
            raise ValueError(f"Karte {card} ist nicht im Deck enthalten und kann nicht entfernt werden.")

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return f"Deck({self.cards})"
