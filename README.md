# FRCstratometer
Simulate First Robotics Challenge games to help determine the effectiveness of different strategies. It does this by running a series of game simulations and illustrating
the score results. For each game, a user-created *strategy function* sets
what actions will be performed by the bot and the typical time it takes to
complete that action.

This software is written in Python and requires the following libraries:

- **numpy** for numerical operations.
- **Matplotlib** for data visualization.

## Writing Strategy Functions.

The strategy functions take, as input, a **status dictionary**. Based on the
game status, it decides what action to take. The action is returned to the
game object as a function that is called (see below).

## Writing Action Functions