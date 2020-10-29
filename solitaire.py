import random

from game import InputGame, ADVANCE, MUSTER, DEVELOP, DESPOIL

# the four center-most spaces on a 6x6 grid
CENTER = ((2, 2), (2, 3), (3, 2), (3, 3))

def random_action (game, action_options):
    possible = []
    for action, options in action_options.items():
        for option in options:
            possible.append([action, option])
    if len(possible) > 0:
        action, param = random.choice(possible)
        action_func = getattr(game, '%s_action' % action.lower())
        action_func(param)

def despoiler (game, player):
    # WORK TIL YOU CAN'T
    # BUY WHILE YOU CAN
    # GRIN FOR YOU MUST
    # DIE! DIE! DIE!
    action_options = game.player_options(player)
    if len(action_options.items()) == 0: return # nothing to do
    if DESPOIL in action_options:
        options = action_options[DESPOIL]
        choice = random.choice(options)
        game.despoil_action(choice)
    elif MUSTER in action_options:
        options = action_options[MUSTER]
        choice = random.choice(options)
        game.muster_action(choice)
    else:
        random_action(game, action_options)

def overseer (game, player):
    # SUPREMACY IS THE POINT
    action_options = game.player_options(player)
    if len(action_options.items()) == 0: return # nothing to do
    # raise infrastructure in order to muster battalions
    if DEVELOP in action_options:
        options = action_options[DEVELOP]
        choice = random.choice(options)
        game.develop_action(choice)
    # raise more forces
    elif MUSTER in action_options:
        options = action_options[MUSTER]
        choice = random.choice(options)
        game.muster_action(choice)
    elif ADVANCE in action_options:
        # stomp a random thing that can be stomped
        other_units = game.other_player_units(player)
        flanked_coords = { unit.coord for unit in other_units if game.is_flanked(unit) }
        advance_options = action_options[ADVANCE]
        capture_options = [option for option in advance_options if option[1] in flanked_coords]
        center_occupied = all([game.unit(*coord) or not game.space(*coord).passable for coord in CENTER])
        if len(capture_options) > 0:
            choice = random.choice(capture_options)
            game.advance_action(choice)
        # or, move battalions toward the center to establish control
        elif not center_occupied:
            units = game.player_units(player)
            distances = []
            for coord in CENTER:
                for option in advance_options:
                    if option[0] in CENTER: continue
                    x_distance = abs(coord[0] - option[1][0])
                    y_distance = abs(coord[1] - option[1][1])
                    distance = x_distance + y_distance
                    distances.append([distance, option])
            min_distance = min([distance for distance, option in distances])
            options = [option for distance, option in distances if distance == min_distance]
            choice = random.choice(options)
            game.advance_action(choice)
        else:
            random_action(game, action_options)
    else:
        random_action(game, action_options)

def technocrat (game, player):
    # I'M SURE THAT WITH THE RIGHT PEOPLE IN PLACE
    # YOU KNOW, THE PEOPLE WHO KNOW ABOUT THIS SORT OF THING
    # THAT EVERYTHING WILL BE FINE.
    action_options = game.player_options(player)
    if len(action_options.items()) == 0: return # nothing to do
    units = game.player_units(player)
    if len(units) == 0 and MUSTER in action_options:
        # no units. attempt to muster.
        options = action_options[MUSTER]
        choice = random.choice(options)
        game.muster_action(choice)
    elif DEVELOP in action_options:
        # develop
        options = action_options[DEVELOP]
        choice = random.choice(options)
        game.develop_action(choice)
    elif ADVANCE in action_options:
        # advance
        options = action_options[ADVANCE]
        choice = random.choice(options)
        game.advance_action(choice)
    else:
        random_action(game, action_options)

class SolitaireGame(InputGame):
    """
    A single-player game in which the other three positions are occupied by AI.
    """

    def __init__ (self):
        super(SolitaireGame, self).__init__(4)

    def do_turn (self, player):
        if player == 0:
            super(SolitaireGame, self).do_turn(player)
        elif player == 1:
            despoiler(self, player)
        elif player == 2:
            overseer(self, player)
        elif player == 3:
            technocrat(self, player)

if __name__ == '__main__':
    SolitaireGame.introduction()
    game = SolitaireGame()
    game.play()
