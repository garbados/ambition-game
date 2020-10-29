# ambition-game

This project contains the digital board-game *Ambition*. This file explains how
to run and play the game. Multiple players can play together in a single
computer. You can even run the game on shared infrastructure and tmux both
players into the game's terminal!

## Rules

> The world is ending.
> The sky churns with poison and toxic seas boil.
> Your people must survive.
> Will they?

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
random adjacent space.

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

Terminology:

- *Despoiled*: A despoiled space is impassable. Units cannot move onto it nor
move over it. Despoiled spaces are so toxic that they cannot be restored.
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

Further thoughts:

- Secret win conditions: At the start of the game, each player receives a unique
win condition from the following deck. That player wins only if their condition
is met.
  - Death Cult: No players survive.
  - Warlord: Destroy at least one unit for each player in the game.
  - Ozymandias: Have the most infrastructure, regardless of whether anyone survives.
  - Highlander: There can be only one! (Only one player survives. It doesn't have to be you!)
  - Malthus: Half (rounded up) of all players survive. No more and no less.
  - Humanitarian: All players survive.
- AI players:
  - Despoiler: Despoils with a random unit every turn, trying to run out the
  clock before anyone can prepare for the end.
  - Overseer: Advances battalions to the center of the map to create a large
  flanking zone, in order to control the activities of other players. Once the
  center is controlled, squadrons develop tiles to prepare for the end.
  - Technocrat: Squadrons develop spaces. If no squadrons remain, muster and
  continue.

## Usage

First, install [Python 3](https://www.python.org/). Then:

```bash
$ python game.py

AMBITION - a game by garbados

> THE WORLD IS ENDING.
> THE SKY CHURNS WITH POISON AND TOXIC SEAS BOIL.
> YOUR PEOPLE MUST SURVIVE.
> WILL THEY?

How many players?

...
```

Each player is prompted in turn for their action. Once an action is chosen,
valid parameters are presented to the player, such as by presenting a list of
possible moves for a unit.
