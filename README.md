# ambition-game

This project contains the digital board-game *Ambition*. This file explains how
to run and play the game. Up to four players can play together on a single
computer. You can even run the game on shared infrastructure and tmux multiple
players into the game's terminal!

## Rules

```
> THE WORLD IS ENDING.
> THE SKY CHURNS WITH POISON AND TOXIC SEAS BOIL.
> YOUR PEOPLE MUST SURVIVE.
> WILL THEY?
```

On an 6x6 square board, two to four players compete. Each player begins with two
*squadrons* on two spaces with 1 *infrastructure*. Here are those spaces for
each player, keyed by their number (first player: 1, second player: 2, etc.):

```
- - 1 1 - -
- - - - - -
3 - - - - 4
3 - - - - 4
- - - - - -
- - 2 2 - -
```

One by one they choose actions -- first player first, second player second, etc.
-- until all players have acted. When all players have taken their turn, the
round ends and a new round begins.

At the end of each round one random passable, unclaimed space is *despoiled*,
making it impassable. If there is a unit on this space, it is shunted to a
random adjacent space. If all adjacent spaces are occupied or impassable, the
unit is destroyed.

When there are no passable, unclaimed spaces left on the board, the game ends.
Whoever has the most *infrastructure* wins. Players with more than 10
*infrastructure* survive the season of destruction that follows the game.

On a player's turn, they must choose one of the following actions:

- **Develop**: Raise the *infrastructure* of a space by 1, to a maximum of 2.
- **Despoil**: Lower the *infrastructure* of a space to 0. If it is already 0,
the space becomes *despoiled*, making it impassable for the rest of the game.
- **Muster**: Spawn a unit on a space you control. If its *infrastructure* is 1,
spawn a *squadron*. If it is 2, spawn a *battalion*.
- **Advance**: Move a unit. If it moves onto the space of another unit that is
*flanked*, that unit is destroyed.

### Terminology

- *Despoiled*: A despoiled space is impassable. Units cannot move onto it, but
*battalions* can jump over it. *Despoiled* spaces are so toxic that they cannot
be restored.
- *Infrastructure*: A space can have 0, 1, or 2 *infrastructure*. It is a
measure of the development of an area, including population centers as well as
military assets. More developed areas can field more powerful units. Communities
require at least 10 *infrastructure* to maintain the equipment and processes
needed to survive the climax of the apocalypse.
- *Claimed / Unclaimed*: A space is *unclaimed* while it has 0 *infrastructure*.
Once it has more than 0 *infrastructure*, it is *claimed* by the last player to
have a unit on that space. Thus, a *claimed* space can be seized by moving a
unit onto it.
- *Flanked*: A unit is *flanked* if more than one enemy unit could move onto its
space. For example, a unit adjacent to at least two *squadrons* controlled by
other players is *flanked* because both *squadrons* could move onto it.
- *Squadron*: A unit that can move one space on an **advance** action.
- *Battalion*: A unit that can move two spaces on an **advance** action. This
means it can *flank* at a range of two spaces.

### Reading the board

Each space on the board is represented by three characters which encode the
different properties of a space.

- The first character is the *infrastructure* level. `_` means the space has no
*infrastructure*; `-` means it has 1; `*` means it has 2. `x` means the space is
*despoiled*.
- The second character indicates the player that has *claimed* the space. If the
space is occupied by a unit, this also indicates who that unit belongs to. If
the space is *unclaimed*, the second character will be `_`.
- The third character indicates the presence and level of the unit occupying the
space. If the space is not occupied by a unit, the third character will be `_`.
If it is occupied by a squadron, the character will be `s`. If by a battalion,
`B`.

For example:

- `___` indicates a space with no *infrastructure*, no claimant, and no unit.
- `-1s` indicates a space with 1 *infrastructure* and a squadron belonging to
player 1.
- `*4_` indicates a space with 2 *infrastructure* claimed by player 4, but which
is not occupied by a unit.

## Usage

First, get the source code with [git](https://git-scm.com/):

```
$ git clone https://github.com/garbados/ambition-game
$ cd ambition-game
```

Then, using [Python](https://www.python.org/), run the game:

```
$ python game.py

AMBITION - a game by garbados

> THE WORLD IS ENDING.
> THE SKY CHURNS WITH POISON AND TOXIC SEAS BOIL.
> YOUR PEOPLE MUST SURVIVE.
> WILL THEY?

How many players?
Choose 2 - 4:
```

Each player is prompted in turn for their action. Once an action is chosen,
valid parameters are presented to the player, such as by presenting a list of
possible moves for a unit.

You can also play a solitaire version of the game by running `solitaire.py`,
in which the other three players are controlled by AI.

## Contributing

To report a bug, please file an [issue](https://github.com/garbados/ambition-game/issues).
Generally speaking, I won't humor feature requests. Feel free to file them anyway.

## License

See [LICENSE.md](./LICENSE.md).
