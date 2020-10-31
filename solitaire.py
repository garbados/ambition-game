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
    # despoil if you can
    if DESPOIL in action_options:
        options = action_options[DESPOIL]
        choice = random.choice(options)
        game.despoil_action(choice)
    # muster if you can't
    elif MUSTER in action_options:
        options = action_options[MUSTER]
        choice = random.choice(options)
        game.muster_action(choice)
    else:
        random_action(game, action_options)

def overseer (game, player):
    # OF COURSE OUR SUPERVISION IS NECESSARY
    # WHY, JUST THINK OF ALL THE TERRIBLE THINGS YOU MIGHT DO
    # IF LEFT TO YOUR OWN DEVICES
    action_options = game.player_options(player)
    other_units = game.other_player_units(player)
    flanked_coords = { unit.coord for unit in other_units if game.is_flanked(unit) }
    advance_options = action_options.get(ADVANCE, [])
    capture_options = [option for option in advance_options if option[1] in flanked_coords]
    center_occupied = all([game.unit(*coord) or not game.space(*coord).passable for coord in CENTER])
    # stomp a random thing that can be stomped
    if len(capture_options) > 0:
        choice = random.choice(capture_options)
        game.advance_action(choice)
    # raise infrastructure in order to muster battalions
    elif DEVELOP in action_options:
        options = action_options[DEVELOP]
        choice = random.choice(options)
        game.develop_action(choice)
    # raise more forces
    elif MUSTER in action_options:
        options = action_options[MUSTER]
        choice = random.choice(options)
        game.muster_action(choice)
    # move toward the center to establish control
    elif ADVANCE in action_options and not center_occupied:
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

def technocrat (game, player):
    # I'M SURE THAT WITH THE RIGHT PEOPLE IN PLACE
    # YOU KNOW, THE PEOPLE WHO KNOW ABOUT THIS SORT OF THING
    # THAT EVERYTHING WILL BE FINE.
    action_options = game.player_options(player)
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

def expansionist (game, player):
    # ONCE, WE SPANNED THE GLOBE
    # WHY NOT AGAIN?
    # WHY NOT FOREVER
    action_options = game.player_options(player)
    develop_options = action_options.get(DEVELOP, [])
    low_infra_spaces = [coord for coord in develop_options if game.space(*coord)._infra == 0]
    move_options = action_options.get(ADVANCE, [])
    no_infra_moves = [coords for coords in move_options if game.space(*coords[1])._infra == 0]
    # develop any spaces with 0 infra
    if len(low_infra_spaces) > 0:
        choice = random.choice(low_infra_spaces)
        game.develop_action(choice)
    # move to a space with 0 infra
    elif ADVANCE in action_options and len(no_infra_moves) > 0:
        choice = random.choice(no_infra_moves)
        game.advance_action(choice)
    # muster if you have no units
    elif MUSTER in action_options:
        options = action_options[MUSTER]
        choice = random.choice(options)
        game.muster_action(choice)
    # develop further if there is nowhere left to go
    elif DEVELOP in action_options:
        options = action_options[DEVELOP]
        choice = random.choice(options)
        game.develop_action(choice)
    # move somewhere. anywhere!
    elif ADVANCE in action_options:
        options = action_options[ADVANCE]
        choice = random.choice(options)
        game.advance_action(choice)
    else:
        random_action(game, action_options)

def random_player (game, player):
    # IS FREE WILL A PHYSICAL FACT
    # OR A MATTER OF PERSPECTIVE?
    action_options = game.player_options(player)
    random_action(game, action_options)

AI = [despoiler, overseer, technocrat, expansionist, random_player]

class SolitaireGame(InputGame):
    """
    A single-player game in which the other three positions are occupied by AI.
    """

    def __init__ (self):
        super(SolitaireGame, self).__init__(4)
        # keep who's who a secret
        self._ai = [random.choice(AI) for i in range(3)]

    def do_turn (self, player):
        if player == 0:
            super(SolitaireGame, self).do_turn(player)
        else:
            ai = self._ai[player-1]
            ai(self, player)

if __name__ == '__main__':
    SolitaireGame.introduction()
    game = SolitaireGame()
    game.play()
