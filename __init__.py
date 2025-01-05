#!/usr/bin/env python3

'''
FRC Stratometer.

See the README for more information on writing the strat function.
'''

import numpy as np


class FrcGame(object):
    '''
    Game object for simulating one game.
    '''

    def __init__(self, stratfunc, gametime=150, autontime=30,
                 endgametime=120):
        '''
        Set up object.

        Parameters
        ----------
        stratfunc : function object
            A function that sets what action will be taken by the robot.
            It must take, as inputs, the current simulation time.
        gametime : float, defaults to 150
            Set the total game time in seconds.
        autontime : float, defaults to 30
            Set the autonomous period in seconds.
        endgametime : float, defaults to 120
            Set the time, in seconds, where endgame begins.
        '''

        # Stash strategy:
        self.strat = stratfunc

        # Stash critical values as object attributes:
        self.gametime = gametime
        self.autontime, self.endgametime = autontime, endgametime

        # Initialize tracking variables:
        self.gametime, self.score = [0], [0]
        # Set broad scoring categories for TOTAL points:
        self.points_auton = 0
        self.points_tele = 0
        self.points_end = 0

        # Create game status.
        self.status = {'time': 0, 'auton': True, 'endgame': False,
                       'autontime': autontime, 'gametime': gametime,
                       'endgametime': endgametime, 'gameover': False}

    def reset_field(self):
        '''
        Reset values for a new simulation, but keep "robot-specific" values
        (e.g., strategy function).
        '''

        # Initialize tracking variables:
        self.gametime, self.score = [0], [0]
        # Set broad scoring categories for TOTAL points:
        self.points_auton = 0
        self.points_tele = 0
        self.points_end = 0

        # Create game status.
        self.status = {'time': 0, 'auton': True, 'endgame': False,
                       'gameover': False}

    def run_game(self):
        '''Run game and save scoring values.'''

        tnow = 0.0  # Set initial time.

        # ##AUTONOMOUS PERIOD## #
        while tnow < self.autontime:
            # Pick action based on game status:
            action = self.strat(self.status)

            # Perform action and get change in time, points:
            dtime, dpoints = action()

            # Update time:
            tnow += dtime

            # Score points if we did it before end of auton period.
            if tnow < self.autontime:
                self.score.append(self.score[-1] + dpoints)
                self.time.append(self.gametime[-1] + dtime)

        # Stash auton points:
        self.points_auton = self.score[-1]

        # After auton, hard-set game clock:
        tnow = self.autontime

        # Update status.
        self.status['auton'] = False

        # ## TELEOP PERIOD ## #
        while tnow < self.gametime:
            # Pick action based on game status:
            action = self.strat(self.status)

            # Perform action and get change in time, points:
            dtime, dpoints = action()

            # Update time:
            tnow += dtime

            # Score points if we did it before end of auton period.
            if tnow < self.gametime:
                self.score.append(self.score[-1] + dpoints)
                self.time.append(self.gametime[-1] + dtime)

        # Stash teleop points.
        self.points_tele = self.score[-1] - self.points_auton

        # ### END GAME ### #
        # Set endgame status values (tbd.)
        self.score.append(self.score[-1])
        self.time.append(self.gametime[-1])

        # End game.
        self.status['gameover'] = True

    def viz_game():
        '''
        Create single-game visualizations.
        '''

        if not self.status['gameover']:
            raise ValueError('Simulation not complete.')

        # Figure 1:
