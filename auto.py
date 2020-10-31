"""
Four AI against each other.
"""

import random
import sys
from game import InputGame
from solitaire import AI

class AutoGame(InputGame):
    # I THOUGHT I WOULD MAKE A WORLD
    # WHERE ALL MY TOYS COULD PLAY
    # BUT BEYOND MY PRECONCEPTIONS
    # I FOUND THEY HAD THEIR OWN
    # STRANGE FANTASIES
    def __init__ (self, *args, **kwargs):
        super(AutoGame, self).__init__(*args, **kwargs)
        self._ai = []
        for player in range(self._players):
            ai = random.choice(AI)
            self._ai.append(ai)
        # since a human is just watching, it's ok for them to know who's who
        print('Playing with:')
        ai_names = [ai.__name__ for ai in self._ai]
        for i in range(len(ai_names)):
            name = ai_names[i]
            print('%d. %s' % (i + 1, name))

    def do_turn (self, player):
        ai = self._ai[player]
        ai(self, player)
        self.print_map()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        raw_players = sys.argv[1]
        players = int(raw_players)
    else:
        players = 4
    AutoGame.introduction()
    game = AutoGame(players)
    game.play()
