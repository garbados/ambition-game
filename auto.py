"""
Four AI against each other.
"""

import random
from solitaire import SolitaireGame, random_action

def random_player (game, player):
    action_options = game.player_options(player)
    random_action(game, action_options)

class AutoGame(SolitaireGame):
    def __init__ (self, *args, **kwargs):
        super(AutoGame, self).__init__(*args, **kwargs)

    def do_turn (self, player):
        if player == 0:
            random_player(self, player)
        else:
            super(AutoGame, self).do_turn(player)
        self.print_map()

if __name__ == '__main__':
    AutoGame.introduction()
    game = AutoGame()
    game.play()
