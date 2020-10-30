import random
import sys

# actions
DESPOIL = 'Despoil'
DEVELOP = 'Develop'
MUSTER = 'Muster'
ADVANCE = 'Advance'
ACTIONS = [
    DESPOIL,
    DEVELOP,
    MUSTER,
    ADVANCE
]

# the dimension of the square board
BOARD_SIZE = 6
ROW_SIZE = range(0, BOARD_SIZE)
X_ROW = list('ABCDEF')

# starting positions for units and infrastructure
STARTING_POSITIONS = [
    [[2, 0], [3, 0]],
    [[2, 5], [3, 5]],
    [[0, 2], [0, 3]],
    [[5, 2], [5, 3]],
]

def abbrev_coords (x, y):
    """
    Abbreviate an (x, y) pair into a string like "A4".
    """
    c1 = X_ROW[x]
    c2 = str(BOARD_SIZE - y)
    return '%s%s' % (c1, c2)

def de_abbrev_coords (abbrev):
    """
    Given an abbreviated coordinate like "A4", convert it back to an (x, y)
    pair.
    """
    # get x coord
    c1 = abbrev[0]
    x = X_ROW.index(c1)
    # get y coord
    c2 = abbrev[1]
    y = int(c2) - 1
    # return as beloved tuple
    return (x, y)

def check_bounds (c):
    """
    Check if a given x- or y-value is within bounds on the board.
    """
    return c < BOARD_SIZE and c >= 0

def check_coords(coords):
    """
    Check a given [x, y] coordinate expression and return whether it is legal.
    """
    return all([check_bounds(c) for c in coords])

def adjacent_coords (x, y):
    """
    Return a list of (x, y) pairs for all valid coordinates adjacent to the
    given coordinates.
    """
    coords = [
        # left
        (x - 1, y),
        # right
        (x + 1, y),
        # up
        (x, y - 1),
        # down
        (x, y + 1),
        # up-left
        (x - 1, y - 1),
        # down-right
        (x + 1, y + 1),
        # down-left
        (x - 1, y + 1),
        # up-right
        (x + 1, y - 1)
    ]
    return [coord for coord in filter(check_coords, coords)]

def twice_adjacent_coords (x, y):
    """
    Return a list of (x, y) pairs for all coordinates within 2 spaces of the
    given coordinates.
    """
    adjacencies = adjacent_coords(x, y)
    further = [adjacent_coords(*coords) for coords in adjacencies]
    uniq_coords = set()
    uniq_coords.update(adjacencies)
    for coords in further:
        uniq_coords.update(coords)
    return list(uniq_coords)

class Space:
    def __init__ (self, x, y):
        self._x = x
        self._y = y
        self._infra = 0
        self._claimant = None
        self._impassable = False

    def __repr__ (self):
        return "%s-%s" % (abbrev_coords(self._x, self._y), self.claimant)

    @property
    def coord (self):
        return (self._x, self._y)

    @property
    def passable (self):
        return self._impassable == False

    @property
    def claimed (self):
        if not self.passable:
            return False
        elif self._infra == 0:
            return False
        elif self._claimant == None:
            return False
        else:
            return True

    @property
    def claimant (self):
        if self.claimed:
            return self._claimant
        else:
            return None

    def develop (self):
        assert self.passable
        if self._infra < 2:
            self._infra += 1

    def despoil (self):
        assert self.passable
        if self._infra == 0:
            self._impassable = True
        else:
            self._infra = 0

    def seize (self, claimant):
        assert self.passable
        self._claimant = claimant

class Unit:
    def __init__ (self, player, x, y, level = 1):
        self._player = player
        self._x = x
        self._y = y
        self._level = level

    @property
    def coord (self):
        return (self._x, self._y)

    @property
    def name (self):
        return self.__class__.__name__

    def advance (self, space):
        space.seize(self._player)
        self._x = space._x
        self._y = space._y

    def advance_options (self):
        pass

class Squadron(Unit):
    def __init__ (self, player, x, y):
        super(Squadron, self).__init__(player, x, y, 1)

    def advance_options (self):
        return adjacent_coords(self._x, self._y)

class Battalion(Unit):
    def __init__ (self, player, x, y):
        super(Battalion, self).__init__(player, x, y, 2)

    def advance_options (self):
        return twice_adjacent_coords(self._x, self._y)

class Game:
    def __init__ (self, players = 2):
        assert players >= 2 and players <= 4
        self._players = players
        # 6x6 grid
        self._map = [[Space(x, y) for y in ROW_SIZE] for x in ROW_SIZE]
        # units list
        self._units = []
        # starting conditions
        for player in range(0, players):
            for x, y in STARTING_POSITIONS[player]:
                space = self.space(x, y)
                # two 1-infra spaces
                space.develop()
                space.seize(player)
                # two squadrons
                unit = Squadron(player, x, y)
                self._units.append(unit)

    def space (self, x, y):
        return self._map[x][y]

    def spaces (self):
        for x in ROW_SIZE:
            for y in ROW_SIZE:
                yield self.space(x, y)

    def player_spaces (self, player):
        return [space for space in self.spaces() if space.claimant == player]

    def unit (self, x, y):
        units = [unit for unit in self._units if unit._x == x and unit._y == y]
        return None if len(units) == 0 else units[0]

    def player_units (self, player):
        """
        Return all units belonging to the given player.
        """
        return [unit for unit in self._units if unit._player == player]

    def other_player_units (self, player):
        """
        Return all units not belonging to the given player.
        """
        return [unit for unit in self._units if unit._player != player]

    def is_flanked (self, unit):
        """
        Return whether a unit is currently flanked.
        """
        player = unit._player
        other_units = self.other_player_units(player)
        can_flank = []
        for other_unit in other_units:
            in_range_x = abs(other_unit._x - unit._x) <= other_unit._level
            in_range_y = abs(other_unit._y - unit._y) <= other_unit._level
            if in_range_x and in_range_y:
                can_flank.append(other_unit)
        if len(can_flank) > 1:
            return True
        else:
            return False

    def shunt (self, unit):
        """
        Advance a unit to a random adjacent space.
        """
        options = []
        for coords in adjacent_coords(unit._x, unit._y):
            if not check_coords(coords): continue # out of bounds
            if self.unit(*coords): continue # occupied
            space = self.space(*coords)
            if not space.passable: continue # impassable
            options.append(space)
        if len(options) == 0:
            # nowhere to go. unit is destroyed in the chaos.
            self._units.remove(unit)
        else:
            space = random.choice(options)
            unit.advance(space)

    def despoilable (self):
        """
        Return all despoilable spaces.
        """
        # get a list of all passable, unclaimed spaces
        return [space for space in self.spaces() if space.passable and not space.claimed]

    def develop_options (self, player):
        """
        Select one space the player controls.
        """
        assert player >= 0 and player <= self._players
        coords_set = set()
        for space in self.player_spaces(player):
            if space._infra < 2:
                coords_set.update([space.coord])
        for unit in self.player_units(player):
            space = self.space(*unit.coord)
            if space._infra < 2 and space.coord not in coords_set:
                coords_set.update([space.coord])
        coords = list(coords_set)
        return coords

    def develop_action (self, coord):
        space = self.space(*coord)
        space.develop()

    def despoil_options (self, player):
        """
        Select once space containing a unit the player controls.
        """
        assert player >= 0 and player <= self._players
        units = self.player_units(player)
        coords = [(unit._x, unit._y) for unit in units]
        return coords

    def despoil_action (self, coord):
        """
        Despoil the space at the given coordinate.
        """
        space = self.space(*coord)
        space.despoil()
        if not space.passable:
            unit = self.unit(*coord)
            if unit: self.shunt(unit)

    def muster_options (self, player):
        """
        Select one space the player controls that is not occupied.
        """
        assert player >= 0 and player <= self._players
        spaces = self.player_spaces(player)
        ok = lambda space: not self.unit(space._x, space._y)
        valid_spaces = filter(ok, spaces)
        coords = [(space._x, space._y) for space in valid_spaces]
        return coords

    def muster_action (self, coord):
        """
        Spawn a new unit at the given coordinates.
        """
        space = self.space(*coord)
        player = space.claimant
        if space._infra == 1:
            # two squadrons
            unit = Squadron(player, *coord)
        elif space._infra == 2:
            unit = Battalion(player, *coord)
        self._units.append(unit)

    def advance_options (self, player):
        """
        Move a unit to somewhere within its range.
        """
        assert player >= 0 and player <= self._players
        units = [unit for unit in self._units if unit._player == player]
        options = []
        for unit in units:
            for coord in unit.advance_options():
                # check if coord is passable
                space = self.space(*coord)
                if not space.passable:
                    continue
                # check if coord is occupied
                other_unit = self.unit(*coord)
                if other_unit:
                    if not self.is_flanked(other_unit) or other_unit._player == player:
                        continue # space is occupied and not flanked or not an enemy
                options.append([(unit._x, unit._y), coord])
        return options

    def advance_action (self, coords):
        """
        Move a unit and potentially destroy the unit that it moves on top of.
        """
        coord1, coord2 = coords
        unit = self.unit(*coord1)
        other_unit = self.unit(*coord2)
        if other_unit:
            self._units.remove(other_unit)
        space = self.space(*coord2)
        unit.advance(space)

    def player_options (self, player):
        all_options = {
            DEVELOP: self.develop_options(player),
            DESPOIL: self.despoil_options(player),
            MUSTER: self.muster_options(player),
            ADVANCE: self.advance_options(player)
        }
        return { action: options for action, options in all_options.items() if len(options) > 0 }

    def end_round (self):
        # if there are no more despoilable spaces, end the game
        despoilable = self.despoilable()
        if len(despoilable) == 0:
            scores = { player: 0 for player in range(0, self._players) }
            for space in self.spaces():
                if space.claimed:
                    scores[space.claimant] += space._infra
            return scores
        else:
            # despoil a space, since we know one can still be despoiled
            space = random.choice(despoilable)
            # despoil it
            space.despoil()
            # shunt unit if one exists
            unit = self.unit(space._x, space._y)
            if unit: self.shunt(unit)

    def do_turn (self, player):
        raise Error("Not Implemented")

    def do_round (self):
        # have each player take their turn
        for player in range(0, self._players):
            self.do_turn(player)
        return self.end_round()

    def play (self):
        while True:
            scores = self.do_round()
            if scores:
                # game over
                break

def choose (options):
    while True:
        raw_choice = input('Choose 1 - %d: ' % len(options))
        # parse choice from string to number, or ask for correct input
        try:
            choice = int(raw_choice)
            if choice > 0 and choice <= len(options):
                break
        except Exception:
            print('Invalid choice. Must be a number between 1 and %d.' % len(options))
    return options[choice - 1]

def print_options (options):
    for i in range(0, len(options)):
        print('%d: %s' % (i + 1, options[i]))

def print_coords (coords):
    print_options([abbrev_coords(*coord) for coord in coords])

def print_advance_coords (options):
    # abbreviate `((x1, y1), (x2, y2))` as `A1 -> B2`
    abbrevs = []
    for option in options:
        abbrev1, abbrev2 = [abbrev_coords(*coord) for coord in option]
        abbrevs.append("%s -> %s" % (abbrev1, abbrev2))
    print_options(abbrevs)

class InputGame(Game):
    """
    Game that can be played in a terminal using a keyboard, using `print` and
    `input`.
    """

    @classmethod
    def introduction (cls):
        print('')
        print('AMBITION - a game by garbados')
        print('')
        print('> THE WORLD IS ENDING.')
        print('> THE SKY CHURNS WITH POISON AND TOXIC SEAS BOIL.')
        print('> YOUR PEOPLE MUST SURVIVE.')
        print('> WILL THEY?')
        print('')

    def conclusion (self, scores):
        print('')
        print("Game over!")
        print('')
        print('> THE SEASON OF DESTRUCTION HAS COME.')
        print('> SURVIVORS HUNKER DOWN WITH THEIR ANGUISH.')
        print('> THE SUN RISES NO LONGER.')
        print('')
        print('> HAVE YOUR AMBITIONS SERVED YOU?')
        print('> OR HAVE THEY DEVOURED YOU?')
        print('')
        print("Scores:")
        for player in range(0, self._players):
            score = scores[player]
            msg = "- Player %d: %d" % (player + 1, score)
            survived = "(dead)" if score < 10 else "(survived)"
            print(msg + " " + survived)
        print('')
        print('Group award:')
        survivors = len([player for player, score in scores.items() if score >= 10])
        if survivors == 0:
            print('- Death Cult (no survivors)')
            print('')
            print('> IN THE END, NO ONE LIVED.')
            print('> NO ONE WANTED TO. NOT ENOUGH, ANYWAY.')
            print('> DYING CORRECTLY PRESENTED THE GREATER FEAT.')
            print('> AN INDIFFERENT UNIVERSE GOES ON.')
        elif survivors == 1:
            print('- Highlander (one survivor)')
            print('')
            print('> ONLY ONE SET OF TALES SURVIVES THE CATACLYSM.')
            print('> GENERATIONS ARE RAISED WITHOUT DAWN, FOR WHOM IT IS HISTORY.')
            print('> OR, A FUTURE IMAGINED.')
            print('> A WORLD LIVES TO DISCOVER THE REST THROUGH THEIR RUINS.')
        elif survivors == round(self._players / 2):
            print('- Malthus (half survived)')
            print('')
            print('> YOU MADE THE HARD CHOICES. YOU DID THE MATH. YOU RAN THE NUMBERS.')
            print('> HOW ELSE COULD IT HAVE BEEN? IF ANYONE WAS TO SURVIVE, YOU HAD TO.')
            print('> AT LEAST,')
            print('> THAT\'S WHAT YOU TELL THEIR GHOSTS.')
        elif survivors == self._players:
            print('- Humanitarian (everyone survived)')
            print('')
            print('> NO ONE HAD TO DIE. THAT HAD ALWAYS BEEN THE TRUTH.')
            print('> WHETHER BY CHANCE OR NATURE, THE BLISTERING SINS')
            print('> OF THE MACHINATIONS OF HATE AND GREED')
            print('> OVERCAME NO ONE.')
            print('> WE STOOD TOGETHER AND PREPARED,')
            print('> AND AFTER US, ALL WE STOOD FOR WENT ON.')
        else:
            print('- None')
            print('')
            print('> SOME LIVE. SOME DIE.')
            print('> THAT IS THE PROCESS BY WHICH LIFE HAS TRAVELLED THROUGH TIME,')
            print('> NOT AS A SINGULAR PHENOMENON LIKE THE CRASHING OF ROCKS')
            print('> BUT AS A TANGLE OF POSSIBILITIES, ALL BOUND UP')
            print('> AND FEEDING UPON ONE ANOTHER.')
        print('')

    def do_turn (self, player):
        # choose action
        action_options = self.player_options(player)
        valid_actions = [action for action, options in action_options.items() if len(options) > 0]
        # skip turns for players without options -- ex, no units, etc.
        if len(valid_actions) > 0:
            # print latest map
            self.print_map()
            # get player choice
            print('')
            print('Player %s, how will you act?' % str(player + 1))
            print('')
            print_options(valid_actions)
            action = choose(valid_actions)
            # resolve action
            options = action_options[action]
            action_func = getattr(self, '%s_action' % action.lower())
            print_func = print_coords if action != ADVANCE else print_advance_coords
            if len(options) == 1:
                choice = options[0]
            else:
                print_func(options)
                choice = choose(options)
            action_func(choice)

    def end_round (self):
        scores = super(InputGame, self).end_round()
        if scores:
            self.print_map()
            self.conclusion(scores)
        return scores

    def print_map (self):
        # space is abc
        # - a: infra. 0: _, 1: -, 2: *, impassable: x
        # - b: player. 1, 2, 3, 4. none: _
        # - c: unit. squadron: s, battalion: B, none: _
        # ex: ___, for an undeveloped, unclaimed, unoccupied space
        # ex: *2B, for a 2-infra space claimed by player 2, occupied by a battalion
        print('')
        print('   ' + '   '.join(X_ROW))
        for y in ROW_SIZE:
            row = []
            for x in ROW_SIZE:
                space = self.space(x, y)
                if space._impassable:
                    infra = 'x'
                elif space._infra == 0:
                    infra = '_'
                elif space._infra == 1:
                    infra = '-'
                elif space._infra == 2:
                    infra = '*'
                unit = self.unit(x, y)
                if unit:
                    player = unit._player + 1 # 0-index -> 1-index
                    char = 'B' if unit._level == 2 else 's'
                else:
                    char = '_'
                    if space.claimed:
                        player = space.claimant + 1 # 0-index -> 1-index
                    else:
                        player = '_'
                symbol = "%s%s%s" % (infra, player, char)
                row.append(symbol)
            print(str(BOARD_SIZE - y) + ' ' + ' '.join(row))

if __name__ == '__main__':
    InputGame.introduction()
    if len(sys.argv) > 1:
        raw_players = sys.argv[1]
        players = int(raw_players)
    else:
        print('How many players?')
        while True:
            raw_players = input('Choose 2 - 4: ')
            # parse choice from string to number, or ask for correct input
            try:
                players = int(raw_players)
                assert players >= 2 and players <= 4
                break
            except Exception:
                print('Invalid choice. Must be 2, 3, or 4.')
    game = InputGame(players)
    game.play()
