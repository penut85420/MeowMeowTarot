import json
import os
import random


class TarotDeck:
    def __init__(self):
        with open("Data/Tarot.json", "rt", encoding="UTF-8") as fp:
            self.tarot_data = json.load(fp)
        self.tarot_img = "Data/TarotImages"
        self.init_deck()

    def init_deck(self):
        self.deck = list(range(78))
        random.shuffle(self.deck)

    def pick(self):
        if not self.deck:
            self.init_deck()

        idx = self.deck.pop()
        path_suffix, data_key, name_prefix = is_reverse()

        fn = f"{idx:02d}{path_suffix}.jpg"
        tarot_path = os.path.join(self.tarot_img, fn)

        data = self.tarot_data[f"{idx:02d}"]
        tarot_name = data["name"]
        tarot_name = f"{name_prefix}{tarot_name}"
        tarot_info = data[data_key]

        return tarot_path, tarot_info, tarot_name


def is_reverse():
    pos = ("", "positive", "正位")
    rev = ("r", "reversed", "逆位")
    return pos if random.random() < 0.5 else rev
