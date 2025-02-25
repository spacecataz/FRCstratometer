#!/usr/bin/env python3

'''
Reefscape: 2025 FRC Season
'''

import numpy as np
from FRCstratometer import roll_for_time, roll_for_success


def init_game_status(status, nloaded_coral=3):
    '''
    Initialize game status to include Reefscape elements.

    Parameters
    ----------
    status : dictionary
        Status dict created by game object.
    nloaded_coral : int, defaults to 3
        Set the number of pre-loaded coral on the alliance bots.
    '''

    # Initialize coral on reef:
    status['coral_l1'] = 0
    status['coral_l2'] = 0
    status['coral_l3'] = 0
    status['coral_l4'] = 0
    status['coral_floor'] = 3
    status['coral_station'] = 60 - nloaded_coral


class FrcBot(object):
    '''
    Example bot class.
    '''

    def __init__(self):
        # Set status variables for bot:
        self.has_coral = True    # Is bot holding coral?
        self.has_algae = False   # Is bot hodling algae?

        # Did we complete our autonomous?
        self.auton_complete = False

    def get_coral(self, status, avgtime=10, stddev=5.0, success_rate=.9):
        '''Move and obtain one coral.'''
        if self.has_coral:
            return 0, 0

        self.has_coral = roll_for_success(success_rate)
        return roll_for_time(avgtime, stddev), 0

    def place_coral(self, status, avgtime=5, stddev=2.5, succrate=.75):
        '''Deliver coral to L1. Always "lose" the coral.'''

        # If we don't have coral, no time and no points.
        if not self.has_coral:
            return 0, 0

        # Drop coral:
        self.has_coral = False

        # Place coral with success rate:
        return roll_for_time(avgtime, stddev), 2*roll_for_success(succrate)

    def remove_algae(self, status):
        pass

    def sleep(self, status, sleeptime=60):
        '''
        Sleep (do nothing) for sleeptime seconds.
        '''

        return sleeptime, 0

    def simple_auton(self, status, duration=10):
        '''
        Simple deliver-the-coral type auton. Returns time taken and points
        obtained.
        '''

        if self.auton_complete:
            return 15, 0

        # Deliver 1 coral to L1.
        if self.has_coral:
            status['coral_l1'] += 1
            self.has_coral = False

        # Auton is complete!
        self.auton_complete = True

        # Return time taken and points obtained (1 L1 delivery and leave.)
        return duration, 3+3

    def simple_coral_strat(self, status, auton=simple_auton):
        '''
        A strategy that focuses solely on obtaining and delivering coral.
        '''

        # Auton:
        if status['auton']:
            return self.simple_auton

        # Tele:
        if self.has_coral:
            return self.place_coral
        else:
            return self.get_coral


